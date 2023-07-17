from logging import getLogger
from logging.config import dictConfig
from typing import Optional

import fastapi

from config import LogConfig
from middleware.identity import IdentityMiddleware
from models.discogs import DiscogsSearchModel
from services import Services

# Config
# ===================

dictConfig(LogConfig().model_dump())

# Setup
# ===================
logger = getLogger("botsuro-api")
logger.info("Starting botsuro api!")

services = Services()
app = fastapi.FastAPI()

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
    return {
        "discogs": "OK"
                   if services.discogs_api.health_check() else "DEGRADED",
        "database": "OK"
    }


# AI Function callbacks
# ===================
@app.get("/discogs/price")
def discogs_price(album: str, artist: str, year: Optional[int] = None):
    """
    Search discogs for an artist and album, getting the price if applicable
    :return:
    """

    logger.info(f"Received price request for {album}{f' ({year})' if year else ''} by {artist}")

    discogs_search = services.discogs_api.artist_album_search(album, artist, year)

    if not discogs_search.results:
        return {
            "error": f"No listings found for {album}{f' ({year})' if year else ''} by {artist}"
        }

    marketplace_summary = services.discogs_api.get_release_marketplace_data(
        discogs_search.results[0].id
    )

    return marketplace_summary
