"""
Services related to discogs
"""
import logging
from typing import Optional, List

import requests
import discogs_client

logger = logging.getLogger("botsuro-api")


def release_to_dict(release: discogs_client.Release) -> dict:
    mp_stats = release.marketplace_stats
    return {
        "title": release.title,
        "year": release.year,
        "marketplace_stats": {
            "num_for_sale": mp_stats.num_for_sale,
            "lowest_price": f"{mp_stats.lowest_price.value} {mp_stats.lowest_price.currency}",
        }
    }


def release_has_results(release: discogs_client.Release) -> bool:
    return release.marketplace_stats.num_for_sale is not None and release.marketplace_stats.num_for_sale > 0


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
        self.client = discogs_client.Client(
            user_agent=user_agent, user_token=access_token
        )

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

        logger.info("Discogs status code: %s", res.status_code)

        if res.status_code == 200:
            reason = "OKAY"
        elif res.status_code == 429:
            reason = "Received rate limiting 429"
        else:
            reason = "Discogs services are down"

        return res.status_code == 200, reason

    def album_marketplace_data(self,
                               album: str, artist: str,
                               year: Optional[int]) -> List[dict]:
        """
        Search discogs for albums and artists matching this
        :param artist:
        :param album:
        :param year:

        :return:
        """

        releases = self.client.search(
            f"{artist} {album}",
            type="release",
            per_page=5
        )

        rel_with_listings = filter(lambda release: release_has_results(release), releases)

        return [release_to_dict(release) for release in rel_with_listings]
