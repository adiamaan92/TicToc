from __future__ import print_function
from mysql_connector import mysql_connector

with mysql_connector() as m:
    print(m.cursor.execute("SELECT * FROM USER;"))

