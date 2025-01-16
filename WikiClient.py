import json
import re

import mwparserfromhell
import requests
import wikipedia
from mwparserfromhell.nodes.extras import Parameter

from models import LocationMeta


class WikiClient:
    @staticmethod
    def get_location_meta(city):
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
    def is_location(page):
        for attr in page.categories:
            if attr == 'Coordinates on Wikidata':
                return True
        return False

    @staticmethod
    def get_nearby_locations(lon, lat):
        loc_list = wikipedia.geosearch(lon, lat, results=10)
        return ', '.join(loc_list)

    # See https://stackoverflow.com/a/33336820/10538678
    @staticmethod
    def get_taxonomy(title):
        infobox = None
        parsed_params = []
        a = ''

        r = requests.get(
            'https://en.wikipedia.org/w/api.php?action=query&titles=' + title + '&prop=revisions&rvprop=content&rvsection'
                                                                                '=0&format=json')
        t = json.loads(r.text)

        for i in t['query']['pages']:
            a = t['query']['pages'][i]['revisions'][0]['*']

        template_list = mwparserfromhell.parse(a).filter_templates()
        for template in template_list:
            if 'Infobox' in template.name:
                infobox = template

        if infobox is None:
            return None
        else:
            for param in infobox.params:
                add_par = Parameter(
                    name=param.name.strip(),
                    value=re.sub('\\n', '', param.value.strip())
                )
                parsed_params.append(add_par)
            return parsed_params