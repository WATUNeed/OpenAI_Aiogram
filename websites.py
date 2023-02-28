import logging

from database import DataBase


class Websites:
    __slots__ = 'url', 'headers', 'data'

    LOGGER = logging.getLogger('bot.Websites')
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            Websites._instances[cls] = super(Websites, cls).__new__(cls, *args, **kwargs)
        return Websites._instances[cls]

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.headers = kwargs.get('headers')
        self.data = kwargs.get('data')

    def __iter__(self):
        print(self.__class__._instances)
        return iter([e for e in self.__class__._instances.values() if e.__class__ is not Websites])

    async def on_validate(self, condition: bool, e: str):
        if condition:
            self.LOGGER.error(e)
            raise Exception(e)

    async def find_unique_article(self, articles_data: list) -> (str, str):
        for article_data in articles_data:
            if not await DataBase().url_in_database(url=article_data[1]):
                return article_data[0], article_data[1]
            else:
                self.LOGGER.error(e := 'no unique articles found')
                raise Exception(e)


class CoinTelegrath(Websites):
    __slots__ = ()

    def __init__(self):
        super().__init__(url='https://cointelegraph.com/', headers={
            'Origin': 'http://fiddle.jshell.net',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'http://fiddle.jshell.net/_display/',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }, data={
            'msg1': 'wow',
            'msg2': 'such',
            'msg3': 'data',
        })
