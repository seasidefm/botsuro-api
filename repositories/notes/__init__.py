from ..database_conn import DatabaseConn


class Notes:
    def __init__(self, ):
        self.collection = DatabaseConn().get_collection("Faves")

    def create_note(self, user_id: str, content: str):
        return self.collection.insert_one(
            {
                "content": content
            }
        )

    def delete_note(self, note_id: str):
        return self.collection.delete_one(
            {
                "_id": note_id
            }
        )
