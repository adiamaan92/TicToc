from __future__ import print_function

from random import Random

from faker import Faker

from mysql_connector import mysql_connector
from user import User

fake = Faker()
fake.seed(5513)
myPRNG = Random(5513)


# Populates a sample table with a unique id, name and age
# makes sure a table user is created in your local my sql db
# Test


def populate_user(n, db=True):
    user_list = list()
    with mysql_connector() as m:
        for i in range(n):
            user_name = fake.name()
            user_age = myPRNG.randint(15, 35)
            execution_string = "INSERT INTO USER VALUES (" + str(i) + ", '" + user_name + "', " \
                               + str(user_age) + ");"
            print(execution_string)
            user = User(i, user_name, user_age)
            user_list.append(user)
            if db:
                m.cursor.execute(execution_string)
        return user_list
