import json
from typing import List, Iterable, Optional

from models.current_song import CurrentSong
from models.pagination import Pagination
from models.faves import FaveLevel, FaveSong
from services.Cache import get_cache
from ..database_conn import DatabaseConn
from ..mem_cache import MemCache


class Faves:
    def __init__(self):
        self.collection = DatabaseConn().get_collection("Faves")
        self.cache = MemCache.from_env()

    @staticmethod
    def to_fave_list(cursor: Iterable):
        return [
            FaveSong(**item) for item in cursor
        ]

    def get_current_song(self) -> Optional[CurrentSong]:
        data = self.cache.get("song_id:seasidefm")
        data = json.loads(data) if data else None

        if data is None or data.get("error") is not None:
            return None

        return CurrentSong(**data)

    def save(self, user_id: str, level: FaveLevel):
        song = self.get_current_song()
        if not song:
            raise ValueError("current song is None in cache!")

        song_string = f"{song.artist} ||| {song.song}"
        search = {
            "user_id": user_id,
            "level": level,
            "song": song_string,
        }
        existing = self.collection.find_one(search)

        if existing:
            raise ValueError("song already exists in faves!")

        self.collection.insert_one(
            FaveSong(
                user_id=user_id,
                level=level,
                song=song_string,
            ).dict()
        )

        return True

    def get_by_level(self, user_id: str, level: FaveLevel, pagination: Pagination) -> List[FaveSong]:
        faves = self.collection.find({
            "user": user_id,
            "level": level
        }).skip(pagination.offset).limit(pagination.count)

        return self.to_fave_list(faves)
