import re
import urllib

WIKI_URL = 'https://en.wikipedia.org/wiki/{}'
VISIT_URL = 'https://www.visitacity.com/en/{}/activities/all-activities'
MAPS_URL = 'https://www.google.com/maps/search/{}'
BOOKING_URL = 'https://www.booking.com/searchresults.sl.html?ss={}'
WANDER_URL = 'http://www.wandermap.net/sl/search/?q={}'
TB_URL = 'https://www.tumblr.com/search/{}'
PT_URL = 'https://www.pinterest.com/search/pins/?q={}'

FOOTER = '\n\n---\n\n^(I am a bot and this was an automated message. I am not responsible for the content neither am ' \
         'I an author of this content. If you think this message is problematic, please contact developers mentioned ' \
         'below.)\n\n^(Author: [u/mtj510](https://www.reddit.com/user/mtj510) | [how to use this bot](' \
         'https://github.com/matej2/location-info/blob/master/README.md#example) | [github](' \
         'https://github.com/matej2/location-info) ) '
NO_BODY = 'Location name not found in comment body.'
LOC_NOT_FOUND = 'No summary found for {}. Either unknown location or mistype.'
SPACE_REGEX = '\s+'


def get_visit_link(txt):
    parsed = re.sub(SPACE_REGEX, '-', txt)
    return VISIT_URL.format(parsed)


def get_map_link(txt):
    parsed = re.sub(SPACE_REGEX, '+', txt)
    return MAPS_URL.format(parsed)


def get_booking_url(txt):
    parsed = re.sub(SPACE_REGEX, '+', txt)
    return BOOKING_URL.format(parsed)


def get_wander_url(txt):
    parsed = re.sub(SPACE_REGEX, '+', txt)
    return WANDER_URL.format(parsed)


def get_th_url(txt):
    parsed = re.sub(SPACE_REGEX, '+', txt)
    return TB_URL.format(parsed)


def get_pt_url(txt):
    parsed = urllib.parse.quote_plus(txt)
    return PT_URL.format(parsed)


def get_response_message(city, msg, nearby: str):
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
