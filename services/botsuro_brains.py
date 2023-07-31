import pprint
from datetime import datetime
from typing import Literal, Type

import openai
import requests

from .Memory import Memories, Memory
from prompts.sanity_urls import MINECRAFT_PERSONALITY, from_prompt_blocks

SELECTED_MODEL = "gpt-3.5-turbo"

Platform = Type[Literal["TWITCH", "DISCORD", "MINECRAFT"]]


class BotsuroBrains:
    """
    The brains of the bot (almost literally). This is where the magic happens.
    """

    def __init__(self, openai_token: str):
        self.model = SELECTED_MODEL
        self.memories = Memories()
        openai.api_key = openai_token

    def _get_memories(self, platform=Platform):
        """
        Get the last N memories
        :return:
        """
        memories = self.memories.get_memories(platform, 10)

        return memories

    # TODO: Make this cache work
    # @cached(namespace="personality", arg_key="platform", cache_time=10 * 60)
    def get_personality(self, platform: Platform) -> str:
        """
        Fetches the personality associated with the given platform.

        :param platform: The platform for which the personality needs to be fetched.
                         Possible values: ["discord", "twitch", "minecraft"]
        :type platform: Literal["discord", "twitch", "minecraft"]

        :return: None
        """
        data = requests.get(MINECRAFT_PERSONALITY).json()

        return from_prompt_blocks(data.get('result')[0].get('aiPrompt'))

    def ask(self, prompt: str, platform: Platform, query: str, max_tokens=175):
        """
        Ask a question to the bot
        :param query:
        :param prompt:
        :param platform:

        :return:
        """
        self.memories.save(Memory(role="user", content=query, platform=platform, created_at=datetime.now()))

        completion = openai.ChatCompletion.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                *[
                    {"role": memory.role, "content": memory.content} for memory in (
                            self._get_memories(platform=platform) or []
                    )
                ],
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        content = completion.choices[0]["message"]["content"]
        self.memories.save(Memory(role="assistant", content=content, platform=platform, created_at=datetime.now()))

        return content

    def save_memory(self, memory: Memory):
        """
        Save a memory to the database
        :param memory:
        :return:
        """
        self.memories.save(memory)
