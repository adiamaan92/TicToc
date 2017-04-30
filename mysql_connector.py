import config as cfg
import mysql.connector


class mysql_connector(object):

    # Constructor that reads the config.py file and establishes the connection with the local
    # mySQL DB running on the local host
    # enter and exist is used to enable the connection to be established like
    # with mysql() as m:
    #   use m as the object
    # no need to explicitly close the connection since this is handled in the exit (destructor)

    def __init__(self):
        self.connection = mysql.connector.connect(user=cfg.mysql_config['user'], password=cfg.mysql_config['password'],
                                                  host=cfg.mysql_config['host'], db=cfg.mysql_config['db'])
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def __enter__(self):
        # print("Connection opened!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print("Connection closed!")
        self.connection.close()





