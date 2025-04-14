import re
from time import sleep

from RedditUtils import RedditUtils
from const import Const


def main():
    reddit_client = RedditUtils()
    reddit_instance = reddit_client.reddit

    for inbox_item in reddit_instance.inbox.stream():

        if Const.mention.lower() in inbox_item.body.lower():
            found_location = RedditUtils.extract_location_from_comment(inbox_item)

            if found_location is not None:
                location_name = found_location.group(1)

                if reddit_client.reply_to_comment(location_name, inbox_item):
                    inbox_item.mark_read()
            else:
                inbox_item.reply(Const.NOT_DETECTED)
            sleep(10)


if __name__ == '__main__':
    main()

