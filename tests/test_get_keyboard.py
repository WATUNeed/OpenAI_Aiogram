# -*- coding: utf-8 -*-
from __init__ import get_keyboard

import asyncio

import platform


def test_correct_cases():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(get_keyboard()).values.keys()
    assert "dict_keys(['inline_keyboard'])" == str(result)
