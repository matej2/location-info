import unittest

from wikipedia import wikipedia

from RedditUtils import RedditUtils
from WikiClient import WikiClient
from replies import get_visit_link, get_map_link, get_response_message


class TestCommonMethods(unittest.TestCase):

    def setUpClass(self):
        self.wiki_client = WikiClient()
        self.reddit_client = RedditUtils()

    def setUp(self):
        self.test_link = 'https: // www.google.com/'
        self.test_location_short = 'Baykit'
        self.test_location = 'Baykit Airport'
        self.test_location_alt = 'Kansas_City,_Missouri'

    def test_link_generation(self):
        test_str = '\'test string ~!˘'
        visit_link = get_visit_link(test_str)
        map_link = get_map_link(test_str)

        self.assertEqual('https://www.visitacity.com/en/\'test-string-~!˘/activities/all-activities', visit_link)
        self.assertEqual('https://www.google.com/maps/search/\'test+string+~!˘', map_link)

    def test_location_meta(self):
        city_meta = self.wiki_client.get_location_meta(self.test_location_short)

        self.assertIsNotNone(city_meta)
        self.assertEqual(city_meta.title, self.test_location)
        self.assertEqual(city_meta.desc, 'Baykit Airport (Russian: Аэропорт Байкит) (ICAO: UNIB) is an airport in '
                                         'Krasnoyarsk Krai, Russia located 1 km (0.62 mi) west of Baykit. It is a '
                                         'major utilitarian transport airfield.')

    def test_nearby_locations(self):
        self.wiki_client.get_nearby_locations(
            61.676666670000003023233148269355297088623046875,
            96.3550000000000039790393202565610408782958984375
        )

    def test_is_page(self):
        test_loc = wikipedia.page(title=self.test_location, auto_suggest=False)
        self.assertEqual(self.wiki_client.is_location(test_loc), True)

    def test_response_message(self):
        nearby = 'Nothing'

        msg_valid = get_response_message(self.test_location, None, nearby)

        self.assertIn('Information for location: Baykit Airport', msg_valid)
        self.assertIn('locations/events nearby: Nothing', msg_valid)
        self.assertIn('links: [wiki](https: // www.google.com/)', msg_valid)

    def test_meta_post(self):
        meta = self.reddit_client.get_or_create_meta_post()

        self.assertIsNotNone(meta)


if __name__ == '__main__':
    unittest.main()
