import pytest

from moduls.websites import Websites

import asyncio


@pytest.mark.parametrize('condition, e', [(True, 'Exception error!'), (True, 1)])
def test_standard_cases(condition: bool, e: str):
    with pytest.raises(Exception):
        asyncio.run(Websites().on_validate(condition, e))


@pytest.mark.parametrize('condition, e', [(False, 'Exception error!')])
def test_nostandard_cases(condition: bool, e: str):
    asyncio.run(Websites().on_validate(condition, e))
