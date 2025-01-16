class Const:
    # Cities
    CITY_REGEX = '.+$'

    NOT_CHAR = '\W+'
    COMMA_REGEX = ',+'
    SPECIAL_CHARS = '[^A-Za-z0-9\s,]'

    # TODO Add links - info about country
    TRIGGER_PHARSE = 'location:'
    TRIGGER_SUBREDDITS = 'naturephotography,AdventurePhotography,snow,UrbanExploring,Outdoors'
    KEYWORD = 'Location:\s*([^.\n]+)'

    # Response messages
    FOOTER = '\n\n---\n\n^(Content is intended to improve search engine optimization by providing information about location.' \
              ' I am a bot and this was an automated message.' \
             'below.)\n\n^(Author: [u/mtj510](https://www.reddit.com/user/mtj510) | [how to use this bot](' \
             'https://github.com/matej2/location-info/blob/master/README.md#example) | [github](' \
             'https://github.com/matej2/location-info) ) '

    NO_BODY = 'Location name not found in comment body.'
    LOC_NOT_FOUND = 'No summary found for {}. Either unknown location or mistype.'
    NOT_DETECTED = f'Did not detect any message. Please try again\n\n{FOOTER}'

    SPACE_REGEX = '\s+'
    NONE = 'None'

    # Reddit meta
    user = 'LocationInfoBot'
    mention = f'u/{user}'

    @staticmethod
    def successfully_processed(city: str):
        """
        :return: str
        """
        return f'{city} successfully processed'

    @staticmethod
    def body_regex(mention: str):
        """
        :return: str
        """
        return f'{mention}\s*({Const.CITY_REGEX})'
