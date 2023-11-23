"""
The main entrypoint for the botsuro api
"""

import json
from logging import getLogger
from logging.config import dictConfig
from typing import Optional, Literal
import fastapi
from fastapi import templating

import queries
from config import LogConfig
from middleware.identity import IdentityMiddleware
from models.faves import FaveSongInput
from models.notes import NewNoteInput
from services import Services

# Config
# ===================

dictConfig(LogConfig().dict())

# Setup
# ===================
logger = getLogger("botsuro-api")
logger.info("Starting botsuro api!")

services = Services()
app = fastapi.FastAPI(docs_url="/docs", redoc_url="/redoc")

templates = templating.Jinja2Templates(directory="templates")

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

    discogs_okay, d_reason = services.discogs_api.health_check()
    song_id_okay, si_reason = services.song_id.health_check()

    return {
        "botsuro": {
            "status": "OK",
            "reason": "No botsuro health check yet"
        },
        "discogs": {
            "status": "OK" if discogs_okay else "DEGRADED",
            "reason": d_reason
        },
        "song_id": {
            "status": "OK" if song_id_okay else "DEGRADED",
            "reason": si_reason
        },
        "database": {
            "status": "OK",
            "reason": "No database health check yet"
        },
    }


# Song ID API Proxy
# ===================
@app.get("/song")
def song_id_proxy(creator: str):
    """
    Get the song ID for a given song
    :param creator:
    :return:
    """

    song_id = services.song_id.get_song_id(creator)
    cached = services.cache.get(f"song_id:{creator}")

    normalized = services.data_norm.normalize(
        queries.SONG_ID_NORMALIZATION, json.dumps(song_id)
    )

    if cached is not None:
        artist, song = normalized.get("artist"), normalized.get("song")
        loaded = json.loads(cached)
        cached_artist, cached_song = loaded.get("artist"), loaded.get("song")

        if artist == cached_artist and song == cached_song:
            return {
                **loaded,
                "changed": False,
            }

    services.cache.set(f"song_id:{creator}", normalized)
    return {
        **normalized,
        "changed": True,
    }


@app.get("/obs/song")
def obs_song_id_proxy(request: fastapi.Request, creator: str, refresh_time: Optional[int] = 10):
    """
    Render the template for the song ID for a given song
    :param request:
    :param creator:
    :param refresh_time:
    :return:
    """

    if cached := services.cache.get(f"song_id:{creator}"):
        loaded = cached
        if loaded.get("error"):
            song_string = "Unknown Song"
        else:
            song_string = f"{loaded.get('artist')} - {loaded.get('song')}"
    else:
        song_string = "Unknown Song"

    return templates.TemplateResponse(
        "song_id.html",
        {
            "request": request,
            "song_string": song_string,
            "refresh_time": refresh_time,
        })


# Fave system v2
# ===================
@app.get("/faves")
def faves_for_user(user: str, level: Optional[str] = None, offset=0, count=10, sort_by="fave_date", sort_order="desc"):
    """
    Retrieves the favorite items for a given user at a specific level.

    :param sort_order:
    :param sort_by:
    :param user: The username of the user.
    :param level: The level of the favorite items.
    :param offset: The starting index from which to retrieve the favorite items. Default is 0.
    :param count: The number of favorite items to retrieve. Default is 10.
    :return: The favorite items for the given user at the specified level.
    """

    return services.faves.get_faves_by_level(user, level, offset, count, sort_by, sort_order)


@app.post("/fave_this")
def fave_this(fave_input: FaveSongInput):
    """
    Marks the current song as a favorite for the given user at the specified level.

    :param fave_input: The input for the favorite item.
    :return: The favorite item that was created.
    """

    fave_status = services.faves.fave_this(fave_input.user, fave_input.level)
    logger.info(f"User {fave_input.user} {fave_input.level}faved with status {fave_status}")

    return fave_status


# Note system
# ===================
@app.post("/notes")
def add_note(note_input: NewNoteInput):
    """
    Marks the current song as a favorite for the given user at the specified level.

    :param note_input: The input for the favorite item.
    :return: The favorite item that was created.
    """

    new_note = services.notes.create_note_for_user(note_input.user, note_input.content)
    logger.info(f"User {note_input.user} created note")

    if new_note:
        return {
            "status": "created",
        }
    else:
        return {
            "status": "error",
            "reason": "unknown",  # TODO: Add reason
        }


@app.get("/notes")
def get_notes(user: str, offset=0, count=10, sort_by="fave_date", sort_order="desc"):
    """
    Retrieves the notes for a given user.

    :param sort_order:
    :param sort_by:
    :param count:
    :param offset:
    :param user: The username of the user.
    :return: The notes for the given user.
    """

    return services.notes.get_notes_for_user(user, offset, count, sort_by, sort_order)


# AI Personas
# ===================
@app.get("/botsuro")
def ai_personas(platform: Literal["twitch", "minecraft", "discord"], query: str):
    """
    Get the AI personas
    :return:
    """

    return services.botsuro.ask(platform.upper(), query, max_tokens=500)


@app.get("/get-completion")
def get_completion(platform: str, query: str, max_tokens: int = 500):
    """
    Get the AI personas
    :return:
    """

    return services.botsuro.ask(platform.upper(), query, max_tokens=max_tokens)


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
