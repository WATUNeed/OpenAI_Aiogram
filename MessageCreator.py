import os

import openai


openai.api_key = os.environ.get('OpenAI_API')

prompt = 'Я веду телеграмм канал с новостями о криптовалюте на русском языке. ' \
         'Выдели основные мысли из статьи и кратко запиши их. Каждую мысль выдели в абзац. ' \
         'Не более 10-15 строк. В конце добавь 4 хештега по теме.' \
         'Статья: '


async def get_message(url):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'{prompt}{url}',
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        logprobs=None,
        stop=['You:']
    )
    message = response['choices'][0]['text']
    if message is None:
        raise Exception('Response from ChatGTP is None.')
    print(f"Spent tokens: {response['usage']['total_tokens']}")
    return message
