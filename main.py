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

CITY_URL = 'https://en.wikipedia.org/wiki/{}'
CITY_REGEX = '.+$';
SPACE_REGEX = '\s+'
BODY_REGEX = f'{mention}\s*({CITY_REGEX})'

FOOTER = 'I am a bot and this was an automated message. I am not responsible for the content neither am I an author. If you think this message is problematic, please contact developers mentioned below.\n\n^(Author: u/mtj510, [source](https://github.com/matej2/location-info) )'

if reddit.read_only == False:
    print("Connected and running.")

def send_link(city, txt, where):
    message = f'Found match for {city}. \n\n' + f'Wiki: {CITY_URL.format(txt)}\n\n---\n\n{FOOTER}'

    if txt is None:
        where.reply('No city found, please check again.')
    else:
        # TODO: Remove once the bot gets higher rate limits
        print(message)
        try:
            where.reply(message)
            print('ok')
            return True
        except:
            print('Rate limited')
            return False

def main():
    inbox = list(reddit.inbox.unread())
    inbox.reverse()

    for item in inbox:
        if mention in item.body:
            text = item.body
            msg = re.search(BODY_REGEX, text).group(1)
            result = re.sub(SPACE_REGEX, '_', msg);

            if send_link(msg, result, item):
                item.mark_read()
            time.sleep(10)


while True:
    main()
    time.sleep(5)