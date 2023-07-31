import os
from typing import Collection, Mapping, Any
from urllib.parse import urlparse

from pymongo import MongoClient


class DatabaseConn:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseConn, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        if mongo_url := os.getenv("DATABASE_URL"):
            self.db_instance = MongoClient(mongo_url)
            self.selected_db = self._get_db_from_url(mongo_url=mongo_url)
        else:
            raise EnvironmentError("DATABASE_URL not found in env")

    @staticmethod
    def _get_db_from_url(mongo_url: str):
        return urlparse(mongo_url).path[1:]

    def get_collection(self, collection: str):
        return self.db_instance.get_database(self.selected_db).get_collection(collection)
