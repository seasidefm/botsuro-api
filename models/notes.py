from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NewNoteInput(BaseModel):
    user: str
    content: str


class Note(BaseModel):
    _id: Optional[str]
    note_id: Optional[str]  # used when returning from the API
    user_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = False
