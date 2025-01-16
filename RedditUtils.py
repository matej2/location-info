import os
import re

import praw
from praw.exceptions import RedditAPIException
from praw.models import Submission, Comment
from psaw import PushshiftAPI

from WikiClient import WikiClient
from const import Const
from replies import get_response_message


class RedditUtils:
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASS')

    def __init__(self):
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent='windows:github.com/matej2/location-info:v0.6 (by /u/mtj510)',
                                  username=self.username,
                                  password=self.password)
        if not self.reddit.read_only:
            print("Connected and running.")

    def get_or_create_meta_post(self):
        """
        Get or create meta post
        :return:
        praw.models.Submission: A meta post
        """
        api = PushshiftAPI()
        sub = self.reddit.subreddit('u_LocationInfoBot')

        gen = api.search_submissions(filter=['title', 'selftext', 'url'], limit=20, q='meta', author=Const.user)
        result = list(gen)

        if result == [] or result is None or result[0].selftext == '':
            post = sub.submit(title='meta', selftext='{ "status": "created" }')
        else:
            post = Submission(self.reddit, url=result[0].url)
        return post

    @staticmethod
    def reply_to_comment(city: str, target_comment: Comment):
        """
        :return:
        str: Comment id
        """

        if city is None:
            new_comment = get_response_message(None, Const.NO_BODY, None)
        else:
            wiki_meta = WikiClient.get_location_meta(city)

            if wiki_meta is None:
                new_comment = get_response_message(None, Const.LOC_NOT_FOUND.format(city), None)
            else:
                nearby_locations = WikiClient.get_nearby_locations(wiki_meta.lon, wiki_meta.lat)
                new_comment = get_response_message(wiki_meta.title, wiki_meta.desc, nearby_locations)

            print(Const.successfully_processed(city))

        try:
            result_comment = target_comment.reply(new_comment)
        except RedditAPIException as e:
            print(e)
        return result_comment.id

    @staticmethod
    def get_location_from_comment(comment: Comment):
        """
        :return:
        str: Location name | None
        """
        result = re.search('Information for location:\s*(.*):$', comment.body, flags=re.IGNORECASE | re.MULTILINE)
        if result is not None:
            return result.group(1)
        else:
            return None
