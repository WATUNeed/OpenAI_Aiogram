import pytest

from moduls.database import DataBase

from conftest import TestDataBase

import asyncio


@pytest.mark.parametrize('url', ['https://cryptoslate.com/binaryx-token-surge-over-9000-following-bnx-split/'])
def test_standard_cases(url: str):
    testdb = TestDataBase()
    asyncio.run(DataBase._insert_url(testdb, url))
    assert (url,) == asyncio.run(DataBase._select_url(testdb, url))
