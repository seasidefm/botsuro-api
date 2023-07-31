from pydantic import BaseModel


class Pagination(BaseModel):
    offset: int = 0
    count: int
