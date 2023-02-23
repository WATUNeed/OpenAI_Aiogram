import os

import openai


openai.api_key = os.environ.get('OpenAI_API')

prompt = 'Я веду телеграмм канал с новостями о криптовалюте на русском языке.\n' \
         'Выдели основные тезисы из статьи и кратко запиши их простейшим языком по шаблону:\n' \
         '"Не менее двух тезисов на русском языке, каждый тезис отдели абзацем, ' \
         'в конце поста добавь абзац с основными хештеги по теме."\n' \
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
        stop=["You:"]
    )
    return response['choices'][0]['text']
