import sqlite3
from db_config import db_path


class DataBase:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        pass_hash TEXT NOT NULL,
        access_lvl INTEGER
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
        projectname TEXT PRIMARY KEY,
        desc TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS components (
        comp_name TEXT PRIMARY KEY,
        comp_version TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS cve (
        id_bdu TEXT PRIMARY KEY,
        cve_name TEXT,
        cve_desc TEXT,
        soft_name TEXT,
        soft_version TEXT,
        soft_type TEXT,
        danger_lvl TEXT,
        advise TEXT,
        cve_status TEXT, 
        id_cve TEXT,
        error_desc TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tgusers (
        id TEXT PRIMARY KEY
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS compCVE (
        compname TEXT PRIMARY KEY,
        cvename TEXT NOT NULL,
        desc TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tgusers_users_conn (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_projects_conn (
        username TEXT PRIMARY KEY,
        projectname TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_components_conn (
        projectname TEXT PRIMARY KEY,
        component TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_user(self, user_name, hash, access):
        self.cursor.execute('''
        INSERT INTO users (username, pass_hash, access_lvl) VALUES (?, ?, ?)
        ''', (user_name, hash, access))
        self.conn.commit()

    def delete_user(self, user_name):

        self.cursor.execute('''
            DELETE FROM users
            WHERE username = ?
            ''', (user_name,))
        self.cursor.execute('''
            DELETE FROM tgusers_users_conn
            WHERE username = ?
            ''', (user_name,))
        self.cursor.execute('''
            DELETE FROM user_projects_conn
            WHERE username = ?
            ''', (user_name,))
        self.conn.commit()

    def check_login(self, user_name):
        user_exists = (self.cursor.execute('''
                SELECT EXISTS(SELECT username FROM users WHERE username = ?)
                ''', (user_name,))).fetchall()[0][0]
        if not user_exists:
            return False
        else:
            return True

    def check_login_data(self, user_name, parol_hash):
        user_exists = (self.cursor.execute('''
            SELECT EXISTS(SELECT pass_hash FROM users WHERE username = ? AND pass_hash = ?)
            ''', (user_name, parol_hash))).fetchall()[0][0]
        if not user_exists:
            return False
        else:
            return True

    def change_password(self, user_name, parol_hash):
        self.cursor.execute('''
            UPDATE users
            SET pass_hash = ? WHERE username = ?
            ''', (parol_hash, user_name))
        self.conn.commit()

    def add_tg_user(self, tg, user_name):
        self.cursor.execute('''
                INSERT INTO tgusers (id) VALUES (?)
                ''', (tg,))
        self.cursor.execute('''
                INSERT INTO tgusers_users_conn (id, username) VALUES (?, ?)
                ''', (tg, user_name))
        self.conn.commit()

    def check_if_tg_user_exists(self, user_name, tg_id):
        tg_exists = (self.cursor.execute('''
                SELECT EXISTS(SELECT username, id FROM tgusers_users_conn WHERE username = ? AND id = ?)
                ''', (user_name, tg_id))).fetchall()[0][0]
        if not tg_exists:
            return False
        else:
            return True

    def delete_tg_user(self, user_name, tg_id):
        tg_exists = (self.cursor.execute('''
                    SELECT EXISTS(SELECT username, id FROM tgusers_users_conn WHERE  id = ?)
                    ''', (user_name, tg_id))).fetchall()[0][0]
        if not tg_exists:
            self.cursor.execute('''DELETE id FROM tgusers WHERE id = ?)
            ''', (tg_id,))
            self.conn.commit()
        else:
            return True

    def add_project(self, project_name, des):
        self.cursor.execute('''
            INSERT INTO projects (projectname, des) VALUES (?, ?)
            ''', (project_name, des))
        self.conn.commit()

    def check_if_project_exist(self, project_name):
        pro_exists = (self.cursor.execute('''
                    SELECT EXISTS(SELECT projectname FROM projects WHERE projectname = ?)
                    ''', (project_name,))).fetchall()[0][0]
        if not pro_exists:
            return False
        else:
            return True

    def delete_project(self, project_name):
        self.cursor.execute('''
            DELETE projectname FROM projects WHERE projectname = ?)
            ''', project_name)
        self.conn.commit()

    def add_user_to_project(self, user_name, project_name):
        self.cursor.execute('''
                INSERT INTO user_projects_conn (username, projectname) VALUES (?, ?)
                ''', (user_name, project_name))
        self.conn.commit()


    def add_components_to_project(self, project_name, component):
        self.cursor.execute('''
                INSERT INTO project_component_conn (projectname, component) VALUES (?, ?)
                ''', (project_name, component))
        self.conn.commit()
    def add_cve_to_components(self, component, cve, desc):
        self.cursor.execute('''
                INSERT INTO compCVE (compname, cvename, desc) VALUES (?, ?, ?)
                ''', (component, cve, desc))
        self.conn.commit()
    def add_data_to_cve(self, corteg):
        self.cursor.execute('''
                INSERT INTO cve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (corteg))
        self.conn.commit()
    def close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    dbase = DataBase(conn, cursor)

    dbase.close()

