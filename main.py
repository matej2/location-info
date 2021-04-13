import json
import os
import re
import urllib
from time import sleep
from requests import get

import praw
import requests
import wikipedia
from wikidata.client import Client

user = 'LocationInfoBot'
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
# TELEPORT_URL = 'https://teleport.org/cities/madrid'
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
COMMA_REGEX = ',+'

FOOTER = '\n\n---\n\n^(I am a bot and this was an automated message. I am not responsible for the content neither am I an author of this content. If you think this message is problematic, please contact developers mentioned below.)\n\n^(Author: [u/mtj510](https://www.reddit.com/user/mtj510) | [how to use this bot](https://github.com/matej2/location-info/blob/master/README.md#example) | [github](https://github.com/matej2/location-info) )'
NO_BODY = 'Location name not found in comment body.'
LOC_NOT_FOUND = 'No summary found for {}. Either unknown location or mistype.'

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
    comment = ''

    if city is None:
        comment = get_response_message(None, NO_BODY , None)
    else:
        # TODO: Remove once the bot gets higher rate limits
        print(message)

        wikiObj = get_location_meta(city)

        if wikiObj is None:
            comment = get_response_message(None, LOC_NOT_FOUND.format(city) , None, 'None')
        else:
            nearby = get_nearby_locations(wikiObj.lon, wikiObj.lat)
            comment = get_response_message(wikiObj.title, wikiObj.desc, wikiObj.link, nearby)

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
            page = wikipedia.page(title=result, auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            return None
        except wikipedia.PageError as e:
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


def get_response_message(city, msg, link, nearby):
    if city is None:
        message = f'''
{msg}
{FOOTER}
'''
    else:
        message = f'''
Information for location: {city}:\n\n {msg} \n\n- locations/events nearby: {nearby}\n\n- links: [wiki]({link}) ~ [map]({get_map_link(city)}) ~ [hotels]({get_booking_url(city)}) ~ [hiking]({get_wander_url(city)}) ~ [thumblr]({get_th_url(city)}) ~ [pinterest]({get_pt_url(city)})
{FOOTER}'''

    return message

def get_nearby_locations(lon, lat):
    list = wikipedia.geosearch(lon, lat, results=10)
    return ', '.join(list)

# See https://stackoverflow.com/a/33336820/10538678
def get_taxonomy(title):
    r = requests.get('https://en.wikipedia.org/w/api.php?action=query&titles=' + title  + '&prop=revisions&rvprop=content&rvsection=0&format=json')

    #https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&prop=revisions&format=json&rvprop=content&rvsection=0&rvcontentformat=text%2Fx-wiki&titles=Foraminifera

    a = ''
    t = json.loads(r.text)
    for i in t['query']['pages']:
        a = t['query']['pages'][ i ]['revisions'][0]['*']

    taxobox = a
    taxobox = taxobox[taxobox.index("\n[["):]
    taxobox = taxobox[:taxobox.index("}}")]

    taxobox = taxobox.replace('[[', '')
    taxobox = taxobox.replace(']]', '')
    taxobox = taxobox.replace('<br>', '')
    taxobox = taxobox.replace("''", '')
    taxobox = taxobox.replace("&nbsp;", ' ')

    t = []
    for i in taxobox.split("\n"):
        if len(i) > 0:
            if '|' in i:                    # for href titles
                t.append( i.split('|')[1] ) # for href titles
            else:
                t.append( i )

    return "\n".join(t)


def get_metadata(loc):
    # Using request as a temp solution because wptools cannot be installed
    res = get('https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={}&format=json'.format(loc))
    wikidata_id = None

    if res.status_code == 200:
        try:
            wiki_res = json.loads(res.content)
            wiki_pages = wiki_res['query']['pages']
            page_id = list(wiki_pages.keys())[0]
            wikidata_id = wiki_pages[page_id]['pageprops']['wikibase_item']
        except:
            print('Wiki API response is not found.')

        print(wikidata_id)

        if wikidata_id is not None:
            client = Client()
            entity = client.get(wikidata_id, load=True)
        print ('ok')

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
