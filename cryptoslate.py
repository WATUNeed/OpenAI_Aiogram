import aiohttp

from bs4 import BeautifulSoup

import logging

from websites import Websites


class CryptoSlate(Websites):
    __slots__ = ()

    LOGGER = logging.getLogger('bot.CryptoSlate')

    def __init__(self):
        super().__init__(url='https://cryptoslate.com/top-news/', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://cryptoslate.com/'
                       'top-news?__cf_chl_tk=XCOyl8L8vYfGil11Kox4cAr8Jkq.BT_uSm5YApRObzg-1677080825-0-gaNycGzNB9A',
            'Origin': 'https://cryptoslate.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }, data={
            'md': '0GX98Fe2eutWqvmFE7yR05kotsBB7FNPWPDCZTvocVQ-1677080825-0-ATJMywi8h-IYkG2EiX0aqkgZC4H1GLilde0599K1W8'
                  'KnZiC9NSVAl-OCNXdtIlQr5O_yzllg5dIg1asGnyXjWTTqbK0wKlI8KNluouTzR1RyomjrcvabWylYlkcxOPSbzibLojoruDx21'
                  'uBZhNIlpFuyDSKAY2jYG9GCLx6oZ5TluUlZHsOCKnopFT5jVBu_zaELHKHmq2ouSML1-ZkNtjLnpoE4IqcZ6TvxKEryUxhiEEfb'
                  'm62IZiAC-jqYbvT-7mwWIYKaeLSKBgWmE9IMD3j2KlLD0GP4kmUfwssnY3Ha_SLDbLb4nBR8zRfzS5ulol7WshPLGCD0oEdYJb8'
                  'nWltpYNDL3qevMS-74rYqrpvlGzjA9GdkE7LQZ332_EYBm1wRKN8vdkapglLX22Pu73RAD2STpQPzgdSWG10QWB-Ai7XY-x-7ic'
                  'QiYMcSMEYuy1W6xiNJHkOei05Gj6NvZZ3buRSj0rFGJ--A7D9sKUoY8TWy7YoKTloeRh7I9DSKtIBSb6d-3o4Kagow-sk_XCHB_'
                  '9esExcuOUabyHiUMcRAj9U3SnZwcTmMug0UdeoC4a5KvYgJfKgbzmuk56d8wXpX8vbwcOcDQuFFYbJK4pZ5ogdVfInbHcByCFoG'
                  '5wnwb4fECl9en6KgRnhTNpaHwb8-CoumXsD9TXmqpiGljF-3b7Z3YqHOr-WLZnt98bO85_Q61zp7ZWXJRir7bYKM9p2mcJcAfyb'
                  '1xkZgzsPEw7iBCaYFhuDB983btmxDszaiciFupbWyOyR3SvhXfnKVl5HII4QmSxtcdraf6fNfFLqgYrt1RqnHpJ4W0zuaXibjbU'
                  '_QbW4VmapU7u8lBHrjykmuAoEkeN2WukVOv4xb8RmV1whK_QHjN5601bYmc8ryOQZATFQcs9c88NHe9AU8B6GskpOoH8TJNwD5V'
                  'fYOCNcoK7LfYTH92jSq2HHWmW7Fw_6GnYiMpUF7ImOlBvICBxUtTk25Qi0UEagZ1iiZ4pG2fiOk7p9lQkT4gsu1TAJLZPO5pUcv'
                  '8FL8U1tFQe2nZ6KogH_Rdkmt_8nvvJljoSFMP9y0_i62g9a3Z9SSWwELbLci6JfAPPp-Y98lFeBBvTSlQCLb9579vW-KO0MXaTt'
                  'w9EB-bl1qMAFuguKYKnV0vYLmbXvG1JRtWGkm3fmX3WAie-oJKQ46X3-pwhvj2YuVGACsWPvruDCCkDc8Jzs2vU9_q_jS-Rppa2'
                  'yy0XJWnlV-BGEL7QNCHuBsKZRFGvLi92BTus1zTCcBlhXv1r2oW_E3yWI-Dio_OgvPsZRdeyrITQyfPEa65ZUmf77TWrOrp9ZFj'
                  '8xm5VZs_C7UIoR-r9JUW6rJSrre_PokaCUc1eIvQD_w1HoScpLuNGYfnIxEtr4-gc1XnJfbevD9tdwPDJLCVYOHiLisbHaHpqUH'
                  '1zmUQxkcuaelCQe4gRTOvsHRna9vzcDHlMAMQaKgqDulK5BR2l7FSB2BG4OHEezrLkoqj70y2XO_9-jLdOFl7jM3FsB7HOkEIB3'
                  '2E-S_NJ4r17oO2yEnax6uYY1YX9KWHap-WdRokbf141SbCi-e_eF7U2Hp_hXlbLiP2wumFffiAstaYuAyBZknJh4i3yFRNOZwiA'
                  '9OsraiKsjLsqeWbTSR_aDBjhUxokbWj7VS-FBY5bvRlxM2f7_3Tb1MOByzLkcDhdVG0AdH64J9lnfI2WnDMh5DK2LMRqskKx3jp'
                  'HEVo60IbhevIud75UD-SGs2ZNedZJVon2ZVh5KxDAgioDK2k8b03cYojhh-6RhtbBv1qRXR6SyXaonC86O7j3VJcL4klPULMEj1'
                  'Vw4QbE4N_PcuS9i1LSjJVKgAYANRe8OU40EFRJ4paxMpIRfpdiZ53FVTOVqtH0RHtFNckabe2gFYr2_LohLfxAGZdPXNXm_UhHm'
                  '1zqZcmT5zLOYmSpDlodE',
            'sh': '57a1a881687ad0c0952b8335b008affe',
            'aw': 'umUiAPGccRss-16-79d8dbb71d1c2074',
        })

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
