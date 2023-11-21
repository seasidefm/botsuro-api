from pydantic import BaseModel


class ChatCompletion(BaseModel):
    """
    Chat completion model, barebones for now
    """
    content: str
