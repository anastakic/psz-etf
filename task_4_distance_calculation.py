import requests                     # pip install requests
import re
import pyodbc
import pandas as pd
from bs4 import BeautifulSoup       # pip install beautifulsoup4

from task_1_database_connection import DataBase


class DistanceCalculation:

    def __init__(self):
        self.distances = dict()
        self.dataframe = None

    @staticmethod
    def parse_data(url):
        try:
            realty = requests.get(url)
            inner_soup = BeautifulSoup(realty.content, "html.parser")
            find_km = re.search('"([\d]+,?[\d]*) km', str(inner_soup), re.IGNORECASE)
            find_m = re.search('"([\d]+,?[\d]*) m', str(inner_soup), re.IGNORECASE)
            if find_km:
                return float(find_km.group(1).replace(',', '.')) * 1000
            elif find_m:
                return float(find_km.group(1).replace(',', '.'))
            return None

        except Exception as e:
            print("Error with parsing data:", str(e))
            return None

    def collect_data(self, part_to):
        try:
            part_to = part_to.replace(' ', '%20').lower()

            url = 'https://www.google.com/maps/dir/knez%20mihailova/{}/?hl=sr'.format(part_to)
            # print(url)
            return self.parse_data(url)

        except requests.exceptions.RequestException as e:
            print('Skipping. Connection error.', e)

        except Exception as e:
            print("Error:", e)
            pass

    def get_distance(self, part_to):
        # uncomment in case of problems with distance calculation
        #
        # if part_to.find('(') > 0:
        #    part_to = part_to[:part_to.find('(')]
        #
        # part_to = part_to.replace('ž', 'z')
        # part_to = part_to.replace('š', 's')

        if part_to not in self.distances.keys():
            self.distances[part_to] = self.collect_data(part_to)

        print('\t' + str(self.distances[part_to]) + ' m')
        return self.distances[part_to]

    # noinspection PyTypeChecker
    def prepare_data(self):
        connection = None
        try:
            connection = DataBase.open_connection()

            for_sale_query = "select * from real_estate where " \
                             "type = 1 and sell_or_rent = 1 and city = 'Beograd' " \
                             "and part_of_city is not null " \
                             "and size is not null " \
                             "and year_built is not null " \
                             "and num_of_rooms is not null " \
                             "and floor is not null " \
                             "and price is not null;" \

            data = pd.read_sql(for_sale_query, connection)
            data['distance'] = data.apply(lambda row: self.get_distance(row['part_of_city']), axis=1)
            data = data.filter(items=['distance', 'size', 'year_built', 'num_of_rooms', 'floor', 'price'])

            # a few parameters set to non-default value
            data.to_csv(path_or_buf=r'data.csv', sep=',', na_rep='',
                                  float_format=None, columns=None, header=True,
                                  index=False, index_label=None, mode='w', encoding=None,
                                  compression='infer', quoting=None, quotechar='"',
                                  line_terminator=None, chunksize=None, date_format=None,
                                  doublequote=True, escapechar=None, decimal='.',
                                  errors='strict', storage_options=None)
            self.dataframe = data
        except (Exception, pyodbc.DatabaseError) as error:
            print("Error: ", error)
        finally:
            # closing database connection.
            if connection:
                connection.close()
