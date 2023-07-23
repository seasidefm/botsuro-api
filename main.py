from logging import getLogger
from logging.config import dictConfig
from typing import Optional, List

import fastapi

from config import LogConfig
from middleware.identity import IdentityMiddleware
from services import Services

# Config
# ===================

dictConfig(LogConfig().model_dump())

# Setup
# ===================
logger = getLogger("botsuro-api")
logger.info("Starting botsuro api!")

services = Services()
app = fastapi.FastAPI(docs_url="/docs", redoc_url="/redoc")

protected_routes = [
    "/search/discogs"
]

app.add_middleware(IdentityMiddleware, protected_routes=protected_routes)


# Information
# ===================
@app.get("/")
def root_information():
    """
    Simple health check
    :return:
    """
    return {
        "about": "This is the API for SeasideFM's Botsuro Yamashita!",
    }


@app.get("/health")
def health_check():
    """
    Simple health check
    :return:
    """

    discogs_okay, reason = services.discogs_api.health_check()

    return {
        "discogs": {
            "status": "OK"
            if discogs_okay else "DEGRADED",
            "reason": reason
        },
        "database": "OK",
    }


# Song ID API Proxy
# ===================
@app.get("/song")
def song_id_proxy(song_id: str):
    """
    Get the song ID for a given song
    :param song_id:
    :return:
    """

    return {"test": "test"}

    # return services.song_id.get_song_id(song_id)


# Fave system v2
# ===================
@app.get("/faves")
def faves_for_user(user: str):
    """
    Get the faves for a given user
    :param user:
    :return:
    """

    return services.faves.get_faves_for_user(user)


@app.get("/superfaves")
def superfaves_for_user(user: str):
    """
    Get the superfaves for a given user
    :param user:
    :return:
    """

    return services.faves.get_superfaves_for_user(user)


# AI Function callbacks
# ===================
@app.get("/discogs/price")
def discogs_price(album: str, artist: str, year: Optional[int] = None):
    """
    Search discogs for an artist and album, getting the price if applicable
    :return:
    """

    search_results = services.discogs_api.album_marketplace_data(
        album, artist, year
    )

    return {"data": search_results}


@app.get("/weather")
def weather_for_lat_long(latitude: float, longitude: float, options: str):
    """
    Attempt to get the weather for given coordinates
    :return:
    """

    return {"data": services.weather.get_weather_for_coords(latitude, longitude, options.split(","))}
