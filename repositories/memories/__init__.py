from typing import Literal


from models.memory import Memory
from repositories.database_conn import DatabaseConn


class Memories:
    """
    Memory service
    """

    def __init__(self):
        self.collection = DatabaseConn().get_collection("Memory")

    def save(self, memory: Memory):
        """
        Saves a memory object to the collection.

        :param memory: The memory object to be saved.
        :type memory: Memory
        """
        self.collection.insert_one(memory.dict())

    def get_memories(
        self, platform: Literal["TWITCH", "DISCORD", "MINECRAFT"], count: int = 10
    ):
        """
        Retrieve memories from the database for a specific platform.

        :param platform: The platform to fetch the memories from. Valid options are 'Memory.platform'.
        :param count: The number of memories to retrieve. Defaults to 10 if not provided.
        :return: A list of Memory instances retrieved from the database.
        """

        memories = [
            Memory(**doc)
            for doc in self.collection.find({"platform": platform})
            .sort("created_at", -1)
            .limit(count)
        ]
        memories.reverse()

        return memories
