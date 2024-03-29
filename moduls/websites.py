import logging

from moduls.database import DataBase


def reconnect(delay: int, logger: logging):
    def outer(func):
        def inner(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    print('w')
                    logger.error(err)
                    continue
        return inner
    return outer


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
        return iter([e for e in self.__class__._instances.values() if e.__class__ is not Websites])

    async def on_validate(self, condition: bool, e: str) -> None:
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
