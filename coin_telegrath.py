import logging

from websites import Websites


class CoinTelegrath(Websites):
    __slots__ = ()

    def __init__(self):
        super().__init__(url='https://cointelegraph.com/', headers={
            'Origin': 'http://fiddle.jshell.net',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'http://fiddle.jshell.net/_display/',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }, data={
            'msg1': 'wow',
            'msg2': 'such',
            'msg3': 'data',
        })