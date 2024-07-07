from data_struct.task import Task
from managers.database_decorators import on_database_operation, get_from_database


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
def add_task(cursor, table_id, description, org_name, priority):
    assert 0 < table_id < 5, "Wrong table id"
    assert type(org_name) is str, "Wrong type of org name"

    create_date = 0     # TODO create_date
    cursor.execute('INSERT INTO tasks (table_id, description, org_name, create_date priority) VALUES (?, ?)',
                   (table_id, description, org_name, create_date, priority))


@on_database_operation
def add_user_to_task(cursor, username, task_id):
    cursor.execute('INSERT INTO user_task (username, task_id) VALUES (?, ?)', (username, task_id))


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


@get_from_database
def get_user_by_username(cursor, username):
    cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user

