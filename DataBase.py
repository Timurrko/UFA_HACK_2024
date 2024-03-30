import sqlite3
from db_config import db_path


class DataBase:
    def __init__(self, path):
        self.path = path
        conn = sqlite3.connect(self.path)
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
        comp_name TEXT PRIMARY KEY,
        comp_version TEXT
        )
        ''')

        cursor.execute('''
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
        username TEXT PRIMARY KEY,
        id TEXT NOT NULL
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
        projectname TEXT PRIMARY KEY,
        component TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()


    def add_user(self, user_name, hash, access):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (username, pass_hash, access_lvl) VALUES (?, ?, ?)
        ''', (user_name, hash, access))
        conn.commit()
        conn.close()

    def delete_user(self, user_name):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM users
            WHERE username = ?
            ''', (user_name,))
        cursor.execute('''
            DELETE FROM tgusers_users_conn
            WHERE username = ?
            ''', (user_name,))
        cursor.execute('''
            DELETE FROM user_projects_conn
            WHERE username = ?
            ''', (user_name,))
        conn.commit()
        conn.close()

    def check_if_login_exists(self, user_name):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        user_exists = (cursor.execute('''
                SELECT EXISTS(SELECT username FROM users WHERE username = ?)
                ''', (user_name,))).fetchall()[0][0]
        if not user_exists:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def get_username_for_tg_user(self, tg_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        user_name = cursor.execute('''SELECT username FROM tgusers_users_conn
        WHERE id = ?''', (tg_id,)).fetchall()[0]
        conn.close()
        return user_name

    def check_login_data(self, user_name, parol_hash):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        user_exists = (cursor.execute('''
            SELECT EXISTS(SELECT username FROM users WHERE username = ? AND pass_hash = ?)
            ''', (user_name, parol_hash))).fetchall()[0][0]
        if not user_exists:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def change_password(self, user_name, parol_hash):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET pass_hash = ? WHERE username = ?
            ''', (parol_hash, user_name))
        conn.commit()
        conn.close()

    def add_tg_user_and_sys_username(self, user_name, tg_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO tgusers (id) VALUES (?)
                ''', (tg_id,))
        cursor.execute('''
                INSERT INTO tgusers_users_conn (username, id) VALUES (?, ?)
                ''', (user_name, tg_id))
        conn.commit()
        conn.close()

    def check_if_tg_user_exists(self, tg_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        tg_exists = (cursor.execute('''
                SELECT EXISTS(SELECT  id FROM tgusers WHERE id = ?)
                ''', (tg_id, ))).fetchall()[0][0]
        if not tg_exists:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def delete_conn_between_tg_id_and_username(self, user_name, tg_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            tg_exists = (cursor.execute('''
                    SELECT username, id FROM tgusers_users_conn WHERE  id = ? AND username = ?
                    ''', (tg_id, user_name))).fetchall()[0][0]
            tg_exists = True
        except IndexError:
            tg_exists = False
        if tg_exists:

            cursor.execute('''DELETE FROM tgusers_users_conn WHERE username = ?
                        ''', (user_name,))
            conn.commit()
            conn.close()
        else:
            conn.commit()
            conn.close()
            return True

    def verify_user(self, tg_id):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            user_autho = cursor.execute('''
                    SELECT id FROM tgusers_users_conn WHERE id = ?
                    ''', (tg_id,)).fetchall()[0][0]
            return True
        except IndexError:
            return False



    def add_project(self, project_name, des):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        print(1)
        cursor.execute('''
            INSERT INTO projects (projectname, desc) VALUES (?, ?)
            ''', (project_name, des))
        print(2)
        conn.commit()
        conn.close()

    def check_if_project_exist(self, project_name):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        pro_exists = (cursor.execute('''
                    SELECT EXISTS(SELECT projectname FROM projects WHERE projectname = ?)
                    ''', (project_name,))).fetchall()[0][0]
        if not pro_exists:
            conn.close()
            return False
        else:
            conn.close()
            return True

    def delete_project(self, project_name):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE projectname FROM projects WHERE projectname = ?)
            ''', project_name)
        conn.commit()
        conn.close()

    def add_user_to_project(self, user_name, project_name):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO user_projects_conn (username, projectname) VALUES (?, ?)
                ''', (user_name, project_name))
        conn.commit()
        conn.close()

    def add_components_to_project(self, project_name, component):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO project_component_conn (projectname, component) VALUES (?, ?)
                ''', (project_name, component))
        conn.commit()
        conn.close()

    def add_cve_to_components(self, component, cve, desc):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO compCVE (compname, cvename, desc) VALUES (?, ?, ?)
            ''', (component, cve, desc))
        conn.commit()
        conn.close()

    def add_data_to_cve(self, corteg):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO cve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', corteg)
        conn.commit()
        conn.close()

    def add_components(self, comp_name):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO components VALUES (?)
                ''', (comp_name,))
        conn.commit()
        conn.close()

    def select_project(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        projects = cursor.execute('''
            SELECT * FROM projects 
            ''',).fetchall()
        conn.commit()
        conn.close()
        return (projects)



if __name__ == '__main__':
    dbase = DataBase(db_path)
    #print(dbase.verify_user('1480780000006'))
