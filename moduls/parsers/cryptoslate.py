from os import environ

import aiohttp

from bs4 import BeautifulSoup

import logging

from moduls.websites import Websites, reconnect


class CryptoSlate(Websites):
    __slots__ = ()

    LOGGER = logging.getLogger('bot.CryptoSlate')

    def __init__(self):
        super().__init__(url='https://cointelegraph.com/',
                         headers=environ.get('cointelegraph_headers'),
                         data=environ.get('cointelegraph_data'))

    async def get_article_data(self) -> (str, str):
        html = await self._get_html_markup()
        soup = BeautifulSoup(html, 'lxml')

        articles = soup.find_all(class_='list-post unlocked')

        await self.on_validate(condition=not articles, e='Posts is None.')
        self.LOGGER.debug('Articles found successfully')

        articles_data = await self._separate_these_articles(articles=articles)

        await self.on_validate(condition=not articles_data, e='The newest article was not found.')
        self.LOGGER.debug('img and url found successfully')

        return await self.find_unique_article(articles_data)

    @reconnect(delay=10, logger=LOGGER)
    async def _get_html_markup(self) -> str:
        self.LOGGER.info('Connecting to the site...')
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url, headers=self.headers, data=self.data) as resp:
                html = await resp.text()
                await session.close()

                assert resp.status == 200, 'Response status error.'
                await self.on_validate(condition=not html, e='HTML is None.')
                self.LOGGER.info('Connection to the site was successful')

                return html

    async def _separate_these_articles(self, articles: list) -> list:
        for index, article in enumerate(articles):
            img = article.find(class_='cover').find('img').get('src')
            url = article.find('a').get('href')
            await self.on_validate(condition=any([not img, not url]), e='Invalid img or url.')
            articles[index] = (img, url)
        return articles
