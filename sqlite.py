import sqlite3 as sq

import logging


logger = logging.getLogger('bot.sqlite')


async def db_start() -> None:
    global DB, CURSOR

    DB = sq.connect('bot.db')
    CURSOR = DB.cursor()
    CURSOR.execute('CREATE TABLE IF NOT EXISTS post(url TEXT PRIMARY KEY)')
    DB.commit()
    logger.info('database was initialized')


async def url_in_db(url: str) -> bool:
    if not url:
        logger.error(ex := 'url is None.')
        raise Exception(ex)
    post = CURSOR.execute(f"SELECT * FROM post WHERE url == '{url}'").fetchone()
    if not post:
        logger.debug('The url is in the database')
        CURSOR.execute(f"INSERT INTO post VALUES('{url}')")
        DB.commit()
        return False
    else:
        logger.debug('url is not in the database')
        return True
