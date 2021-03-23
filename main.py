import os
import re
import urllib
from time import sleep

import praw
import requests
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


def get_wiki_link(txt):
    str = re.sub(SPACE_REGEX, '_', txt)
    return WIKI_URL.format(str)

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
    summary = ''

    if city is None:
        message += 'No city found. Please try again.'
    else:
        # TODO: Remove once the bot gets higher rate limits
        print(message)

        try:
            summary += wikipedia.summary(city, sentences=3) + '\n\n'
        except:
            summary += 'No summary found.'

        visit_link = get_visit_link(city)

        message = f'Information for location: {city}:\n\n {summary} \n\n- wiki: {get_wiki_link(city)}\n\n- map: {get_map_link(city)}\n\n- hotels: {get_booking_url(city)}\n\n- hiking: {get_wander_url(city)}\n\n- social: [ig]({get_ig_url(city)}), [fb]({get_fb_url(city)}), [tw]({get_tw_url(city)}), [thumblr]({get_th_url(city)}), [pinterest]({get_pt_url(city)})'

        if requests.get(visit_link).status_code == 200:
            message += f'\n\n- visit: {visit_link}\n\n'


        print(f'{city} succsessfully processed')
        isSuccessful = True

    message += f'{FOOTER}'

    where.reply(message)
    return isSuccessful

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
