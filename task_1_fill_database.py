import pyodbc  # pip install pyodbc

SERVER = 'localhost'
DATABASE = 'psz_db'
USERNAME = 'ana'
PASSWORD = 'VeryStrongPassword1.'


class DataBase:

    def __init__(self):
        self.queries = []

    @staticmethod
    def open_connection():
        connection = None
        try:
            connection = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};'
                                        'SERVER=' + SERVER + ';' +
                                        'DATABASE=' + DATABASE + ';' +
                                        'UID=' + USERNAME + ';' +
                                        'PWD=' + PASSWORD + ';')
        except (Exception, pyodbc.DatabaseError) as error:
            print("Connection error:", error)

        return connection

    @staticmethod
    def parse_value(value):
        if value is None:
            return 'NULL'
        try:
            return float(value)
        except ValueError:
            return '"{}"'.format(value)

    def add_data(self, data):
        insert_into_query = \
            'INSERT INTO `psz_db`.`realty`' \
            '(`type`,' \
            '`offer_type`,' \
            '`heating_type`,' \
            '`city`,' \
            '`quarter`,' \
            '`webpage`,' \
            '`state`,' \
            '`parking`,' \
            '`elevator`,' \
            '`balcony`,' \
            '`registered`,' \
            '`square_meters`,' \
            '`year_built`,' \
            '`land_area`,' \
            '`total_floors`,' \
            '`floor`,' \
            '`total_rooms`,' \
            '`total_bathrooms`,' \
            '`price`)' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
            % (tuple([self.parse_value(single_data) for single_data in data]))

        print(insert_into_query)
        self.queries.append(insert_into_query)

    def insert_data(self):
        connection = cursor = None
        try:
            connection = self.open_connection()
            cursor = connection.cursor()

            # insert into table
            for query in self.queries:
                cursor.execute(query)

            connection.commit()
            if len(self.queries) > 0:
                print("Inserted {} rows in database done!".format(str(len(self.queries))))

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error inserting data", error)
            
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

