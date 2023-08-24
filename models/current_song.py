from typing import Optional

from pydantic import BaseModel


class CurrentSong(BaseModel):
    song: str
    artist: str
    album: Optional[str]
    link: Optional[str]
