from datetime import datetime
from typing import Literal, Type

import openai
import requests

from models.memory import Memory
from models.platform import Platform, PlatformEnum
from repositories.ai import OpenAi
from repositories.memories import Memories
from prompts.sanity_urls import MINECRAFT_PERSONALITY, from_prompt_blocks

SELECTED_MODEL = "gpt-3.5-turbo"


class BotsuroBrains:
    """
    The brains of the bot (almost literally). This is where the magic happens.
    """

    personality_queries = {
        PlatformEnum.MINECRAFT: MINECRAFT_PERSONALITY,
        PlatformEnum.TWITCH: "",
        PlatformEnum.DISCORD: ""
    }

    def __init__(self, openai_token: str):
        self.model = SELECTED_MODEL
        self.memories = Memories()
        self.ai = OpenAi()

    def _get_memories(self, platform=Platform):
        """
        Get the last N memories
        :return:
        """
        memories = self.memories.get_memories(platform, 10)

        return memories

    def get_personality(self, platform: Platform) -> str:
        """
        Fetches the personality associated with the given platform.

        :param platform: The platform for which the personality needs to be fetched.
                         Possible values: ["discord", "twitch", "minecraft"]
        :type platform: Literal["discord", "twitch", "minecraft"]

        :return: None
        """
        # TODO: Move this to a Sanity repository
        query: str = self.personality_queries[platform]
        data = requests.get(query).json()

        return from_prompt_blocks(data.get('result')[0].get('aiPrompt'))

    def ask(self, platform: Platform, query: str, max_tokens=175):
        """
        Ask a question to the bot

        :param platform: The platform on which the question is being asked.
        :param query: The question being asked.
        :param max_tokens: The maximum number of tokens for the response. Default is 175.

        :return: The response from the bot.
        """
        self.memories.save(Memory(role="user", content=query, platform=platform, created_at=datetime.now()))
        prompt = self.get_personality(platform=platform)

        completion = self.ai.get_chat_completion(
            prompt,
            query,
            model="premium",
            max_tokens=max_tokens,
            memories=self._get_memories(platform=platform)
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