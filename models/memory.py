from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Memory(BaseModel):
    """
    Memory model
    """

    created_at: datetime = None
    role: str
    content: str
    platform: str
