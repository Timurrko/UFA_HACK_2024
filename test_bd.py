import sqlite3

import pandas as pd

from DataBase import DataBase
from db_config import db_path, excel_path

df = pd.read_excel(open(excel_path, 'rb'), index_col=0)
#print(list(df.iloc[0]))

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

dbase = DataBase(conn, cursor)
#print(len(list(df.iloc[1])))
for i in range(len(df)):
    try:
        dbase.add_data_to_cve(list(df.iloc[i]))
    except:
        pass
dbase.close()
