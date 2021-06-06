import pyodbc  # pip install pyodbc

SERVER = 'localhost'
DATABASE = 'psz_db'
USERNAME = 'ana'
PASSWORD = 'VeryStrongPassword1.'


class DataBase:

    @staticmethod
    def insert_data(data):
        connection = cursor = None
        try:
            connection = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};'
                                        'SERVER=' + SERVER + ';' +
                                        'DATABASE=' + DATABASE + ';' +
                                        'UID=' + USERNAME + ';' +
                                        'PWD=' + PASSWORD + ';')
            cursor = connection.cursor()

            # insert into table

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error importing data", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def empty_database():
        connection = cursor = None
        try:
            connection = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};'
                                        'SERVER=' + SERVER + ';' +
                                        'DATABASE=' + DATABASE + ';' +
                                        'UID=' + USERNAME + ';' +
                                        'PWD=' + PASSWORD + ';')
            cursor = connection.cursor()

            # delete from table

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error emptying database", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


