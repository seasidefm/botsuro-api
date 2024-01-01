import os
from typing import Collection, Mapping, Any
from urllib.parse import urlparse

import certifi
from pymongo import MongoClient


class DatabaseConn:
    def __init__(self):
        if mongo_url := os.getenv("DATABASE_URL"):
            self.db_instance = MongoClient(
                mongo_url, connect=True, tlsCAFile=certifi.where()
            )
            self.selected_db = self._get_db_from_url(mongo_url=mongo_url)
        else:
            raise EnvironmentError("DATABASE_URL not found in env")

    @staticmethod
    def _get_db_from_url(mongo_url: str):
        return urlparse(mongo_url).path[1:]

    def get_collection(self, collection: str):
        return self.db_instance.get_database(self.selected_db).get_collection(
            collection
        )
