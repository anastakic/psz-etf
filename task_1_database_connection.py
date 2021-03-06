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
            # encoding problems
            value = str(value).replace('č', 'c')
            value = str(value).replace('ć', 'c')
            value = str(value).replace('đ', 'dj')
            value = str(value).replace('Č', 'C')
            value = str(value).replace('Ć', 'C')
            value = str(value).replace('Đ', 'Dj')
            return '"{}"'.format(str(value))

    def add_query(self, data):
        insert_into_query = \
            'INSERT INTO `psz_db`.`real_estate`' \
            '(`type`, ' \
            '`sell_or_rent`, ' \
            '`size`, ' \
            '`price`, ' \
            '`city`, ' \
            '`part_of_city`, ' \
            '`land_size`, ' \
            '`floor`, ' \
            '`total_floors`, ' \
            '`num_of_rooms`, ' \
            '`num_of_bathrooms`, ' \
            '`is_registered`, ' \
            '`parking`, ' \
            '`elevator`, ' \
            '`balcony`, ' \
            '`heating_type`, ' \
            '`year_built`, ' \
            '`construction_type`, ' \
            '`url`) ' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);' \
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
