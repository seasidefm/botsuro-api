import os
from typing import Optional

import requests

from models.streams import Stream


class XiuServer:
    """
    A tiny wrapper for the Xiu service
    """

    def __init__(self):
        self.management_host = os.getenv("XIU_MANAGEMENT_API", "http://192.168.1.168:8001")
        self.botsuro_stream_url = os.getenv("BOTSURO_STREAM_URL", "http://192.168.1.168:8081")

    def get_health(self) -> bool:
        """
        Check if xiu service returns 200 as a quick health check
        :return:
        """
        return requests.get(f"{self.management_host}/", timeout=60).status_code == 200

    def get_active_streams(self) -> Optional[list[str]]:
        """
        Get the active streams from the xiu service
        :return:
        """
        response = requests.get(f"{self.management_host}/get_stream_status", timeout=60)

        if response.status_code != 200:
            return []

        data = [Stream(**s) for s in response.json()]
        print(data)
        return [
            self.botsuro_stream_url
            + '/' + s.identifier.Rtmp.app_name
            + '/' + s.identifier.Rtmp.stream_name
            + '/' + 'test.m3u8'
            for s in data
        ]
