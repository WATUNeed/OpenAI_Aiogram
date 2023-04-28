from os import environ

from moduls.websites import Websites


class CoinTelegrath(Websites):
    __slots__ = ()

    def __init__(self):
        super().__init__(url='https://cointelegraph.com/',
                         headers=environ.get('cointelegraph_headers'),
                         data=environ.get('cointelegraph_data'))