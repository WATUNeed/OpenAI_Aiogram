# -*- coding: utf-8 -*-
import sys

import pytest

from websites import CryptoSlate, get_html_markup

import asyncio

import platform


@pytest.mark.parametrize('expect_response', [b'<!DOCTYPE html><html lang="en-US"><head> <script async src=', ])
def test_correct_cases(expect_response):
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(get_html_markup(CryptoSlate()))
    assert expect_response == result.encode(sys.stdout.encoding, errors='replace')[:59]
