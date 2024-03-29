import sqlite3


conn = sqlite3.connect('C:/Users/о/PycharmProjects/UFA_HACK_2024/frAGILE.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
username TEXT PRIMARY KEY,
pass_hash TEXT NOT NULL,
access_lvl INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
projectname TEXT PRIMARY KEY,
desc TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS components (
compname TEXT PRIMARY KEY,
desc TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cve (
cvename TEXT PRIMARY KEY,
advice TEXT,
desc TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tgusers (
id TEXT PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS compCVE (
compname TEXT PRIMARY KEY,
cvename TEXT NOT NULL,
desc TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tgusers_users_conn (
id TEXT PRIMARY KEY,
username TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS user_projects_conn (
username TEXT PRIMARY KEY,
projectname TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS project_components_conn (
username TEXT PRIMARY KEY,
projectname TEXT NOT NULL
)
''')


def add_user(name, hash, access):
    try:
        cursor.execute('''
        INSERT INTO users (username, pass_hash, access_lvl) VALUES (?, ?, ?)
        ''', (name, hash, access))
    except sqlite3.IntegrityError:
        print("Такой пользователь уже существует")


def delete_user(name):

    cursor.execute('''
        DELETE FROM users
        WHERE username = ?
        ''', (name,))
    cursor.execute('''
        DELETE FROM tgusers_users_conn
        WHERE username = ?
        ''', (name,))
    cursor.execute('''
        DELETE FROM user_projects_conn
        WHERE username = ?
        ''', (name,))

def change_password(name, parol_hash):
    cursor.execute('''
        UPDATE users
        SET pass_hash = ? WHERE username = ?
        ''', (parol_hash, name))


def check_login(name):
    user_exists = (cursor.execute('''
            SELECT EXISTS(SELECT username FROM users WHERE username = ?)
            ''', (name, ))).fetchall()[0][0]
    if not user_exists:
        return False
    else:
        return True
def check_login_data(name, parol_hash):
    user_exists = (cursor.execute('''
        SELECT EXISTS(SELECT pass_hash FROM users WHERE username = ? AND pass_hash = ?)
        ''', (name, parol_hash))).fetchall()[0][0]
    if not user_exists:
        return False
    else:
        return True

def add_tg_user(tg, name):
    cursor.execute('''
            INSERT INTO tgusers (id) VALUES (?)
            ''', (tg,))
    cursor.execute('''
            INSERT INTO tgusers_users_conn (id, username) VALUES (?, ?)
            ''', (tg, name))
def check_if_tg_user_exists(name, tg_id):
    tg_exists = (cursor.execute('''
            SELECT EXISTS(SELECT username, id FROM tgusers_users_conn WHERE username = ? AND id = ?)
            ''', (name, tg_id))).fetchall()[0][0]
    if not tg_exists:
        return False
    else:
        return True



conn.commit()
conn.close()

