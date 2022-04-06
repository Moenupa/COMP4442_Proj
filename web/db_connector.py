import mysql.connector
import os

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
        self.USER=os.getenv("USER")
        self.PORT=os.getenv("PORT")
        self.PASSWD=os.getenv("PASSWD")
        self.DB_NAME=os.getenv("DB_NAME")
        self.SUMMARY_TABLE=os.getenv("SUMMARY_TABLE")
        self.SPEED_TABLE=os.getenv("SPEED_TABLE")
    
    def establish_connection(self):
        # establish db connection
        self.connection = mysql.connector.connect(
            host = self.HOST, 
            user = self.USER, 
            port = self.PORT, 
            passwd = self.PASSWD, 
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
        cursor.execute(f"DROP DATABASE if exists {self.DB_NAME};")
        cursor.execute(f"CREATE DATABASE {self.DB_NAME} CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cursor.execute(f"USE {self.DB_NAME};")
        return cursor

    def get_db_cursor(self):
        '''
        Establish a connection to the database;
        Get a cursor.
        '''
        cursor = self.get_mysql_cursor()
        cursor.execute(f"USE {self.DB_NAME};")
        return cursor