import sqlite3
import database
from config import DATABASE_PATH


def on_database_operation(func):
    def wrapper(*args, **kwargs):
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            db.commit()
        finally:
            db.close()
        return result
    return wrapper


def get_from_database(func):
    def wrapper(*args, **kwargs):
        db = sqlite3.connect('database/data.db')
        cursor = db.cursor()
        try:
            result = func(cursor, *args, **kwargs)
        finally:
            db.close()
        return result
    return wrapper