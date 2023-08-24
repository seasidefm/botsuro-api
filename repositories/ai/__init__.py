import os
from typing import Literal, List

import openai

from models.memory import Memory
from models.platform import Platform


class OpenAi:
    _instance = None
    models = {
        "default": "gpt-3.5-turbo",
        "premium": "gpt-4"
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OpenAi, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        if openai_token := os.getenv("OPENAI_TOKEN"):
            openai.api_key = openai_token
            self.chat_completion = openai.ChatCompletion
        else:
            raise EnvironmentError("OPENAI_TOKEN not found in env")

    def get_chat_completion(self,
                            prompt: str,
                            query: str,
                            model: Literal["default", "premium"] = None,
                            max_tokens=125,
                            memories: List[Memory] = None,
                            ):
        if prompt is None:
            raise ValueError("prompt argument cannot be None!")

        if query is None:
            raise ValueError("query argument cannot be None!")

        if memories is None:
            memories = []

        return self.chat_completion.create(
            model=self.models["default"] if model is None else self.models[model],
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                *[
                    {"role": memory.role, "content": memory.content} for memory in (
                            memories
                    )
                ],
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
