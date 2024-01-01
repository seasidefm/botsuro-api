"""
Song History access
"""
from typing import Optional, Mapping, Any

from pydantic import BaseModel
from pymongo.database import Database


class StoredSongModel(BaseModel):
    """
    A song stored in the database
    """

    _id: Optional[str]
    title: str
    artist: str
    timestamp: int
    album: Optional[str]
    year: Optional[int]
    link: Optional[str]


class SongHistory:
    """
    Song history database
    """

    def __init__(self, database=Database[Mapping[str, Any]]):
        self.collection = database["song_history"]

    def get_history(self, limit=20):
        """
        Get the song history
        :return:
        """

        return list(self.collection.find().sort("timestamp", -1).limit(limit))

    def add_song(self, song: StoredSongModel):
        """
        Add a song to the history
        :param song:
        :return:
        """

        return self.collection.insert_one(song.dict())
