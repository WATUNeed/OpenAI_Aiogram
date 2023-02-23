import os

import openai

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from ArticleLinkFinder import ArticleLinkFinder, response_request

from MessageCreator import get_message


env = '6115324570:AAFhFRtMRozek0f7Dpq070u1AB627At0ulc'

# dp = Dispatcher(Bot(os.environ.get('Hideway_Crypto_bot')))
# bot = Bot(os.environ.get('Hideway_Crypto_bot'))

bot = Bot(env)

dispatcher = Dispatcher(bot)

openai.api_key = os.environ.get('OpenAI_API')


def get_button_source_url(url: str, message='Ссылка на источник') -> types.InlineKeyboardMarkup:
    button_source_reference = types.InlineKeyboardMarkup(row_width=1)
    button_source_reference.add(types.InlineKeyboardButton(text=message, url=url))
    return button_source_reference


@dispatcher.message_handler()
async def send(message: types.Message):
    await message.answer('Please waiting...')
    age_post, status = await send_post()
    await message.answer(text=f'Response status: {status}\nage_post: {age_post} hours')


async def send_post():
    url_finder = ArticleLinkFinder()
    age_post, img, url, status = await response_request(url_finder)
    message = await get_message(url)
    await bot.send_photo(chat_id='@hidewaycrypto', photo=img, caption=message, reply_markup=get_button_source_url(url=url))
    return age_post, status


executor.start_polling(dispatcher, skip_updates=True)
