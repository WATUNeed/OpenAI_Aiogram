import sqlite3 as sq

import logging


class DataBase:
    __slots__ = 'database', 'cursor'

    LOGGER = logging.getLogger('bot.sqlite')
    _instances = {}

    def __new__(cls):
        if cls not in DataBase._instances:
            DataBase._instances[cls] = super(DataBase, cls).__new__(cls)
        return DataBase._instances[cls]

    def __init__(self):
        self.database = sq.connect('database.db')
        self.cursor = self.database.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS post(url TEXT PRIMARY KEY)')
        self.database.commit()

    async def url_in_database(self, url: str):
        if not self._select_url(url):
            self.LOGGER.debug('The url is in the database')
            self.cursor.execute(f"INSERT INTO post VALUES('{url}')")
            self.database.commit()
            return False
        else:
            self.LOGGER.debug('url is in the database')
            return True

    async def _select_url(self, url: str) -> str:
        return self.cursor.execute(f"SELECT * FROM post WHERE url == '{url}'").fetchone()
