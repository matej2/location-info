import os
import re

import praw
import requests
import wikipedia

mention = "u/LocationInfoBot"
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

# TODO Add links - info about country

SPACE_REGEX = '\s+'
BODY_REGEX = f'{mention}\s*({CITY_REGEX})'

FOOTER = '\n\n---\n\nI am a bot and this was an automated message. I am not responsible for the content neither am I an author of this content. If you think this message is problematic, please contact developers mentioned below.\n\n^(Author: [u/mtj510](https://www.reddit.com/user/mtj510) | [how to use this bot](https://github.com/matej2/location-info/blob/master/README.md#example) | [github](https://github.com/matej2/location-info) )'

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

        try:
            message = f'Information for city: {city}:\n\n {summary} \n\n- wiki: {get_wiki_link(city)}\n\n- map: {get_map_link(city)}\n\n- hotels: {get_booking_url(city)}\n\n- hiking: {get_wander_url(city)}'

            if requests.get(visit_link).status_code == 200:
                message += f'\n\n- visit: {visit_link}\n\n'

            print(f'{city} succsessfully processed')
            isSuccessful = True
        except:
            print('Rate limited')

    message += f'{FOOTER}'

    where.reply(message)
    return isSuccessful

def main():
    inbox = list(reddit.inbox.unread())
    inbox.reverse()

    for item in inbox:
        if mention in item.body:
            text = item.body
            body = re.search(BODY_REGEX, text).group(1)

            if not body:
                item.reply(f'Did not detect any message. Please try again\n\n{FOOTER}')
            else:
                if send_link(body, item):
                    item.mark_read()
            break
