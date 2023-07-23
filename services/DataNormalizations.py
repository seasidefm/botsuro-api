import json

import openai

MODEL: str = "gpt-3.5-turbo"


class DataNormalization:
    """
    API wrapper for connecting to OpenAI's Data Normalization API
    """
    def __init__(self, openai_token: str):
        self.model = MODEL
        self.openai_token = openai_token
        openai.api_key = openai_token

    def health_check(self):
        return True, "OK"

    def normalize(self, prompt: str, data: str):
        """
        Normalize a given string of data
        :param data:
        :param prompt:
        :return:
        """

        if prompt is None:
            prompt = "Normalize the following data:\n\n" + data + "\n\nNormalized data:"

        chat_completion = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=100,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": data}],
        )

        return json.loads(chat_completion.choices[0].message.content)
