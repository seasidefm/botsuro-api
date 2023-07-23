import requests


class SongIdProxy:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def health_check(self):
        return requests.get(self.endpoint, timeout=45).status_code == 200, "OK"

    def get_song_id(self, creator: str):
        return requests.get(f"{self.endpoint}/identify/{creator}", timeout=90).json()
