import pyodbc
import csv
import matplotlib.pyplot as plt  # pip install matplotlib
from matplotlib import ticker
import numpy as np

from task_1_fill_database import DataBase

SERVER = 'localhost'
DATABASE = 'psz_db'
USERNAME = 'ana'
PASSWORD = 'VeryStrongPassword1.'


class DataVisualization:

    def start(self):
        print('TASK 3 STARTED...')

        DataVisualization.do_visualization()

        print('TASK 3 FINISHED!')
        print('****************')

    @staticmethod
    def show_visualization(file, title, bar_labels=[], bottom=0):
        x = []
        y = []
        x_label = y_label = ''

        with open(file, 'r') as csv_file:
            plots = csv.reader(csv_file)

            for i, row in enumerate(plots):
                if i == 0:
                    x_label = row[0]
                    y_label = row[1]
                else:
                    x.append(row[0])
                    y.append(int(row[1]))

        plt.figure(constrained_layout=True)
        for i, xx in enumerate(bar_labels):
            plt.text(i-.1, y[i]+10, '{}%'.format(str(bar_labels[i])))
        plt.bar(x, y, color='g', width=0.5, label="Offer number", bottom=bottom)
        plt.xlabel(str(x_label))
        plt.xticks(rotation=75)
        plt.minorticks_on()
        plt.ylabel(str(y_label))
        plt.title(title)
        plt.legend(loc='best', fontsize=15)
        # plt.show()
        plt.savefig(file[:-4])
        plt.close()

    @staticmethod
    def show_visualization_two_charts(file, title, bottom=0):

        values_sell = []
        values_rent = []
        pct_sell = []
        pct_rent = []
        cities = []

        with open(file, 'r') as csv_file:
            plots = csv.reader(csv_file)

            for i, row in enumerate(plots):
                if i > 0:
                    values_sell.append(int(row[1]))
                    values_rent.append(int(row[3]))
                    pct_sell.append(round(float(row[2])))
                    pct_rent.append(round(float(row[4])))
                    cities.append(row[0])

        x = np.arange(len(cities))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        ax.bar(x - width / 2, values_sell, width, label='Sell', color='g')
        ax.bar(x + width / 2, values_rent, width, label='Rent', color='y')

        for i, xx in enumerate(pct_rent):
            plt.text(i - .35, values_sell[i] + 10, '{}%'.format(str(pct_sell[i])))
            plt.text(i + .05, values_rent[i] + 10, '{}%'.format(str(pct_rent[i])))

        ax.set_xlabel('Cities')
        ax.set_ylabel('Offer number')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(cities)
        ax.legend(loc='best', fontsize=15)

        fig.tight_layout()
        plt.savefig(file[:-4])
        plt.close()

    @staticmethod
    def task_a(cursor):
        query = "select quarter as `Part of Belgrade`, count(*) as `Total offers` from realty where city like 'Beograd' and quarter is not NULL group by quarter order by 2 desc limit 10;"
        cursor.execute(query)
        with open("task_3_visualization/A_top_10_Belgrade_quarters.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        DataVisualization.show_visualization("task_3_visualization/A_top_10_Belgrade_quarters.csv",
                                             'top_10_Belgrade_quarters')

    @staticmethod
    def task_b(cursor):
        query = \
            "select '<= 35 m²' as 'Size', count(*) as 'Total offers' from realty where square_meters <= 35 and offer_type = 'prodaja' and `type` = 'stan'  " \
            "union select '36-50 m²', count(*) from realty where square_meters > 35 and square_meters <= 50 and offer_type = 'prodaja' and `type` = 'stan' " \
            "union select '51-65 m²', count(*) from realty where square_meters > 50 and square_meters <= 65 and offer_type = 'prodaja' and `type` = 'stan' " \
            "union select '66-80 m²', count(*) from realty where square_meters > 65 and square_meters <= 80 and offer_type = 'prodaja' and `type` = 'stan' " \
            "union select '81-95 m²', count(*) from realty where square_meters > 80 and square_meters <= 95 and offer_type = 'prodaja' and `type` = 'stan' " \
            "union select '96-110 m²', count(*) from realty where square_meters > 95 and square_meters <= 110 and offer_type = 'prodaja' and `type` = 'stan' " \
            "union select '>= 111 m²', count(*) from realty where square_meters >= 111 and offer_type = 'prodaja' and `type` = 'stan';"

        cursor.execute(query)
        with open("task_3_visualization/B_offers_by_apartment_size.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        DataVisualization.show_visualization("task_3_visualization/B_offers_by_apartment_size.csv",
                                             'offers_by_apartment_size')

    @staticmethod
    def task_c(cursor):
        query = \
            "select '1951-1960' as 'Decade', count(*) as 'Total built' from realty where year_built > 1950 and year_built <= 1960 " \
            "union select '1961-1970', count(*) from realty where year_built > 1960 and year_built <= 1970 " \
            "union select '1971-1980', count(*) from realty where year_built > 1970 and year_built <= 1980 " \
            "union select '1981-1990', count(*) from realty where year_built > 1980 and year_built <= 1990 " \
            "union select '1991-2000', count(*) from realty where year_built > 1990 and year_built <= 2000 " \
            "union select '2001-2010', count(*) from realty where year_built > 2000 and year_built <= 2010 " \
            "union select '2011-2020', count(*) from realty where year_built > 2010 and year_built <= 2020;"

        cursor.execute(query)
        with open("task_3_visualization/C_offers_by_build_year.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        DataVisualization.show_visualization("task_3_visualization/C_offers_by_build_year.csv", 'offers_by_build_year')

    @staticmethod
    def task_d(cursor):
        query = \
            "with temp as (" \
            "select city as `City`, " \
            "	(select count(*) from realty where offer_type = 'prodaja' and city = r.city) as `Sell`, " \
            "	(select count(*) from realty where offer_type = 'izdavanje' and city = r.city) as `Rent`," \
            "	(select count(*) from realty where city = r.city) as `Total`" \
            "from realty r group by city order by 4 desc limit 5" \
            ")" \
            "select `City`, `Sell`, `Sell`/`Total`*100 as `Sell pct.`, `Rent`, `Rent`/`Total`*100 as `Rent pct.` from temp;"

        cursor.execute(query.format('stan'))
        with open("task_3_visualization/D_top_5_cities_ratio.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        DataVisualization.show_visualization_two_charts("task_3_visualization/D_top_5_cities_ratio.csv", 'top_5_cities_ratio')

    @staticmethod
    def task_e(cursor):
        query = \
            "select '< 50k EUR' as `Price`, count(*) as `Total offers` from realty where offer_type = 'prodaja' and price < 50000  " \
            "union select '50-100k EUR', count(*) from realty where offer_type = 'prodaja' and price >= 50000 and price < 100000   " \
            "union select '100-150k EUR', count(*) from realty where offer_type = 'prodaja' and price >= 100000 and price < 150000 " \
            "union select '150-200k EUR', count(*) from realty where offer_type = 'prodaja' and price >= 150000 and price < 200000 " \
            "union select '> 200k EUR', count(*) from realty where offer_type = 'prodaja' and price >= 200000;" \

        cursor.execute(query)
        with open("task_3_visualization/E_offers_number_by_price.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            total = 0
            data = cursor.fetchall()
            for i in data:
                total += int(i[1])
            bar_labels = [round(int(row[1])/total * 100) for row in data]
            print(bar_labels)
            csv_writer.writerows(data)

        DataVisualization.show_visualization("task_3_visualization/E_offers_number_by_price.csv", 'offers_number_by_price', bar_labels)

    @staticmethod
    def task_f(cursor):
        query = \
            "select 'With parking' as `Realty in Belgrade`, count(*) as `Number of offers` " \
            "from realty where offer_type = 'prodaja' and city = 'Beograd' and parking = 'Da' union " \
            "select 'Total realty', count(*) from realty where offer_type = 'prodaja' and city = 'Beograd';"

        cursor.execute(query)
        with open("task_3_visualization/F_realty_in_Belgrade_with_parking.csv", "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        DataVisualization.show_visualization("task_3_visualization/F_realty_in_Belgrade_with_parking.csv", 'realty_in_Belgrade_with_parking')

    @staticmethod
    def do_visualization():
        connection = cursor = None
        try:
            connection = DataBase.open_connection()
            cursor = connection.cursor()

            DataVisualization.task_a(cursor)
            DataVisualization.task_b(cursor)
            DataVisualization.task_c(cursor)
            DataVisualization.task_d(cursor)
            DataVisualization.task_e(cursor)
            DataVisualization.task_f(cursor)

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error: ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
