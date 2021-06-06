import pyodbc  # pip install pyodbc

SERVER = 'localhost'
DATABASE = 'psz_db'
USERNAME = 'ana'
PASSWORD = 'VeryStrongPassword1.'


class DataBase:

    def __init__(self):
        self.queries = []

    def parse_value(self, value, i):
        # for i between 0 and 5 strings
        # for i equals 6 boolean
        # for i larger than 6 int / float
        if value is None:
            return 'NULL'

        if i <= 5:
            return '"' + value + '"'
        elif i == 6:
            return value
        else:
            return value

    def add_data(self, data):
        insert_into_query = \
            'INSERT INTO `psz_db`.`realty`' \
            '(`type`,' \
            '`offer_type`,' \
            '`heating_type`,' \
            '`city`,' \
            '`quarter`,' \
            '`webpage`,' \
            '`registered`,' \
            '`square_meters`,' \
            '`year_built`,' \
            '`land_area`,' \
            '`total_floors`,' \
            '`floor`,' \
            '`total_rooms`,' \
            '`total_bathrooms`,' \
            '`price`)' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
            % (tuple([self.parse_value(single_data, i) for i, single_data in enumerate(data)]))
        print(insert_into_query)
        self.queries.append(insert_into_query)

    def insert_data(self):
        connection = cursor = None
        try:
            print("insert!")
            connection = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};'
                                        'SERVER=' + SERVER + ';' +
                                        'DATABASE=' + DATABASE + ';' +
                                        'UID=' + USERNAME + ';' +
                                        'PWD=' + PASSWORD + ';')
            cursor = connection.cursor()

            # insert into table

            for query in self.queries:
                print(cursor.execute(query))

            connection.commit()

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error importing data", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


    def empty_database(self):
        connection = cursor = None
        try:
            connection = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};'
                                        'SERVER=' + SERVER + ';' +
                                        'DATABASE=' + DATABASE + ';' +
                                        'UID=' + USERNAME + ';' +
                                        'PWD=' + PASSWORD + ';')
            cursor = connection.cursor()

            # delete from table

            clean_database = 'delete from "realty"'
            cursor.execute(clean_database)
            connection.commit()
            print("Database_empty: ")

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error emptying database", error)

        finally:

            # closing database connection.

            if connection:
                cursor.close()
                connection.close()
