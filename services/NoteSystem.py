from models.notes import Note
from repositories.notes import Notes


class NoteSystem:
    def __init__(self):
        self.notes = Notes()

    def create_note_for_user(self, user_id: str, content: str):
        inserted_note = self.notes.create_note(
            user_id,
            content
        )

        return Note(
            _id=str(inserted_note),
            user_id=user_id,
            content=content,
        )

    def get_notes_for_user(self, user_id: str):
        notes = self.notes.get_notes_for_user(
            user_id
        )

        return [
            Note(**note, note_id=str(note.get("_id"))) for note in notes
        ]

    def delete_note(self, note_id: str):
        return self.notes.delete_note(
            note_id
        )
