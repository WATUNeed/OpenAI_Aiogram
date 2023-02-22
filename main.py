import os

import openai

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from ArticleLinkFinder import ArticleLinkFinder

env = '6115324570:AAFhFRtMRozek0f7Dpq070u1AB627At0ulc'

# dp = Dispatcher(Bot(os.environ.get('Hideway_Crypto_bot')))
# bot = Bot(os.environ.get('Hideway_Crypto_bot'))

ArticleLinkFinder()

bot = Bot(env)

dispatcher = Dispatcher(bot)

openai.api_key = os.environ.get('OpenAI_API')


def get_button_source_reference(url: str, message='Ссылка на источник') -> types.InlineKeyboardMarkup:
    button_source_reference = types.InlineKeyboardMarkup(row_width=1)
    button_source_reference.add(types.InlineKeyboardButton(text=message, url=url))
    return button_source_reference


@dispatcher.message_handler()
async def send(message: types.Message):
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=message.text,
    #     temperature=0.9,
    #     max_tokens=1000,
    #     top_p=1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.6,
    #     stop=["You:"]
    # )
    # await message.answer(response['choices'][0]['text'])
    #answer = 'Популярность залогов на NFT-токенах продолжает расти, так как в январе было заимствовано более 18 тысяч ETH через этот механизм.\nЦена NFT-токенов и ETH непредсказуема, что может привести к риску не выплаты займа, если цена токена снизится и его стоимости не хватит, чтобы погасить займ.\nОсновные хештеги: #NFT, #ETH, #криптовалюта, #займ, #криптозалог.'
    # await message.answer(answer)

    answer = 'Self-hosted wallet ban avoided in new draft of EU’s anti-money laundering bill.'
    await bot.send_message(chat_id='@hidewaycrypto', text=answer, reply_markup=get_button_source_reference(url='https://www.theblock.co/post/213380/self-hosted-wallet-ban-avoided-in-new-draft-of-eus-anti-money-laundering-bill'),
                           disable_web_page_preview=True)

executor.start_polling(dispatcher, skip_updates=True)
