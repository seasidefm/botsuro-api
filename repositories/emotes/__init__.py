from typing import Optional
from pydantic import BaseModel
from pymongo.collection import Collection
from redis import Redis

from repositories.database_conn import DatabaseConn
from repositories.mem_cache import MemCache


class EmoteDB(BaseModel):
    id: str
    name: str
    images: dict
    tier: str
    emote_type: str
    emote_set_id: str
    format: list
    scale: list
    theme_mode: list


class EmoteCRUD:
    def __init__(self, collection: Collection, cache: Redis):
        self.collection = DatabaseConn().get_collection("Faves")
        self.cache = MemCache.from_env()

    def create_emote(self, emote: EmoteDB) -> EmoteDB:
        emote_dict = emote.dict()
        self.collection.insert_one(emote_dict)
        self.cache.set(emote.id, emote_dict)
        return emote

    def read_emote(self, emote_id: str) -> Optional[EmoteDB]:
        cached_emote = self.cache.get(emote_id)
        if cached_emote:
            return EmoteDB(**cached_emote)
        else:
            emote_data = self.collection.find_one({"id": emote_id})
            if emote_data:
                emote_model = EmoteDB(**emote_data)
                self.cache.set(emote_id, emote_data)
                return emote_model
        return None

    def update_emote(self, emote_id: str, emote: EmoteDB) -> Optional[EmoteDB]:
        existing_emote = self.read_emote(emote_id)
        if existing_emote:
            updated_data = emote.dict(exclude_unset=True)
            self.collection.update_one({"id": emote_id}, {"$set": updated_data})
            updated_emote = existing_emote.copy(update=updated_data)
            self.cache.set(emote_id, updated_data)
            return updated_emote
        return None

    def delete_emote(self, emote_id: str) -> Optional[EmoteDB]:
        deleted_emote = self.read_emote(emote_id)
        if deleted_emote:
            self.collection.delete_one({"id": emote_id})
            self.cache.delete(emote_id)
        return deleted_emote
