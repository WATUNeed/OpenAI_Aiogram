from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ArticleLinkFinder import ArticleLinkFinder, response_request

from MessageCreator import get_message

from sqlite import db_start

from os import environ


bot = Bot(environ.get('Hideway_Crypto_bot'))
dispatcher = Dispatcher(bot)


async def on_startup(_):
    await db_start()


def get_button_source_url(url: str, message='Ссылка на источник') -> types.InlineKeyboardMarkup:
    button_source_reference = types.InlineKeyboardMarkup(row_width=1)
    button_source_reference.add(types.InlineKeyboardButton(text=message, url=url))
    return button_source_reference


@dispatcher.message_handler(commands=['post'])
async def start_scheduler(message: types.Message):
    await message.answer('Post scheduler is started. Interval = 1 hour')
    await send_post_interval()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_post_interval, trigger='interval', hours=1)
    scheduler.start()


async def send_post_interval():
    url_finder = ArticleLinkFinder()
    age_post, img, url, status = await response_request(url_finder)
    message = await get_message(url)
    await bot.send_photo(chat_id='@hidewaycrypto', photo=img, caption=message, reply_markup=get_button_source_url(url=url))


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
