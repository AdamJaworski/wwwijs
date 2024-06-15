"""
Plan na całość jest taki:
    * database "data.db" będzie zawierać 2 tabele: users, organizations w relacji 1-inf.
    * w user będą kolumny username, hasedpassword i id. przy pomocy relacji bedzie można wyciągnąć ogarniazację
"""

import sqlite3


class Database:
    db_cursor: sqlite3.Cursor
    db: sqlite3.Connection

    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db_cursor = self.db.cursor()