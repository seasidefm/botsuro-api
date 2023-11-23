import enum

from models.faves import FaveLevel, FaveSong
from models.pagination import Pagination
from repositories.faves import Faves


class FaveResult(enum.Enum):
    NOTFOUND = "notfound"
    SAVED = "saved"
    EXISTS = "exists",
    ERROR = "error"


class FaveSystem:
    def __init__(self):
        self.faves = Faves()

    def get_faves_by_level(self, user_id: str, level: FaveLevel, offset=0, count=10, sort_by="fave_date", sort_order="desc"):
        return self.faves.get_by_level(
            user_id,
            level,
            pagination=Pagination(
                count=count,
                offset=offset,
            ),
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def fave_this(self, user_id: str, level: FaveLevel) -> FaveResult:
        try:
            self.faves.save(user_id, level)
            return FaveResult.SAVED
        except ValueError as e:
            if "not found" in str(e):
                return FaveResult.NOTFOUND
            if "already exists" in str(e):
                return FaveResult.EXISTS
            else:
                print("Unknown error: ", e)

        return FaveResult.ERROR
