import os
import re
import urllib
from time import sleep

import praw
import wikipedia

user =  'LocationInfoBot'
mention = f'u/{user}'
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
username = os.environ.get('USERNAME')
password = os.environ.get('PASS')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='windows:github.com/matej2/location-info:v0.5 (by /u/mtj510)',
                     username=username,
                     password=password)
# Cities
CITY_REGEX = '.+$'

WIKI_URL = 'https://en.wikipedia.org/wiki/{}'
VISIT_URL = 'https://www.visitacity.com/en/{}/activities/all-activities'
MAPS_URL = 'https://www.google.com/maps/search/{}'
#TELEPORT_URL = 'https://teleport.org/cities/madrid'
BOOKING_URL = 'https://www.booking.com/searchresults.sl.html?ss={}'
WANDER_URL = 'http://www.wandermap.net/sl/search/?q={}'
FB_URL = 'https://www.facebook.com/search/places/?q={}'
IG_URL = 'https://www.instagram.com/explore/tags/{}/'
TW_URL = 'https://twitter.com/search?q={}&src=typeahead_click&f=image'
TB_URL = 'https://www.tumblr.com/search/{}'
PT_URL = 'https://www.pinterest.com/search/pins/?q={}'

# TODO Add links - info about country

SPACE_REGEX = '\s+'
NOT_CHAR = '\W+'
BODY_REGEX = f'{mention}\s*({CITY_REGEX})'

FOOTER = '\n\n---\n\n^(I am a bot and this was an automated message. I am not responsible for the content neither am I an author of this content. If you think this message is problematic, please contact developers mentioned below.)\n\n^(Author: [u/mtj510](https://www.reddit.com/user/mtj510) | [how to use this bot](https://github.com/matej2/location-info/blob/master/README.md#example) | [github](https://github.com/matej2/location-info) )'

if reddit.read_only == False:
    print("Connected and running.")

class LocationMeta(object):
    def __init__(self, title, desc, lon, lat, link):
        self.title = title
        self.desc = desc
        self.lon = lon
        self.lat = lat
        self.link = link

    def __str__(self):
        return f'Location name: {self.name}'


def get_visit_link(txt):
    str = re.sub(SPACE_REGEX, '-', txt)
    return VISIT_URL.format(str)

def get_map_link(txt):
    str = re.sub(SPACE_REGEX, '+', txt)
    return MAPS_URL.format(str)

def get_booking_url(txt):
    str = re.sub(SPACE_REGEX, '+', txt)
    return BOOKING_URL.format(str)

def get_wander_url(txt):
    str = re.sub(SPACE_REGEX, '+', txt)
    return WANDER_URL.format(str)

def get_fb_url(txt):
    str = urllib.parse.quote_plus(txt)
    return FB_URL.format(str)

def get_ig_url(txt):
    str = re.sub(NOT_CHAR, '', txt)
    return IG_URL.format(str)

def get_tw_url(txt):
    str = urllib.parse.quote_plus(txt)
    return TW_URL.format(str)

def get_th_url(txt):
    str = re.sub(SPACE_REGEX, '+', txt)
    return TB_URL.format(str)

def get_pt_url(txt):
    str = urllib.parse.quote_plus(txt)
    return PT_URL.format(str)

def send_link(city, where):
    message = ''
    isSuccessful = False
    wikiObj = None
    msg = ''
    comment = ''

    if city is None:
        message += 'No city found in comment. Please try again.'
    else:
        # TODO: Remove once the bot gets higher rate limits
        print(message)

        wikiObj = get_location_meta(city)

        if wikiObj is None:
            msg = 'No summary found.'
            comment = get_response_message(None, msg, None)
        else:
            comment = get_response_message(wikiObj.title, wikiObj.desc, wikiObj.link)

        print(f'{city} succsessfully processed')
        isSuccessful = True


    where.reply(comment)
    return isSuccessful


def get_location_meta(city):
    search = wikipedia.search(city)
    st = 0

    if search is None:
        return False

    # Get first location
    for result in search:
        try:
            page = wikipedia.page(title=result)
        except wikipedia.DisambiguationError as e:
            return None
        except wikipedia.PageError:
            return None

        for attr in page.categories:
            if attr == 'Coordinates on Wikidata':
                summary = wikipedia.summary(page.title, sentences=3)
                return LocationMeta(page.title, summary, page.coordinates[0], page.coordinates[1], page.url)

        if st > 3:
            return None
        st = st + 1

    return None


def get_response_message(city, summary, link):
    body = ''
    if city is None:
        message = f'''
No summary found
{FOOTER}
'''
    else:
        message = f'''
Information for location: {city}:\n\n {summary} \n\n- wiki: {link}\n\n- map: {get_map_link(city)}\n\n- hotels: {get_booking_url(city)}\n\n- hiking: {get_wander_url(city)}\n\n- social: [instagram]({get_ig_url(city)}) ~ [facebook]({get_fb_url(city)}) ~ [twitter]({get_tw_url(city)}) ~ [thumblr]({get_th_url(city)}) ~ [pinterest]({get_pt_url(city)})
{FOOTER}'''

    return message


def main():
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
    for comment in reddit.redditor(user).comments.new(limit=20):
        if comment.score < 0:
            print(f'Removing comment {comment.body}')
            comment.delete()
