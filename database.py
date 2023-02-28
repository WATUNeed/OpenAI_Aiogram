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
        create_post_table_query = 'CREATE TABLE IF NOT EXISTS post(url TEXT PRIMARY KEY)'
        self.cursor.execute(create_post_table_query)
        self.database.commit()

    async def url_in_database(self, url: str) -> bool:
        if not self._select_url(url):
            self.LOGGER.debug('The url is in the database')
            insert_url_into_post_table_query = f"INSERT INTO post VALUES('{url}')"
            self.cursor.execute(insert_url_into_post_table_query)
            self.database.commit()
            return False
        else:
            self.LOGGER.debug('url is in the database')
            return True

    async def _select_url(self, url: str) -> set:
        select_url_from_post_query = f"SELECT * FROM post WHERE url == '{url}'"
        return self.cursor.execute(select_url_from_post_query).fetchone()
