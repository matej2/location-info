import re
import urllib
from typing import Optional
from const import Const


class ResponseUtils:
    WIKI_URL = 'https://en.wikipedia.org/wiki/{}'
    VISIT_URL = 'https://www.visitacity.com/en/{}/activities/all-activities'
    MAPS_URL = 'https://www.google.com/maps/search/{}'
    BOOKING_URL = 'https://www.booking.com/searchresults.sl.html?ss={}'
    WANDER_URL = 'http://www.wandermap.net/sl/search/?q={}'
    TB_URL = 'https://www.tumblr.com/search/{}'
    PT_URL = 'https://www.pinterest.com/search/pins/?q={}'

    @staticmethod
    def get_visit_link(txt: str):
        parsed = re.sub(Const.SPACE_REGEX, '-', txt)
        return ResponseUtils.VISIT_URL.format(parsed)

    @staticmethod
    def get_map_link(txt: str):
        parsed = re.sub(Const.SPACE_REGEX, '+', txt)
        return ResponseUtils.MAPS_URL.format(parsed)

    @staticmethod
    def get_booking_url(txt: str):
        parsed = re.sub(Const.SPACE_REGEX, '+', txt)
        return ResponseUtils.BOOKING_URL.format(parsed)

    @staticmethod
    def get_wander_url(txt: str):
        parsed = re.sub(Const.SPACE_REGEX, '+', txt)
        return ResponseUtils.WANDER_URL.format(parsed)

    @staticmethod
    def get_th_url(txt: str):
        parsed = re.sub(Const.SPACE_REGEX, '+', txt)
        return ResponseUtils.TB_URL.format(parsed)

    @staticmethod
    def get_pt_url(txt: str):
        parsed = urllib.parse.quote_plus(txt)
        return ResponseUtils.PT_URL.format(parsed)

    @staticmethod
    def get_response_message(city: str, msg: str, nearby: Optional[str]):
        if city is None:
            message = f'''
    {msg}
    {Const.FOOTER}
    '''
        else:
            message = f'''
    Information for location: {city}:\n\n {msg} \n\n
    
    Links:\n
    [wiki]({ResponseUtils.WIKI_URL.format(city)})\n
    [visitacity]({ResponseUtils.get_visit_link(city)})\n
    [google maps]({ResponseUtils.get_map_link(city)})\n
    [booking]({ResponseUtils.get_booking_url(city)})\n
    [wandermap]({ResponseUtils.get_wander_url(city)})\n
    [tumblr]({ResponseUtils.get_th_url(city)})\n
    [pinterest]({ResponseUtils.get_pt_url(city)})\n
    Locations/events nearby: {nearby}\n\n
    {Const.FOOTER}'''

        return message
