class Const:
    # Basic config
    user = 'LocationInfoBot'
    mention = f'u/{user}'

    # Regex selectors
    CITY_REGEX = '.+$'

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
