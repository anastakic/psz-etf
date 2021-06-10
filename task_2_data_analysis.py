import pyodbc
import csv
from task_1_fill_database import DataBase

SERVER = 'localhost'
DATABASE = 'psz_db'
USERNAME = 'ana'
PASSWORD = 'VeryStrongPassword1.'


class DataAnalysis:

    def start(self):
        print('TASK 2 STARTED...')

        self.do_analysis()

        print('TASK 2 FINISHED!')
        print('****************')

    @staticmethod
    def task_a(cursor):
        query = 'select count(*) as `total offers`, offer_type from `realty` group by offer_type;'
        cursor.execute(query)
        with open("task_2_analysis/A_count_by_type_offer.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_b(cursor):
        query = 'select count(*) as `total offers`, city from `realty` group by city order by 1 desc;'
        cursor.execute(query)
        with open("task_2_analysis/B_count_offers_by_city.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_c(cursor):
        query = "select count(*) as `total offers`, 'uknjižen' as `registered` from realty where registered = 1 and `type` = '{}' " \
                "union " \
                "select count(*), 'neuknjižen' from realty where registered = 0 and `type` = '{}';"

        cursor.execute(query.format('stan', 'stan'))
        with open("task_2_analysis/C_count_offers_by_type_apartment.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        cursor.execute(query.format('kuca', 'kuca'))
        with open("task_2_analysis/C_count_offers_by_type_house.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_d(cursor):
        query = "select * from realty where type = '{}' order by price desc limit 30;"

        cursor.execute(query.format('stan'))
        with open("task_2_analysis/D_top_30_most_expensive_apartments.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        cursor.execute(query.format('kuca'))
        with open("task_2_analysis/D_top_30_most_expensive_houses.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_e(cursor):
        query = "select * from realty where type = '{}' order by square_meters desc limit 100;"

        cursor.execute(query.format('stan'))
        with open("task_2_analysis/E_top_100_biggest_apartments.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        cursor.execute(query.format('kuca'))
        with open("task_2_analysis/E_top_100_biggest_houses.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_f(cursor):
        query = "select * from realty where offer_type = '{}' and year_built = 2021 order by price desc;"

        cursor.execute(query.format('prodaja'))
        with open("task_2_analysis/F_built_in_2020_sell.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        cursor.execute(query.format('izdavanje'))
        with open("task_2_analysis/F_built_in_2020_rent.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_g(cursor):
        query = 'select * from realty order by total_rooms desc limit 30;'
        cursor.execute(query)
        with open("task_2_analysis/G_offers_by_total_rooms.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        query = "select * from realty where `type` = 'stan' order by square_meters desc limit 30;"
        cursor.execute(query)
        with open("task_2_analysis/G_offers_by_size_apartments.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        query = "select * from realty where `type` = 'kuca' order by land_area desc limit 30;"
        cursor.execute(query)
        with open("task_2_analysis/G_offers_by_land_area_size.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def do_analysis():
        connection = cursor = None
        try:
            connection = DataBase.open_connection()
            cursor = connection.cursor()

            DataAnalysis.task_a(cursor)
            DataAnalysis.task_b(cursor)
            DataAnalysis.task_c(cursor)
            DataAnalysis.task_d(cursor)
            DataAnalysis.task_e(cursor)
            DataAnalysis.task_f(cursor)
            DataAnalysis.task_g(cursor)

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error: ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
