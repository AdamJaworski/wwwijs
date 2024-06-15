import sqlite3

db = sqlite3.connect('../database/data.db')
cursor = db.cursor()


def init_data_db():
    create_users_table = \
        'CREATE TABLE IF NOT EXISTS users (' \
        'username TEXT PRIMARY KEY,' \
        'password TEXT NOT NULL);'

    create_organizations_table = \
        'CREATE TABLE IF NOT EXISTS organizations (' \
        'username TEXT PRIMARY KEY,' \
        'password TEXT NOT NULL);'

    cursor.execute(create_users_table)
    db.commit()
    db.close()


if __name__ == "__main__":
    init_data_db()
