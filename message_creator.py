import os

import openai

import asyncio

import logging

from websites import Websites


class MessageCreator:
    __slots__ = 'prompt'

    LOGGER = logging.getLogger('bot.MessageCreator')

    def __init__(self):
        openai.api_key = os.environ.get('OpenAI_API')
        self.prompt = ("Create a Russian-language social media post about the article ",
                       "do not include lists. "
                       "the keyword should be in the first or second sentence. "
                       "add a little emoji to the following text to make it easier to read and more engaging. "
                       "do not add explanation to your answer. "
                       "make the post no more than 250 words. "
                       "make it ironic and personal. "
                       "add four hashtags at the end on the topic.")

    async def get_message(self, url: str) -> str:
        try:
            response = await self._get_response(url)
        except openai.error as ex:
            self.LOGGER.error(str(ex))
            await asyncio.sleep(timeout := 300)
            response = await self.get_message(url)

        message = response['choices'][0]['text']
        await Websites.on_validate(self, condition=(message is None), e='Response from ChatGTP is None')
        self.LOGGER.debug('Spent tokens: %s', response['usage']['total_tokens'])
        return message

    async def _get_response(self, url: str) -> str:
        return openai.Completion.create(
            model="text-davinci-003",
            prompt=f'{self.prompt[0]}{url} {self.prompt[1]}',
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
