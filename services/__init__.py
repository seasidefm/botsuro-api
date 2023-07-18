"""
The app-level service dependency injector
"""
import os

from dotenv import load_dotenv

from .OpenWeather import OpenWeatherApi
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

        if owm_token := os.getenv("OPEN_WEATHER_MAP_TOKEN"):
            self.weather = OpenWeatherApi(owm_token)
        else:
            raise EnvironmentError("OPEN_WEATHER_MAP_TOKEN not found in env")
