import os
from typing import List
from urllib.parse import urlencode

import dotenv
import requests

from models.sanity import BotPersonalityResult, QueryResponse
from queries.bot_personality import BOT_PERSONALITY_QUERY
from repositories.cache import Cache


class Sanity:
    def __init__(self):
        dotenv.load_dotenv()
        self.base_url = os.getenv("SANITY_URL")

    def encode_query(self, query: str) -> str:
        """
        Encode the query for Sanity
        :param query:
        :return:
        """
        return urlencode({"query": query})

    def _get_bot_personality(self, platform: str) -> List[BotPersonalityResult]:
        """
        Get the list of bot personalities from Sanity
        :return:
        """

        try:
            query = self.encode_query(BOT_PERSONALITY_QUERY.format(PLATFORM=platform.lower()))
            url = f"{self.base_url}?{query}"
            data = requests.get(url).json()

            return QueryResponse(**data).result
        except KeyError:
            print("KeyError? what caused this?")
            return []

    def get_bot_personality(self, platform: str) -> List[BotPersonalityResult]:
        """
        Get the list of bot personalities from Sanity
        :return:
        """

        return Cache.cached_function(
            self._get_bot_personality,
            platform,
            key_prefix="bot_personality",
            # Cache for 20 minutes
            cache_time=20 * 60
        )
