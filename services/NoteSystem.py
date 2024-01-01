from models.pagination import Pagination
from models.notes import Note
from repositories.notes import Notes


class NoteSystem:
    def __init__(self):
        self.notes = Notes()

    def create_note_for_user(self, user_id: str, content: str):
        inserted_note = self.notes.create_note(user_id, content)

        return Note(
            _id=str(inserted_note),
            user_id=user_id,
            content=content,
        )

    def get_notes_for_user(
        self, user_id: str, offset=0, count=10, sort_by="created_at", sort_order="desc"
    ):
        return self.notes.get_notes_for_user(
            user_id,
            pagination=Pagination(
                count=count,
                offset=offset,
            ),
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def delete_note(self, note_id: str):
        return self.notes.delete_note(note_id)
