import mysql.connector

class DBConnecter():
    '''
    "Wrapper for mysql database connection."
    '''
    db_name = "DriveStats"
    
    def mysql_connection(self):
        # establish db connection
        self.connection = mysql.connector.connect(
            host='database-1.ca3min6kadhv.us-east-1.rds.amazonaws.com', 
            user='admin', 
            port='3306', 
            passwd='12345678', 
            autocommit = True
        )
    
    def mysql_cursor(self):
        self.mysql_connection()
        return self.connection.cursor()
    
    def create_db_and_get_cursor(self):
        '''
        Create a database using mysql_cursor and return cursor
        '''
        cursor = self.mysql_cursor()
        cursor.execute("drop database if exists %s;" % (self.db_name))
        cursor.execute("create database `%s` CHARACTER SET utf8 COLLATE utf8_general_ci;" % (self.db_name))
        cursor.execute("use %s;" % (self.db_name))
        return cursor

    def db_cursor(self):
        '''
        Get a cursor to the database
        '''
        cursor = self.mysql_cursor()
        cursor.execute("use %s;" % (self.db_name))
        return cursor