import os

import openai

import asyncio

import logging


logger = logging.getLogger('Bot.MessageCreator')

openai.api_key = os.environ.get('OpenAI_API')

prompt = 'Я веду телеграмм канал с новостями о криптовалюте на русском языке. ' \
         'Выдели основные мысли из статьи и кратко запиши их. Каждую мысль выдели в абзац. ' \
         'Не более 10-15 строк. В конце добавь 4 хештега по теме.' \
         'Статья: '


async def get_message(url: str) -> str:
    logger.info('function "get_message" was called')
    try:
        logger.debug('Trying to get a response from OpenAi')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'{prompt}{url}',
            temperature=0.9,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stream=False,
            logprobs=None,
            stop=['You:']
        )
    except openai.error as ex:
        logger.error(str(ex))
        await asyncio.sleep(300)
        response = await get_message(url)

    message = response['choices'][0]['text']
    if message is None:
        logger.error(ex := 'Response from ChatGTP is None')
        raise Exception(ex)
    logger.debug('Spent tokens: %s', response['usage']['total_tokens'])
    return message
