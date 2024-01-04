from typing import Optional

from pydantic.main import BaseModel

from .on_publish import Publish
from .on_subscribe import Subscribe
from .on_unpublish import UnPublish


class BaseEvent(BaseModel):
    Publish: Optional[Publish]
    Subscribe: Optional[Subscribe]
    UnPublish: Optional[UnPublish]
