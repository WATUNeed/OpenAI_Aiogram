import os
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

dp = Dispatcher(Bot(os.environ.get('Hideway_Crypto_bot')))
#dp = Dispatcher(Bot('5706198981:AAFTTMonKsarNEHfmYqbuV6fGiJTe0luGTs'))
openai.api_key = os.environ.get('OpenAI_API')

@dp.message_handler()
async def send(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    await message.answer(response['choices'][0]['text'])

executor.start_polling(dp, skip_updates=True)
