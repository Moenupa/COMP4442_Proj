import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

class DBConnector():
    '''
    Wrapper for preset information and mysql database connection.
    How to use this:
        ```python
        from db_connector import DBConnector
        connector = DBConnector()               # prepare information to connect, 
                                                # does not really establish connection
        
        # the following will really establish connection
        connection = connector.establish_connection()   # get connection but not cursor
        cursor = connector.create_db_and_get_cursor()   # get cursor if database is not initialized
        cursor = connector.get_db_cursor()              # get cursor if database is already initialized
        ```
    '''
    def __init__(self) -> None:
        self.database_name = os.getenv("DATABASE")
        self.summary_table_name = os.getenv("SUMMARY_TABLE")
        self.speed_table_name = os.getenv("SPEED_TABLE")
        self.host = os.getenv("HOST")
        self.user = os.getenv("ADMIN")
        self.port = os.getenv("PORT")
        self.passwd = os.getenv("PASSWD")
    
    def establish_connection(self):
        # establish db connection
        self.connection = mysql.connector.connect(
            host = self.host, 
            user = self.user, 
            port = self.port, 
            passwd = self.passwd, 
            autocommit = True
        )
    
    def get_mysql_cursor(self):
        '''
        Establish a connection to mysql;
        Get a cursor.
        '''
        self.establish_connection()
        return self.connection.cursor()
    
    def create_db_and_get_cursor(self):
        '''
        Create a database using mysql_cursor;
        Establish connection;
        Get a cursor.
        '''
        cursor = self.get_mysql_cursor()
        cursor.execute(f"DROP DATABASE if exists {self.database_name};")
        cursor.execute(f"CREATE DATABASE {self.database_name} CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cursor.execute(f"USE {self.database_name};")
        return cursor

    def get_db_cursor(self):
        '''
        Establish a connection to the database;
        Get a cursor.
        '''
        cursor = self.get_mysql_cursor()
        cursor.execute(f"USE {self.database_name};")
        return cursor