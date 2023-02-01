import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")


def get_message(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    return response['choices'][0]['text']
