from __future__ import print_function
from mysql_connector import mysql_connector
from faker import Faker
import uuid
from random import Random

fake = Faker()
fake.seed(5513)
myPRNG = Random(5513)

# Populates a sample table with a unique id, name and age
# makes sure a table user is created in your local my sql db

with mysql_connector() as m:
    for i in range(100):
        execution_string = "INSERT INTO USER VALUES (" + str(uuid.uuid1().int % 10000000) + ", '" + fake.name() + "', " + str(myPRNG.randint(15, 35)) + ");"
        print(execution_string)
        m.cursor.execute(execution_string)

