from typing import Iterable

from models.notes import Note
from models.pagination import Pagination
from ..database_conn import DatabaseConn


class Notes:
    def __init__(self, ):
        self.collection = DatabaseConn().get_collection("Notes")

    @staticmethod
    def to_note_list(cursor: Iterable):
        return [
            Note(**{**item, "note_id": str(item.get("_id"))}) for item in cursor
        ]

    def create_note(self, user_id: str, content: str):
        return self.collection.insert_one(
            Note(
                user_id=user_id,
                content=content,
            ).dict()
        ).inserted_id

    def get_notes_for_user(self, user_id: str, pagination: Pagination, sort_by="created_at", sort_order="desc"):
        config = {
            "user_id": user_id
        }

        notes = (self.collection.find(config)
                 .sort(sort_by, -1 if sort_order == "desc" else 1)
                 .skip(pagination.offset).limit(pagination.count))

        return {
            "notes": self.to_note_list(notes),
            "total": self.collection.count_documents(config),
            "pagination": pagination,
        }

    def delete_note(self, note_id: str):
        return self.collection.delete_one(
            {
                "_id": note_id
            }
        )
