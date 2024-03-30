import sqlite3
from DataBase import DataBase
from db_config import db_path


conn = sqlite3.connect(db_path)
cursor = conn.cursor()



dbase = DataBase(db_path)

print(dbase.add_user('timur1', '123456', 0))
print(dbase.check_login('timur'))

