import re
from time import sleep

from RedditUtils import RedditUtils
from const import Const


def main_stream():
    reddit_client = RedditUtils()
    reddit_instance = reddit_client.reddit

    for item in reddit_instance.inbox.stream():
        if Const.mention.lower() in item.body.lower():
            text = item.body
            result = re.search(Const.body_regex(Const.mention), text, flags=re.IGNORECASE)
            if result is not None:
                body = result.group(1)

                if reddit_instance.reply_to_comment(body, item):
                    item.mark_read()
            else:
                item.reply(Const.NOT_DETECTED)
            sleep(10)


