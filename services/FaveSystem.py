from typing import Mapping, Any

from pymongo import MongoClient
from pymongo.database import Database


class FaveSystem:
    def __init__(self, database: Database[Mapping[str, Any]]):
        self.collection = database["faves"]

    def get_faves_for_user(self, user: str):
        """
        Get the faves for a given user
        :param user:
        :return:
        """

        return list(self.collection.find({"user": user, "superfave": False}))

    def get_superfaves_for_user(self, user: str):
        """
        Get the superfaves for a given user
        :param user:
        :return:
        """

        return list(self.collection.find({"user": user, "superfave": True}))
