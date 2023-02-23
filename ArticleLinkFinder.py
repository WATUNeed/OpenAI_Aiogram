import aiohttp

from bs4 import BeautifulSoup

from sqlite import find_post


async def get_url(src: str, status: int):
    soup = BeautifulSoup(src, 'lxml')

    posts = soup.find_all(class_='list-post unlocked')
    if not posts:
        raise Exception(f'posts is None.')
    posts_new = list()

    for post in posts:
        age = post.find(class_='read').text.split()
        if age[1] == 'hours':
            age_post = int(age[0])
            img = post.find(class_='cover').find('img').get('src')
            url = post.find('a').get('href')
            if any([not age_post, not img, not url]):
                raise Exception('Invalid age_post, img or url')
            posts_new.append((age_post, img, url))
    for post in posts_new:
        if not await find_post(url=post[2]):
            return post[0], post[1], post[2], status


async def response_request(url_finder):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url_finder.url, headers=url_finder.headers, data=url_finder.data) as resp:
            src = await resp.text()
            await session.close()
            if resp.status != 200:
                raise Exception(f'Response status error. {resp.status}')
            if not src:
                raise Exception(f'src is None.')
            return await get_url(src, resp.status)


class ArticleLinkFinder:
    __slots__ = 'headers', 'data', 'url'

    def __init__(self):
        self.url = 'https://cryptoslate.com/top-news'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://cryptoslate.com/top-news?__cf_chl_tk=XCOyl8L8vYfGil11Kox4cAr8Jkq.BT_uSm5YApRObzg-1677080825-0-gaNycGzNB9A',
            'Origin': 'https://cryptoslate.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        self.data = {
            'md': '0GX98Fe2eutWqvmFE7yR05kotsBB7FNPWPDCZTvocVQ-1677080825-0-ATJMywi8h-IYkG2EiX0aqkgZC4H1GLilde0599K1W8KnZiC9NSVAl-OCNXdtIlQr5O_yzllg5dIg1asGnyXjWTTqbK0wKlI8KNluouTzR1RyomjrcvabWylYlkcxOPSbzibLojoruDx21uBZhNIlpFuyDSKAY2jYG9GCLx6oZ5TluUlZHsOCKnopFT5jVBu_zaELHKHmq2ouSML1-ZkNtjLnpoE4IqcZ6TvxKEryUxhiEEfbm62IZiAC-jqYbvT-7mwWIYKaeLSKBgWmE9IMD3j2KlLD0GP4kmUfwssnY3Ha_SLDbLb4nBR8zRfzS5ulol7WshPLGCD0oEdYJb8nWltpYNDL3qevMS-74rYqrpvlGzjA9GdkE7LQZ332_EYBm1wRKN8vdkapglLX22Pu73RAD2STpQPzgdSWG10QWB-Ai7XY-x-7icQiYMcSMEYuy1W6xiNJHkOei05Gj6NvZZ3buRSj0rFGJ--A7D9sKUoY8TWy7YoKTloeRh7I9DSKtIBSb6d-3o4Kagow-sk_XCHB_9esExcuOUabyHiUMcRAj9U3SnZwcTmMug0UdeoC4a5KvYgJfKgbzmuk56d8wXpX8vbwcOcDQuFFYbJK4pZ5ogdVfInbHcByCFoG5wnwb4fECl9en6KgRnhTNpaHwb8-CoumXsD9TXmqpiGljF-3b7Z3YqHOr-WLZnt98bO85_Q61zp7ZWXJRir7bYKM9p2mcJcAfyb1xkZgzsPEw7iBCaYFhuDB983btmxDszaiciFupbWyOyR3SvhXfnKVl5HII4QmSxtcdraf6fNfFLqgYrt1RqnHpJ4W0zuaXibjbU_QbW4VmapU7u8lBHrjykmuAoEkeN2WukVOv4xb8RmV1whK_QHjN5601bYmc8ryOQZATFQcs9c88NHe9AU8B6GskpOoH8TJNwD5VfYOCNcoK7LfYTH92jSq2HHWmW7Fw_6GnYiMpUF7ImOlBvICBxUtTk25Qi0UEagZ1iiZ4pG2fiOk7p9lQkT4gsu1TAJLZPO5pUcv8FL8U1tFQe2nZ6KogH_Rdkmt_8nvvJljoSFMP9y0_i62g9a3Z9SSWwELbLci6JfAPPp-Y98lFeBBvTSlQCLb9579vW-KO0MXaTtw9EB-bl1qMAFuguKYKnV0vYLmbXvG1JRtWGkm3fmX3WAie-oJKQ46X3-pwhvj2YuVGACsWPvruDCCkDc8Jzs2vU9_q_jS-Rppa2yy0XJWnlV-BGEL7QNCHuBsKZRFGvLi92BTus1zTCcBlhXv1r2oW_E3yWI-Dio_OgvPsZRdeyrITQyfPEa65ZUmf77TWrOrp9ZFj8xm5VZs_C7UIoR-r9JUW6rJSrre_PokaCUc1eIvQD_w1HoScpLuNGYfnIxEtr4-gc1XnJfbevD9tdwPDJLCVYOHiLisbHaHpqUH1zmUQxkcuaelCQe4gRTOvsHRna9vzcDHlMAMQaKgqDulK5BR2l7FSB2BG4OHEezrLkoqj70y2XO_9-jLdOFl7jM3FsB7HOkEIB32E-S_NJ4r17oO2yEnax6uYY1YX9KWHap-WdRokbf141SbCi-e_eF7U2Hp_hXlbLiP2wumFffiAstaYuAyBZknJh4i3yFRNOZwiA9OsraiKsjLsqeWbTSR_aDBjhUxokbWj7VS-FBY5bvRlxM2f7_3Tb1MOByzLkcDhdVG0AdH64J9lnfI2WnDMh5DK2LMRqskKx3jpHEVo60IbhevIud75UD-SGs2ZNedZJVon2ZVh5KxDAgioDK2k8b03cYojhh-6RhtbBv1qRXR6SyXaonC86O7j3VJcL4klPULMEj1Vw4QbE4N_PcuS9i1LSjJVKgAYANRe8OU40EFRJ4paxMpIRfpdiZ53FVTOVqtH0RHtFNckabe2gFYr2_LohLfxAGZdPXNXm_UhHm1zqZcmT5zLOYmSpDlodE',
            'sh': '57a1a881687ad0c0952b8335b008affe',
            'aw': 'umUiAPGccRss-16-79d8dbb71d1c2074',
        }
