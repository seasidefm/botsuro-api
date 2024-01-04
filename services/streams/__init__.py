from datetime import datetime
import json
import time

from dotenv import load_dotenv

from models.streams.events import Publish
from models.streams.events import UnPublish
from repositories.mem_cache import MemCache
from repositories.xiu_server import XiuServer


class StreamsService:
    def __init__(self):
        load_dotenv()
        self.xiu_service = XiuServer()
        self.cache = MemCache.from_env()

    def get_active_streams(self):
        return self.xiu_service.get_active_streams()

    def set_stream_active(self, pub: Publish):
        stream_name = pub.identifier.Rtmp.stream_name
        self.cache.set(
            f"stream:{stream_name}",
            json.dumps({"live_since": time.mktime(datetime.now().timetuple())}),
        )

    def set_stream_inactive(self, unpub: UnPublish):
        stream_name = unpub.identifier.Rtmp.stream_name
        self.cache.set(
            f"stream:{stream_name}",
        )
