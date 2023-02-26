import os

import openai

import asyncio

import logging


openai.api_key = os.environ.get('OpenAI_API')

LOGGER = logging.getLogger('bot.MessageCreator')

PROMPT = ("Create a Russian-language social media post about the article ",
          "do not include lists. "
          "the keyword should be in the first or second sentence. "
          "add a little emoji to the following text to make it easier to read and more engaging. "
          "do not add explanation to your answer. "
          "make the post no more than 250 words. "
          "make it ironic and personal. "
          "add four hashtags at the end on the topic.")


async def get_message(url: str) -> str:
    LOGGER.info('function "get_message" was called')
    try:
        LOGGER.debug('Trying to get a response from OpenAi')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'{PROMPT[0]}{url} {PROMPT[1]}',
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
    except openai.error as ex:
        LOGGER.error(str(ex))
        await asyncio.sleep(300)
        response = await get_message(url)

    message = response['choices'][0]['text']
    if message is None:
        LOGGER.error(ex := 'Response from ChatGTP is None')
        raise Exception(ex)
    LOGGER.debug('Spent tokens: %s', response['usage']['total_tokens'])
    return message
