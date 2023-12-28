from dotenv import load_dotenv

from repositories.xiu_server import XiuServer


class StreamsService:
    def __init__(self):
        load_dotenv()
        self.xiu_service = XiuServer()

    def get_active_streams(self):
        return self.xiu_service.get_active_streams()
