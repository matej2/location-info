import json
import re

import mwparserfromhell
import requests
import wikipedia
from mwparserfromhell.nodes.extras import Parameter
from wikipedia import WikipediaPage

from models import LocationMeta


class WikiClient:
    @staticmethod
    def get_location_meta(city: str):
        """
        Get location metadata
        :return:
        LocationMeta: Meta data
        """
        search = wikipedia.search(city)
        st = 0

        if search is None:
            return False

        for result in search:
            try:
                page = wikipedia.page(title=result, auto_suggest=False)
            except wikipedia.DisambiguationError:
                return None
            except wikipedia.PageError:
                return None

            if WikiClient.is_location(page):
                summary = wikipedia.summary(page.title, sentences=3, auto_suggest=False)
                return LocationMeta(page.title, summary, page.coordinates[0], page.coordinates[1], page.url)

            if st > 3:
                return None
            st = st + 1

        return None

    @staticmethod
    def is_location(page: WikipediaPage):
        """
        :return:
        bool: True if page is a location
        """
        for attr in page.categories:
            if attr == 'Coordinates on Wikidata':
                return True
        return False

    @staticmethod
    def get_nearby_locations(lon: float, lat: float):
        """
        :return:
        str: A list of nearby locations
        """
        loc_list = wikipedia.geosearch(lon, lat, results=10)
        return ', '.join(loc_list)