import pyodbc
import csv
from task_1_database_connection import DataBase

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
        query = 'select count(*) as `total offers`, sell_or_rent from `real_estate` group by sell_or_rent;'
        cursor.execute(query)
        with open("task_2_analysis/A_count_by_type_offer.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_b(cursor):
        query = 'select count(*) as `total offers`, city from `real_estate` group by city order by 1 desc;'
        cursor.execute(query)
        with open("task_2_analysis/B_count_offers_by_city.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_c(cursor):
        query = "select count(*) as `total offers`, 'uknjižen' as `is_registered` from real_estate where is_registered = 1 and `type` = '{}' " \
                "union " \
                "select count(*), 'neuknjižen' from real_estate where is_registered = 0 and `type` = '{}';"

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
        query = "select * from real_estate where type = {} order by price desc limit 30;"

        # for apartments type is set to 1
        cursor.execute(query.format('1'))
        with open("task_2_analysis/D_top_30_most_expensive_apartments.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        # for houses type is set to 0
        cursor.execute(query.format('0'))
        with open("task_2_analysis/D_top_30_most_expensive_houses.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_e(cursor):
        query = "select * from real_estate where type = {} order by size desc limit 100;"

        # for apartments type is set to 1
        cursor.execute(query.format('1'))
        with open("task_2_analysis/E_top_100_biggest_apartments.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        # for houses type is set to 0
        cursor.execute(query.format('0'))
        with open("task_2_analysis/E_top_100_biggest_houses.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_f(cursor):
        query = "select * from real_estate where sell_or_rent = {} and year_built = 2021 order by price desc;"

        # for sell column sell_or_rent has value 1
        cursor.execute(query.format('1'))
        with open("task_2_analysis/F_built_in_2020_sell.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        # for rent column sell_or_rent has value 0
        cursor.execute(query.format('0'))
        with open("task_2_analysis/F_built_in_2020_rent.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

    @staticmethod
    def task_g(cursor):
        query = 'select * from real_estate order by num_of_rooms desc limit 30;'
        cursor.execute(query)
        with open("task_2_analysis/G_offers_by_total_rooms.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        query = "select * from real_estate where `type` = 1 order by size desc limit 30;"
        cursor.execute(query)
        with open("task_2_analysis/G_offers_by_size_apartments.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        query = "select * from real_estate where `type` = 0 order by land_size desc limit 30;"
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
