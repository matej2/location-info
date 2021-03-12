import os
import time

import praw
import re

mention = "u/LocationInfoBot"
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
username = os.environ.get('USERNAME')
password = os.environ.get('PASS')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Location info bot by /mtj510',
                     username=username,
                     password=password)
# Cities
CITY_REGEX = '.+$'

WIKI_URL = 'https://en.wikipedia.org/wiki/{}'
VISIT_URL = 'https://www.visitacity.com/en/{}'
MAPS_URL = 'https://www.google.com/maps/search/{}'

SPACE_REGEX = '\s+'
BODY_REGEX = f'{mention}\s*({CITY_REGEX})'

FOOTER = 'I am a bot and this was an automated message. I am not responsible for the content neither am I an author. If you think this message is problematic, please contact developers mentioned below.\n\n^(Author: [u/mtj510](https://www.reddit.com/user/mtj510) | [how to use this bot](https://github.com/matej2/location-info/blob/master/README.md#example) | [github](https://github.com/matej2/location-info) )'

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

def send_link(city, where):
    message = ''
    isSuccessful = False

    if city is None:
        message += 'No city found. Please try again.'
    else:
        # TODO: Remove once the bot gets higher rate limits
        print(message)
        try:
            message = f'Information for city: {city}. \n\n' + f'- wiki: {get_wiki_link(city)}\n\n- visit: {get_visit_link(city)}\n\n- map: {get_map_link(city)}\n\n'
            isSuccessful = True
        except:
            print('Rate limited')

    message += f'---\n\n{FOOTER}'

    where.reply(message)
    return isSuccessful

def main():
    inbox = list(reddit.inbox.unread())
    inbox.reverse()

    for item in inbox:
        if mention in item.body:
            text = item.body
            msg = re.search(BODY_REGEX, text).group(1)

            if send_link(msg, item):
                item.mark_read()
            time.sleep(10)

while True:
    main()
    time.sleep(5)
