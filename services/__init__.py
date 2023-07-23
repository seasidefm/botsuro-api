"""
The app-level service dependency injector
"""
import os

from dotenv import load_dotenv
from pymongo import MongoClient

from .DataNormalizations import DataNormalization
from .FaveSystem import FaveSystem
from .OpenWeather import OpenWeatherApi
from .SongIdProxy import SongIdProxy
from .discogs import DiscogsApi


class Services:
    """
    The seaside Api services in one convenient dependency injection
    """
    def __init__(self):
        load_dotenv()

        if mongo_uri := os.getenv("DATABASE_URL"):
            database = MongoClient(mongo_uri)
        else:
            raise EnvironmentError("DATABASE_URL not found in env")

        # Services that don't require any special setup
        # =============================================
        self.faves = FaveSystem(database["main"])

        # Services that require a special token or setup
        # =============================================
        if discogs_token := os.getenv("DISCOGS_ACCESS_TOKEN"):
            self.discogs_api = DiscogsApi(discogs_token)
        else:
            raise EnvironmentError("DISCOGS_ACCESS_TOKEN not found in env")

        if owm_token := os.getenv("OPEN_WEATHER_MAP_TOKEN"):
            self.weather = OpenWeatherApi(owm_token)
        else:
            raise EnvironmentError("OPEN_WEATHER_MAP_TOKEN not found in env")

        if song_id_token := os.getenv("SONG_ID_URL"):
            self.song_id = SongIdProxy(song_id_token)
        else:
            raise EnvironmentError("SONG_ID_URL not found in env")

        if openai_token := os.getenv("OPENAI_TOKEN"):
            self.data_norm = DataNormalization(openai_token)
        else:
            raise EnvironmentError("OPENAI_TOKEN not found in env")

