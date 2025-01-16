import re
import urllib
from typing import Optional

from const import Const

WIKI_URL = 'https://en.wikipedia.org/wiki/{}'
VISIT_URL = 'https://www.visitacity.com/en/{}/activities/all-activities'
MAPS_URL = 'https://www.google.com/maps/search/{}'
BOOKING_URL = 'https://www.booking.com/searchresults.sl.html?ss={}'
WANDER_URL = 'http://www.wandermap.net/sl/search/?q={}'
TB_URL = 'https://www.tumblr.com/search/{}'
PT_URL = 'https://www.pinterest.com/search/pins/?q={}'

def get_visit_link(txt):
    parsed = re.sub(Const.SPACE_REGEX, '-', txt)
    return VISIT_URL.format(parsed)


def get_map_link(txt):
    parsed = re.sub(Const.SPACE_REGEX, '+', txt)
    return MAPS_URL.format(parsed)


def get_booking_url(txt):
    parsed = re.sub(Const.SPACE_REGEX, '+', txt)
    return BOOKING_URL.format(parsed)


def get_wander_url(txt):
    parsed = re.sub(Const.SPACE_REGEX, '+', txt)
    return WANDER_URL.format(parsed)


def get_th_url(txt):
    parsed = re.sub(Const.SPACE_REGEX, '+', txt)
    return TB_URL.format(parsed)


def get_pt_url(txt):
    parsed = urllib.parse.quote_plus(txt)
    return PT_URL.format(parsed)


def get_response_message(city, msg, nearby: Optional[str]):
    if city is None:
        message = f'''
{msg}
{FOOTER}
'''
    else:
        message = f'''
Information for location: {city}:\n\n {msg} \n\n
Locations/events nearby: {nearby}\n\n
{FOOTER}'''

    return message

def is_replied(submission):
    for comment in submission.comments:
        if comment.author is not None and comment.author.name == user:
            return True
    return False