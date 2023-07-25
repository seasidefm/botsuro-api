from functools import lru_cache

import requests


class SongIdProxy:
    """
    API wrapper for connecting to Song ID
    """
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def health_check(self):
        """
        Check if Song ID API is doing okay
        :return:
        """
        try:
            return requests.get(self.endpoint, timeout=45).status_code == 200, "OK"
        except ConnectionError:
            return False, "Could not connect to Song ID API"

    def get_song_id(self, creator: str):
        """
        Get the song ID for a given creator
        :param creator:
        :return:
        """
        return requests.get(f"{self.endpoint}/identify/{creator}", timeout=90).json()
