from models.notes import Note
from ..database_conn import DatabaseConn


class Notes:
    def __init__(self, ):
        self.collection = DatabaseConn().get_collection("Notes")

    def create_note(self, user_id: str, content: str):
        return self.collection.insert_one(
            Note(
                user_id=user_id,
                content=content,
            ).dict()
        ).inserted_id

    def get_notes_for_user(self, user_id: str):
        return self.collection.find(
            {
                "user_id": user_id
            }
        )

    def delete_note(self, note_id: str):
        return self.collection.delete_one(
            {
                "_id": note_id
            }
        )
