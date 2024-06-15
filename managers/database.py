import sqlite3
from data_struct.task import Task


def on_database_operation(func):
    def wrapper(*args, **kwargs):
        db = sqlite3.connect('../database/data.db')
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
        db = sqlite3.connect('../database/data.db')
        cursor = db.cursor()
        try:
            result = func(cursor, *args, **kwargs)
        finally:
            db.close()
        return result
    return wrapper


@on_database_operation
def add_user(cursor, username, password):
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))


@on_database_operation
def add_organization(cursor, org_name):
    cursor.execute('INSERT INTO organizations (org_name) VALUES (?)', (org_name,))


@on_database_operation
def assign_user_to_organization(cursor, username, org_name, access_level):
    cursor.execute('INSERT INTO user_organizations (username, org_name, access_level) VALUES (?, ?, ?)', (username, org_name, access_level))


@on_database_operation
def add_task(cursor, description, org_name):
    cursor.execute('INSERT INTO tasks (description, org_name) VALUES (?, ?)', (description, org_name))


@get_from_database
def get_tasks_for_organization(cursor, org_name):
    cursor.execute('SELECT id, table_id, description FROM tasks WHERE org_name = ?', (org_name,))
    tasks = cursor.fetchall()
    return [Task(task_id=row[0], assigned_to=row[1], description=row[2]) for row in tasks]


@get_from_database
def get_user_access_level(cursor, username, org_name):
    cursor.execute('SELECT access_level FROM user_organizations WHERE username = ? AND org_name = ?', (username, org_name))
    access_level = cursor.fetchone()
    return access_level[0]


add_user('test', 'test')