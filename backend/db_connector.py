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
        self.HOST=os.getenv("HOST")
        self.ADMIN=os.getenv("ADMIN")
        self.PORT=os.getenv("PORT")
        self.PASSWD=os.getenv("PASSWD")
        self.DB_NAME=os.getenv("DB_NAME")
        self.SUMMARY_TABLE=os.getenv("SUMMARY_TABLE")
        self.SPEED_TABLE=os.getenv("SPEED_TABLE")
    
    def establish_connection(self):
        # establish db connection
        self.connection = mysql.connector.connect(
            host = self.HOST, 
            user = self.ADMIN, 
            port = self.PORT, 
            passwd = self.PASSWD, 
            autocommit = True
        )
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
    
    def create_mysql_cursor(self):
        '''
        Establish a connection to mysql;
        Get a cursor.
        '''
        self.establish_connection()
        self.cursor = self.connection.cursor()
    
    def create_db_and_get_cursor(self):
        '''
        Create a database using mysql_cursor;
        Establish connection;
        Get a cursor.
        '''
        self.create_mysql_cursor()
        self.cursor.execute(f"DROP DATABASE if exists {self.DB_NAME};")
        self.cursor.execute(f"CREATE DATABASE {self.DB_NAME} CHARACTER SET utf8 COLLATE utf8_general_ci;")
        self.cursor.execute(f"USE {self.DB_NAME};")
        return self.cursor

    def get_db_cursor(self):
        '''
        Establish a connection to the database;
        Get a cursor.
        '''
        self.create_mysql_cursor()
        self.cursor.execute(f"USE {self.DB_NAME};")
        return self.cursor