import sqlite3 as sq


async def db_start():
    global db, cursor

    db = sq.connect('bot.db')
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS post(url TEXT PRIMARY KEY)')
    db.commit()


async def find_post(url: str) -> bool:
    if not url:
        raise Exception('url is None.')
    post = cursor.execute(f"SELECT * FROM post WHERE url == '{url}'").fetchone()
    if not post:
        cursor.execute(f"INSERT INTO post VALUES('{url}')")
        db.commit()
        return False
    else:
        return True
