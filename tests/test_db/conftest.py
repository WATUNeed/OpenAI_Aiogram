import sqlite3

import pytest


TEST_DB_URL = 'test_db.db'


@pytest.fixture(scope='session', autouse=True)
def create_moderate_table():
    db_connection = sqlite3.connect(TEST_DB_URL)
    create_url_table_query = 'CREATE TABLE IF NOT EXISTS post(url TEXT PRIMARY KEY)'
    drop_url_table_query = 'DROP TABLE url'
    db_connection.execute(create_url_table_query)
    db_connection.commit()
    yield
    db_connection.execute(drop_url_table_query)
    db_connection.commit()
