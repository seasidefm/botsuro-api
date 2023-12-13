import os
import pprint
from typing import List, Optional
from urllib.parse import urlencode

import dotenv
import requests

from models.sanity.album_menu import AlbumMenuQueryResult, AlbumMenuQueryResponse
from models.sanity_blocks import BotPersonalityResult, QueryResponse
from queries.album_menu import ALBUM_MENUS_QUERY
from queries.bot_personality import BOT_PERSONALITY_QUERY
from repositories.cache import Cache


class Sanity:
    def __init__(self, use_archive_link=False):
        dotenv.load_dotenv()
        if not use_archive_link:
            self.base_url = os.getenv("SANITY_URL")
        else:
            self.base_url = os.getenv("ARCHIVES_SANITY_URL")

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

    def _get_album_menus(self) -> AlbumMenuQueryResponse:
        """
        Get the list of album menus from Sanity
        :return:
        """

        try:
            query = self.encode_query(ALBUM_MENUS_QUERY.format(
                NAME_FILTER="",
            ))
            url = f"{self.base_url}?{query}"
            data = requests.get(url).json()

            return AlbumMenuQueryResponse(**data)

        except KeyError:
            print("KeyError in _get_album_menus")
            return AlbumMenuQueryResponse(
                query="",
                result=[],
                ms=-1
            )

    # Album and Album menus
    def get_album_menus(self) -> AlbumMenuQueryResponse:
        """
        Get the list of album menus from Sanity
        :return:
        """
        return Cache.cached_function(
            self._get_album_menus,
            key_prefix="album_menus",
            # Cache for 20 minutes
            cache_time=20 * 60
        )

    def _get_unique_album_menu(self, menu_slug: str) -> Optional[AlbumMenuQueryResult]:
        """
        Get a specific album menu from Sanity
        :return:
        """

        try:
            query = self.encode_query(ALBUM_MENUS_QUERY.format(
                NAME_FILTER=f'&& menuSlug.current == "{menu_slug}"',
            ))
            url = f"{self.base_url}?{query}"
            data = AlbumMenuQueryResponse(**requests.get(url).json())

            if data.result:
                return data.result[0]

            return None
        except KeyError:
            print("KeyError in _get_unique_album_menu")
            return None

    def get_unique_album_menu(self, menu_slug: str, bypass_cache=False) -> Optional[AlbumMenuQueryResult]:
        """
        Get a specific album menu from Sanity
        :return:
        """

        if bypass_cache:
            return self._get_unique_album_menu(menu_slug)

        return Cache.cached_function(
            self._get_unique_album_menu,
            menu_slug,
            key_prefix="unique_albums",
            # Cache for 20 minutes
            cache_time=20 * 60
        )
