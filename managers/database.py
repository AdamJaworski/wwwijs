from data_struct import Task, Org
from managers.database_decorators import on_database_operation, get_from_database


@on_database_operation
def add_user(cursor, username, password):
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))


@on_database_operation
def add_organization(cursor, org_name, password):
    cursor.execute('INSERT INTO organizations (org_name, password) VALUES (?, ?)', (org_name, password))


@on_database_operation
def assign_user_to_organization(cursor, username, org_name, access_level=None):
    assert type(username) is str, "Wrong type of username"
    assert type(org_name) is str, "Wrong type of org name"

    access_level = 1 if not access_level else access_level
    assert 0 < access_level < 6, "Wrong level of access"

    cursor.execute('INSERT INTO user_organizations (username, org_name, access_level) VALUES (?, ?, ?)', (username, org_name, access_level))


@on_database_operation
def add_task(cursor, table_id, description, org_name, priority, title):
    assert 0 < table_id < 5, "Wrong table id"
    assert 0 < priority < 5, "Wrong priority" # TODO: to nie miało buć do 4? ? 
    assert type(org_name) is str, "Wrong type of org name"
    assert type(title) is str, "Wrong type of title"
    assert type(description) is str, "Wrong type of description"

    create_date = 0     # TODO create_date
    cursor.execute('INSERT INTO tasks (table_id, description, org_name, create_date, priority, title) VALUES (?, ?, ?, ?, ?, ?)',
                   (table_id, description, org_name, create_date, priority, title))


@on_database_operation
def update_task_table(cursor, task_id, new_table):
    cursor.execute('UPDATE tasks SET table_id = ? WHERE id = ?', (new_table, task_id))


@on_database_operation
def change_user_permission(cursor, username, org_name, access_lvl):
    cursor.execute('UPDATE user_organizations SET access_level = ? WHERE username = ? AND org_name = ?', (access_lvl, username, org_name))


@on_database_operation
def delete_task(cursor, task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id, ))


@on_database_operation
def add_user_to_task(cursor, username, task_id):
    cursor.execute('INSERT INTO user_task (username, task_id) VALUES (?, ?)', (username, task_id))


@on_database_operation
def get_users_from_task(cursor, task_id):
    cursor.execute('SELECT username FROM tasks FULL JOIN user_task ON tasks.id = user_task.task_id WHERE task_id = ?', (task_id,))
    users = cursor.fetchall()
    return [user[0] for user in users]


@get_from_database
def get_tasks_for_organization(cursor, org_name):
    cursor.execute('SELECT id, table_id, description, title, priority FROM tasks WHERE org_name = ?', (org_name,))
    tasks = cursor.fetchall()
    return [Task(task_id=row[0], assigned_to=row[1], description=row[2], title=row[3], priority=row[4]) for row in tasks]


@get_from_database
def get_user_orgs(cursor, username):
    cursor.execute('SELECT org_name, access_level FROM user_organizations WHERE username = ?', (username,))
    orgs = cursor.fetchall()
    return [Org(org_name=row[0], access_lvl=row[1]) for row in orgs]


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


@get_from_database
def get_org_by_org_name(cursor, org_name):
    cursor.execute('SELECT org_name, password FROM organizations WHERE org_name = ?', (org_name,))
    org = cursor.fetchone()
    return org


@get_from_database
def get_org_by_org_task_id(cursor, task_id):
    cursor.execute('SELECT org_name FROM tasks WHERE id = ?', (task_id,))
    org = cursor.fetchone()
    return org[0]


@get_from_database
def get_task_by_id(cursor, task_id):
    cursor.execute('SELECT id, table_id, description, title, priority FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchall()[0]
    return Task(task_id=row[0], assigned_to=row[1], description=row[2], title=row[3], priority=row[4])