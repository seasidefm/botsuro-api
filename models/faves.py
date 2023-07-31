from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field

FaveLevel = Optional[Literal["super", "ultra", "hyper"]]


class FaveSong(BaseModel):
    """
    Represents a favorite song.

    Attributes:
        user (str): The username of the user who has this favorite song.
        level (FaveLevel): The level of favoritism given to this song.
        fave_date (datetime): The date and time when the song was marked as a favorite.

    """
    user: str
    level: FaveLevel
    fave_date: datetime = Field(default_factory=datetime.now)
    song_id: str
