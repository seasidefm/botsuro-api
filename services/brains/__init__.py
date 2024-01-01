from datetime import datetime

import openai

from models.completion import ChatCompletion
from models.memory import Memory
from models.platform import Platform
from repositories.ai import OpenAi
from repositories.memories import Memories
from queries.sanity_urls import from_prompt_blocks
from repositories.sanity import Sanity

SELECTED_MODEL = "gpt-3.5-turbo"


class BotsuroBrains:
    """
    The brains of the bot (almost literally). This is where the magic happens.
    """

    def __init__(self, openai_token: str):
        self.model = SELECTED_MODEL
        self.memories = Memories()
        self.ai = OpenAi()
        self.sanity = Sanity()

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

        data = self.sanity.get_bot_personality(platform)

        return from_prompt_blocks(data[0].aiPrompt)

    def ask(self, platform: Platform, query: str, max_tokens=175) -> ChatCompletion:
        """
        Ask a question to the bot

        :param platform: The platform on which the question is being asked.
        :param query: The question being asked.
        :param max_tokens: The maximum number of tokens for the response. Default is 175.

        :return: The response from the bot.
        """

        try:
            self.memories.save(
                Memory(
                    role="user",
                    content=query,
                    platform=platform,
                    created_at=datetime.now(),
                )
            )
            prompt = self.get_personality(platform=platform)

            completion = self.ai.get_chat_completion(
                prompt,
                query,
                model="premium",
                max_tokens=max_tokens,
                memories=self._get_memories(platform=platform),
            )

            content = completion.choices[0].message.content
            self.memories.save(
                Memory(
                    role="assistant",
                    content=content,
                    platform=platform,
                    created_at=datetime.now(),
                )
            )

            return ChatCompletion(content=content)
        except openai.InternalServerError as e:
            print("CAUGHT ERROR: ", e)
            return ChatCompletion(
                content="I'm sorry, I'm having trouble thinking right now. Can you ask me again in "
                "a few minutes? (OpenAI is probably down)"
            )

    def save_memory(self, memory: Memory):
        """
        Save a memory to the database
        :param memory:
        :return:
        """
        self.memories.save(memory)
