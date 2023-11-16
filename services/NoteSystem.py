from repositories.notes import Notes


class NoteSystem:
    def __init__(self):
        self.notes = Notes()

    def create_note_for_user(self, user_id: str, content: str):
        return self.notes.create_note(
            user_id,
            content
        )

    def delete_note(self, note_id: str):
        return self.notes.delete_note(
            note_id
        )
