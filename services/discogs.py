"""
Services related to discogs
"""
import logging
import urllib.parse
from typing import Optional

import requests

from models.discogs import DiscogsSearchModel

logger = logging.getLogger("botsuro-api")


class DiscogsApi:
    """
    API wrapper for connecting to Discogs
    """
    base_url: str = "https://api.discogs.com"

    def __init__(self,
                 access_token: str,
                 user_agent="SeasideAPI/2.0 +https://twitch.tv/seasidefm"
                 ):
        self.access_token = access_token
        self.user_agent = user_agent

    def _get_headers(self):
        return {
            "Authorization": f"Discogs token={self.access_token}",
            "User-Agent": self.user_agent
        }

    def health_check(self):
        """
        Check if discogs API is doing okay
        :return:
        """
        res = requests.get(
            headers=self._get_headers(),
            url=f"{self.base_url}/",
            timeout=15
        )

        return res.status_code == 200

    def artist_album_search(self,
                            album: str, artist: str,
                            year: Optional[int], media="album"):
        """
        Search discogs for albums and artists matching this
        :param artist:
        :param album:
        :param year:
        :param media:
        :return:
        """

        url = f"{self.base_url}/database/search?release_title={urllib.parse.quote(album)}" \
              f"&artist={urllib.parse.quote(artist)}" \
              f"{f'&year={year}' if year else ''}&format={media}"

        logger.info(url)

        res = requests.get(
            headers=self._get_headers(),
            url=url,
            timeout=15
        )

        if res.status_code != 200:
            logger.error(res.text)
            raise requests.HTTPError(f"Got code {res.status_code} for album search!")

        return DiscogsSearchModel(**res.json())

    def get_release_marketplace_data(self, release_id: int, currency="USD"):
        """
        Using a discogs release ID, get marketplace information
        :param release_id:
        :param currency:
        :return:
        """

        res = requests.get(
            headers=self._get_headers(),
            url=f"{self.base_url}/marketplace/stats/{release_id}?curr_abbr={currency}",
            timeout=15
        )

        if res.status_code != 200:
            logger.error(res.text)
            raise requests.HTTPError(f"Got code {res.status_code} for marketplace search!")

        return res.json()
