from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from SiteData import SiteData, get_html_markup, get_article_data

from MessageCreator import get_message

from SQLite import db_start

from os import environ

import logging
import logging.handlers
import logging.config

import json

bot = Bot(environ.get('Hideway_Crypto_bot'))
dispatcher = Dispatcher(bot)
logger = logging.getLogger('Bot')
channel_id = '@hidewaycrypto'


async def on_startup(_) -> None:
    await init_logging()
    await db_start()
    logger.info('Bot was initialized')


async def init_scheduler():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_post_interval, trigger='interval', hours=1)
    scheduler.start()
    logger.debug('scheduler was initialized')


async def init_logging():
    logging.config.dictConfig(get_log_config())
    logger.debug('logger was initialized')


def get_log_config():
    with open('localLogConfig.json', 'r') as config:
        return json.load(config)


def get_button_url(url: str, message='Ссылка на источник') -> types.InlineKeyboardMarkup:
    button_source_reference = types.InlineKeyboardMarkup(row_width=1)
    button_source_reference.add(types.InlineKeyboardButton(text=message, url=url))
    return button_source_reference


@dispatcher.message_handler(commands=['post'])
async def create_post(message: types.Message) -> None:
    logger.info('Call to create a post')
    answer = await message.answer('A post in the making...')
    try:
        await send_post_interval()
    except Exception as e:
        logger.exception(e)
        await answer.edit_text('An error during post creation')
    finally:
        await answer.edit_text('The post was successfully created')


@dispatcher.message_handler(commands=['run_schedule'])
async def start_scheduler(message: types.Message) -> None:
    await init_scheduler()
    await message.answer('Schedule is up and running')


async def send_post_interval() -> None:
    html = await get_html_markup(SiteData())
    logger.info('HTML successfully received')
    img, url = await get_article_data(html)
    logger.info('img and url successfully received')
    message = await get_message(url)
    await bot.send_photo(chat_id=channel_id, photo=img, caption=message, reply_markup=get_button_url(url=url))
    logger.info('The post was successfully created')


if __name__ == '__main__':
    try:
        executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, timeout=120)
    except exceptions.NetworkError as e:
        logger.exception(e)
