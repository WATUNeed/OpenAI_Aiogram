import pytest

from database import DataBase

import asyncio

import sqlite3


TEST_DB_URL = 'test_db.db'


class TestDataBase:
    __slots__ = 'cursor'

    def __init__(self):
        database = sqlite3.connect(TEST_DB_URL)
        self.cursor = database.cursor()


@pytest.mark.parametrize('url, expect', [
    ('https://cryptoslate.com/coinbase-survey-indicates-20-of-americans-own-crypto/',
     ('https://cryptoslate.com/coinbase-survey-indicates-20-of-americans-own-crypto/',)),
    ('https://cryptoslate.com/over-2b-busd-burnt-in-the-last-seven-days/',
     ('https://cryptoslate.com/over-2b-busd-burnt-in-the-last-seven-days/',)),
    ('https://cryptoslate.com/reddit-avatar-nfts-market-cap-exceeds-35-million/',
     ('https://cryptoslate.com/reddit-avatar-nfts-market-cap-exceeds-35-million/',)),
    ('https://cryptoslate.com/someone-forked-bitcoin-ordinals-nfts-onto-litecoin-network/',
     ('https://cryptoslate.com/someone-forked-bitcoin-ordinals-nfts-onto-litecoin-network/',)),
    ('https://cryptoslate.com/some-twitter-users-can-now-buy-twitter-coins-via-stripe/',
     ('https://cryptoslate.com/some-twitter-users-can-now-buy-twitter-coins-via-stripe/',)),
    ('error', None), (404, None)
])
def test_standard_cases(url: str, expect: bool):
    assert (expect == asyncio.run(DataBase._select_url(TestDataBase(), url)))
