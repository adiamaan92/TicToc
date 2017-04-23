from mysql_connector import mysql_connector
from row import row

data_list = list()
for i in range(5):
    data_list.append(row(5, 64, 74))

print(data_list[0].value)