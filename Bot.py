from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from SiteData import CryptoSlate, get_html_markup, get_article_data

from MessageCreator import get_message

from SQLite import db_start

from os import environ

import logging
import logging.config
import logging.handlers

import json


BOT = Bot(environ.get('HidewayPosterBot'))
DP = Dispatcher(BOT)
LOGGER = logging.getLogger('bot')
CHANNEL_ID = '@hidewaycrypto'


async def on_startup(_) -> None:
    await init_logging()
    await db_start()
    LOGGER.info('Bot was initialized')


async def init_scheduler() -> None:
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_post_interval, trigger='interval', hours=1)
    scheduler.start()
    LOGGER.info('scheduler was initialized')


async def init_logging() -> None:
    logging.config.dictConfig(get_log_config())
    LOGGER.debug('logger was initialized')


def get_log_config() -> dict:
    with open('localLogConfig.json', 'r') as config:
        return json.load(config)


async def get_keyboard() -> InlineKeyboardMarkup:
    btn_post = InlineKeyboardButton(text='Create new post ✍', callback_data='post')
    btn_run = InlineKeyboardButton(text='Run the scheduler ⏳', callback_data='run')
    menu = InlineKeyboardMarkup(row_width=2)
    menu.insert(btn_post)
    menu.insert(btn_run)
    return menu


def get_button_url(url: str, message='Ссылка на источник') -> types.InlineKeyboardMarkup:
    button_source_reference = types.InlineKeyboardMarkup(row_width=1)
    button_source_reference.add(types.InlineKeyboardButton(text=message, url=url))
    return button_source_reference


@DP.message_handler(commands=['start', 'Start', 'START'])
async def start_bot(message: types.Message) -> None:
    await BOT.send_message(message.from_user.id, 'Select function: 🛠', reply_markup=await get_keyboard())


@DP.callback_query_handler(text='post')
@DP.message_handler(commands=['post', 'Post', 'POST'])
async def create_post(message: types.Message) -> None:
    LOGGER.info('Call to create a post')
    answer = await message.answer('A post in the making...')
    try:
        await send_post_interval()
    except Exception as e:
        LOGGER.exception(e)
        await answer.edit_text('An error during post creation')
        return
    finally:
        LOGGER.info('The post was successfully created')
        await answer.edit_text('The post was successfully created')


@DP.callback_query_handler(text='run')
@DP.message_handler(commands=['run', 'Run', 'RUN'])
async def run_scheduler(message: types.Message) -> None:
    await init_scheduler()
    await message.answer('Scheduler was successfully created')


@DP.message_handler(commands=['clear', 'Clear', 'CLEAR'])
async def main(message: types.Message):
    return await BOT.send_message(message.from_user.id, 'cleared', reply_markup=types.ReplyKeyboardRemove())


async def send_post_interval() -> None:
    html = await get_html_markup(CryptoSlate())
    LOGGER.info('HTML successfully received')
    img, url = await get_article_data(html)
    LOGGER.info('img and url successfully received')
    message = await get_message(url)
    await BOT.send_photo(chat_id=CHANNEL_ID, photo=img, caption=message, reply_markup=get_button_url(url=url))


if __name__ == '__main__':
    try:
        executor.start_polling(DP, skip_updates=True, on_startup=on_startup, timeout=120)
    except exceptions.NetworkError as e:
        LOGGER.exception(e)
