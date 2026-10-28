"""Local note storage, independent of the Flet interface."""

import sqlite3
from contextlib import closing
from pathlib import Path


NOTES_PATH = Path(__file__).with_name("notes.sqlite3")


def load_notes():
    with closing(sqlite3.connect(NOTES_PATH)) as connection:
        with connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS notes "
                "(id TEXT PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL)"
            )
        return {
            note_id: {"title": title, "body": body}
            for note_id, title, body in connection.execute(
                "SELECT id, title, body FROM notes ORDER BY rowid"
            )
        }


def save_note(note_id, title, body):
    with closing(sqlite3.connect(NOTES_PATH)) as connection:
        with connection:
            connection.execute(
                "INSERT INTO notes (id, title, body) VALUES (?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET title=excluded.title, body=excluded.body",
                (note_id, title, body),
            )


def delete_note(note_id):
    with closing(sqlite3.connect(NOTES_PATH)) as connection:
        with connection:
            connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
