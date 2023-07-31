from typing import List, Iterable

from models.pagination import Pagination
from models.faves import FaveLevel, FaveSong
from ..database_conn import DatabaseConn


class Faves:
    def __init__(self):
        self.collection = DatabaseConn().get_collection("Faves")

    @staticmethod
    def to_fave_list(cursor: Iterable):
        return [
            FaveSong(**item) for item in cursor
        ]

    def get_by_level(self, user_id: str, level: FaveLevel, pagination: Pagination) -> List[FaveSong]:
        faves = self.collection.find({
            "userId": user_id,
            "level": level
        }).skip(pagination.offset).limit(pagination.count)

        return self.to_fave_list(faves)
