from pydantic import BaseModel


class NewNoteInput(BaseModel):
    user: str
    content: str
