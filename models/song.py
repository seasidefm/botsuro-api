from datetime import datetime
from typing import Optional

from pydantic import Field


class StoredSong:
    _id: Optional[str]
    artist: str
    song: str
    album: Optional[str]
    url: Optional[str]
    last_played: datetime = Field(default_factory=datetime.now)
    first_recorded: datetime = Field(default_factory=datetime.now)
