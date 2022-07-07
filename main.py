import json
import os
import re
from time import sleep

import mwparserfromhell
import praw
import requests
import wikipedia
from mwparserfromhell.nodes.extras import Parameter
from praw.exceptions import RedditAPIException
from praw.models import Submission
from psaw import PushshiftAPI

from models import LocationMeta
from replies import FOOTER, LOC_NOT_FOUND, get_response_message, NO_BODY

user = 'LocationInfoBot'
mention = f'u/{user}'
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
username = os.environ.get('USERNAME')
password = os.environ.get('PASS')

# Cities
CITY_REGEX = '.+$'

NOT_CHAR = '\W+'
BODY_REGEX = f'{mention}\s*({CITY_REGEX})'
COMMA_REGEX = ',+'
SPECIAL_CHARS = '[^A-Za-z0-9\s,]'

# TODO Add links - info about country
TRIGGER_PHARSE = 'location:'
TRIGGER_SUBREDDITS = 'naturephotography,AdventurePhotography,snow,UrbanExploring,Outdoors'
KEYWORD = 'Location:\s*([^.\n]+)'


def get_reddit_instance():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='windows:github.com/matej2/location-info:v0.6 (by /u/mtj510)',
                         username=username,
                         password=password)
    if not reddit.read_only:
        print("Connected and running.")
        return reddit
    else:
        return False


def send_link(city, where):

    if city is None:
        comment = get_response_message(None, NO_BODY, None)
    else:
        wiki_obj = get_location_meta(city)

        if wiki_obj is None:
            comment = get_response_message(None, LOC_NOT_FOUND.format(city), None, 'None')
        else:
            nearby = get_nearby_locations(wiki_obj.lon, wiki_obj.lat)
            comment = get_response_message(wiki_obj.title, wiki_obj.desc, wiki_obj.link, nearby)

        print(f'{city} successfully processed')

    try:
        comment = where.reply(comment)
    except RedditAPIException as e:
        print(e)
    return comment.id


def get_location_meta(city):
    search = wikipedia.search(city)
    st = 0

    if search is None:
        return False

    for result in search:
        try:
            page = wikipedia.page(title=result, auto_suggest=False)
        except wikipedia.DisambiguationError:
            return None
        except wikipedia.PageError:
            return None

        if is_location(page):
            summary = wikipedia.summary(page.title, sentences=3, auto_suggest=False)
            return LocationMeta(page.title, summary, page.coordinates[0], page.coordinates[1], page.url)

        if st > 3:
            return None
        st = st + 1

    return None


def is_location(page):
    for attr in page.categories:
        if attr == 'Coordinates on Wikidata':
            return True
    return False


def get_nearby_locations(lon, lat):
    loc_list = wikipedia.geosearch(lon, lat, results=10)
    return ', '.join(loc_list)


# See https://stackoverflow.com/a/33336820/10538678
def get_taxonomy(title):
    infobox = None
    parsed_params = []
    a = ''

    r = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&titles=' + title + '&prop=revisions&rvprop=content&rvsection'
                                                                            '=0&format=json')
    t = json.loads(r.text)

    for i in t['query']['pages']:
        a = t['query']['pages'][i]['revisions'][0]['*']

    template_list = mwparserfromhell.parse(a).filter_templates()
    for template in template_list:
        if 'Infobox' in template.name:
            infobox = template

    if infobox is None:
        return None
    else:
        for param in infobox.params:
            add_par = Parameter(
                name=param.name.strip(),
                value=re.sub('\\n', '', param.value.strip())
            )
            parsed_params.append(add_par)
        return parsed_params


def is_replied(submission):
    for comment in submission.comments:
        if comment.author.name == user:
            return True
    return False


def process_keywords():
    api = PushshiftAPI()
    r = get_reddit_instance()
    config = get_config()
    last_processed_key = 'last_processed'
    last_processed = ''

    # Retrieves subs ordered by time descending
    gen = api.search_submissions(
        limit=100,
        filter=['id', 'title', 'url'],
        q='Location:|location:',
        subreddit=TRIGGER_SUBREDDITS)
    results = list(gen)

    for s in results:
        if TRIGGER_PHARSE in s.title.lower():
            if s.id == config.get(last_processed_key):
                return True

            # extract the word from the comment
            body = re.search(KEYWORD, s.title, flags=re.IGNORECASE)

            if body is not None:
                word = re.sub(SPECIAL_CHARS, '', body.group(1)).strip()

                post = Submission(r, id=s.id)
                if is_replied(post) is False:
                    send_link(word, post)
                else:
                    return True

                if last_processed == '':
                    last_processed = post.id
                sleep(3)

    last = {
        last_processed_key: last_processed
    }
    update_config(last)
    return True


def get_meta_post():
    r = get_reddit_instance()
    api = PushshiftAPI()
    sub = r.subreddit('u_LocationInfoBot')

    gen = api.search_submissions(filter=['title', 'selftext', 'url'], limit=20, q='meta', author=user)
    result = list(gen)

    if result == [] or result is None or result[0].selftext == '':
        post = sub.submit(title='meta', selftext='{ "status": "created" }')
    else:
        post = Submission(r, url=result[0].url)
    return post


def update_config(obj):
    conf = get_meta_post()
    curr = json.loads(conf.selftext)

    curr.update(obj)

    updated = json.dumps(curr)
    conf.edit(updated)


def get_config():
    return json.loads(get_meta_post().selftext)


def main():
    reddit = get_reddit_instance()
    try:
        inbox = list(reddit.inbox.unread())
    except praw.exceptions.APIException:
        print('Rate limited.')
        return False
    inbox.reverse()

    for item in inbox:
        if mention.lower() in item.body.lower():
            text = item.body
            result = re.search(BODY_REGEX, text, flags=re.IGNORECASE)
            if result is not None:
                body = result.group(1)

                if send_link(body, item):
                    item.mark_read()
            else:
                item.reply(f'Did not detect any message. Please try again\n\n{FOOTER}')
            sleep(10)


def purge():
    reddit = get_reddit_instance()
    for comment in reddit.redditor(user).comments.new(limit=20):
        if comment.score < 0:
            print(f'Removing comment {comment.body}')
            comment.delete()
