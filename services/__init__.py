"""
The app-level service dependency injector
"""
import os

from dotenv import load_dotenv

from .discogs import DiscogsApi


class Services:
    """
    The seaside Api services in one convenient dependency injection
    """
    def __init__(self):
        load_dotenv()

        if discogs_token := os.getenv("DISCOGS_ACCESS_TOKEN"):
            self.discogs_api = DiscogsApi(discogs_token)
        else:
            raise EnvironmentError("DISCOGS_ACCESS_TOKEN not found in env")
