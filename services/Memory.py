from typing import Mapping, Any

from pymongo.database import Database

from Cache import Cache


class Memories:
    """

    """
    def __init__(self, database: Database[Mapping[str, Any]], cache: Cache):
        self.collection = database["memories"]

    def get_memories_for_context(self, context: str):
        """
        Get the memories for a given context
        :param context:
        :return:
        """

        return list(self.collection.find({"context": context}))
