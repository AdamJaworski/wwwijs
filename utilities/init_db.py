import sqlite3


def init_data_db():
    db = sqlite3.connect('../database/data.db')
    cursor = db.cursor()

    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        
        password TEXT NOT NULL
    );
    '''

    create_organizations_table = '''
    CREATE TABLE IF NOT EXISTS organizations (
        org_name TEXT PRIMARY KEY
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


if __name__ == "__main__":
    init_data_db()
