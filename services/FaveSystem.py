from models.faves import FaveLevel
from models.pagination import Pagination
from repositories.faves import Faves


class FaveSystem:
    def __init__(self):
        self.faves = Faves()

    def get_faves_by_level(self, user_id: str, level: FaveLevel, offset=0, count=10):
        return self.faves.get_by_level(
            user_id,
            level,
            pagination=Pagination(
                count=count,
                offset=0,
            )
        )
