import sqlite3
import uuid
import os
import numpy as np
from config import DATABASE_PATH
from managers.database import *
from werkzeug.security import generate_password_hash


def init_data_db():
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()

    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    '''

    create_organizations_table = '''
    CREATE TABLE IF NOT EXISTS organizations (
        org_name TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    '''

    # Create tasks table
    create_tasks_table = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        org_name TEXT,
        create_date REAL NOT NULL,
        priority INT NOT NULL,
        title TEXT NOT NULL,
        FOREIGN KEY (org_name) REFERENCES organizations(org_name)
    );
    '''

    create_user_organizations_table = '''
    CREATE TABLE IF NOT EXISTS user_organizations (
        username TEXT,
        org_name TEXT,
        access_level INT NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (org_name) REFERENCES organizations(org_name),
        PRIMARY KEY (username, org_name)
    );
    '''

    create_user_task_table = '''
    CREATE TABLE IF NOT EXISTS user_task (
        username TEXT,
        task_id INTEGER,
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (username) REFERENCES tasks(id)
    );
    '''

    cursor.execute(create_users_table)
    cursor.execute(create_organizations_table)
    cursor.execute(create_tasks_table)
    cursor.execute(create_user_organizations_table)
    cursor.execute(create_user_task_table)

    db.commit()
    db.close()


def fill_with_random_orgs():
    for i in range(1, 5):
        org_name = org_password = f"example_org{i}"
        org_password = generate_password_hash(org_password)

        add_organization(org_name, org_password)

        for task_index in range(25):
            table_id = np.random.randint(1, 5)
            prio     = np.random.randint(1, 5)
            #table_id, description, org_name, priority, title
            add_task(table_id, "Example task created with random fill", org_name, prio, str(uuid.uuid4()))


if __name__ == "__main__":
    try:
        os.remove(DATABASE_PATH)
    except Exception:
        pass
    init_data_db()
    fill_with_random_orgs()
