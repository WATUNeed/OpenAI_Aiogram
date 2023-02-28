import sqlite3

import pytest


TEST_DB_URL = 'test_db.db'


@pytest.fixture(scope='session', autouse=True)
def create_moderate_table():
    db_connection = sqlite3.connect(TEST_DB_URL)
    create_url_table_query = 'CREATE TABLE IF NOT EXISTS post(url TEXT PRIMARY KEY);'
    drop_url_table_query = 'DROP TABLE post;'
    insert_urls_into_post_table_query = """
                INSERT INTO post (url) VALUES
                ('https://cryptoslate.com/coinbase-survey-indicates-20-of-americans-own-crypto/'),
                ('https://cryptoslate.com/over-2b-busd-burnt-in-the-last-seven-days/'),
                ('https://cryptoslate.com/reddit-avatar-nfts-market-cap-exceeds-35-million/'),
                ('https://cryptoslate.com/someone-forked-bitcoin-ordinals-nfts-onto-litecoin-network/'),
                ('https://cryptoslate.com/some-twitter-users-can-now-buy-twitter-coins-via-stripe/');
                """
    db_connection.execute(create_url_table_query)
    db_connection.execute(insert_urls_into_post_table_query)
    db_connection.commit()
    yield
    db_connection.execute(drop_url_table_query)
    db_connection.commit()
