"""
The app-level service dependency injector
"""
import os

from dotenv import load_dotenv

from repositories.cache import Cache
from .AiChat import AiChat
from .DataNormalizations import DataNormalization
from .FaveSystem import FaveSystem
from .NoteSystem import NoteSystem
from .SongHistory import SongHistory
from .SongIdProxy import SongIdProxy
from .discogs import DiscogsApi
from .brains import BotsuroBrains
from .menus import AlbumMenus
from .weather import WeatherService


class Services:
    """
    The seaside Api services in one convenient dependency injection
    """
    def __init__(self):
        # Load the .env file HERE so the service initializations can
        # happen as needed below
        load_dotenv()

        # Services that don't require any special setup
        # =============================================
        # self.history = SongHistory(database["main"])
        self.faves = FaveSystem()
        self.weather = WeatherService()
        self.notes = NoteSystem()
        self.ai_chat = AiChat()
        self.album_menus = AlbumMenus()

        # Services that require a special token or setup
        # =============================================
        if cache_uri := os.getenv("REDIS_URL"):
            self.cache = Cache(cache_uri)
        else:
            raise EnvironmentError("REDIS_URL not found in env")

        if discogs_token := os.getenv("DISCOGS_ACCESS_TOKEN"):
            self.discogs_api = DiscogsApi(discogs_token)
        else:
            raise EnvironmentError("DISCOGS_ACCESS_TOKEN not found in env")

        if song_id_token := os.getenv("SONG_ID_URL"):
            self.song_id = SongIdProxy(song_id_token)
        else:
            raise EnvironmentError("SONG_ID_URL not found in env")

        if openai_token := os.getenv("OPENAI_TOKEN"):
            self.data_norm = DataNormalization(openai_token)
            self.botsuro = BotsuroBrains(openai_token)
        else:
            raise EnvironmentError("OPENAI_TOKEN not found in env")
