import pyodbc
import numpy as np
import matplotlib.pyplot as plt  # pip install matplotlib

from task_1_database_connection import DataBase

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
    def show_visualization(df, path, title, bar_labels=None, bottom=0):
        if bar_labels is None:
            bar_labels = []
        x = []
        y = []
        x_label = y_label = ''

        print(df)

        for i, row in enumerate(df):
            if i == 0:
                x_label = row[0]
                y_label = row[1]
            else:
                x.append(row[0])
                y.append(int(row[1]))

        plt.figure(constrained_layout=True)
        for i, xx in enumerate(bar_labels):
            plt.text(i - .1, y[i] + 10, '{}%'.format(str(bar_labels[i])))
        plt.bar(x, y, color='g', width=0.5, label="Offer number", bottom=bottom)
        plt.xlabel(str(x_label))
        plt.xticks(rotation=75)
        plt.minorticks_on()
        plt.ylabel(str(y_label))
        plt.title(title)
        plt.legend(loc='best', fontsize=15)
        # plt.show()
        plt.savefig(path)
        plt.close()

    @staticmethod
    def show_visualization_two_charts(df, path, title):

        values_sell = []
        values_rent = []
        pct_sell = []
        pct_rent = []
        cities = []

        for i, row in enumerate(df):
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
        plt.savefig(path)
        plt.close()

    @staticmethod
    def task_a(cursor):
        query = "select part_of_city as `Part of Belgrade`, count(*) as `Total offers` from real_estate where city like 'Beograd' and part_of_city is not NULL group by part_of_city order by 2 desc limit 10;"
        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        df += cursor.fetchall()  # data

        DataVisualization.show_visualization(df, "task_3_visualization/A_top_10_parts_of_Belgrade",
                                             'top_10_parts_of_Belgrade')

    @staticmethod
    def task_b(cursor):
        query = \
            "select '<= 35 m²' as 'Size', count(*) as 'Total offers' from real_estate where size <= 35 and sell_or_rent = 1 and `type` = 1  " \
            "union select '36-50 m²', count(*) from real_estate where size > 35 and size <= 50 and sell_or_rent = 1 and `type` = 1 " \
            "union select '51-65 m²', count(*) from real_estate where size > 50 and size <= 65 and sell_or_rent = 1 and `type` = 1 " \
            "union select '66-80 m²', count(*) from real_estate where size > 65 and size <= 80 and sell_or_rent = 1 and `type` = 1 " \
            "union select '81-95 m²', count(*) from real_estate where size > 80 and size <= 95 and sell_or_rent = 1 and `type` = 1 " \
            "union select '96-110 m²', count(*) from real_estate where size > 95 and size <= 110 and sell_or_rent = 1 and `type` = 1 " \
            "union select '>= 111 m²', count(*) from real_estate where size >= 111 and sell_or_rent = 1 and `type` = 1;"

        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        df += cursor.fetchall()  # data

        DataVisualization.show_visualization(df, "task_3_visualization/B_offers_by_apartment_size",
                                             'offers_by_apartment_size')

    @staticmethod
    def task_c(cursor):
        # order by year
        query = \
            "select '1951-1960' as 'Decade', count(*) as 'Total built' from real_estate where year_built > 1950 and year_built <= 1960 " \
            "union select '1961-1970', count(*) from real_estate where year_built > 1960 and year_built <= 1970 " \
            "union select '1971-1980', count(*) from real_estate where year_built > 1970 and year_built <= 1980 " \
            "union select '1981-1990', count(*) from real_estate where year_built > 1980 and year_built <= 1990 " \
            "union select '1991-2000', count(*) from real_estate where year_built > 1990 and year_built <= 2000 " \
            "union select '2001-2010', count(*) from real_estate where year_built > 2000 and year_built <= 2010 " \
            "union select '2011-2020', count(*) from real_estate where year_built > 2010 and year_built <= 2020;"

        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        df += cursor.fetchall()  # data

        DataVisualization.show_visualization(df, "task_3_visualization/C_offers_by_build_year",
                                             'offers_by_build_year')

        # order by construction_type
        query = "select construction_type, count(*) as `total offers` from real_estate where construction_type is " \
                "not null group by construction_type order by construction_type;"

        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        df += cursor.fetchall()  # data

        DataVisualization.show_visualization(df, "task_3_visualization/C_offers_by_real_estate_state",
                                             'offers_by_real_estate_state')

    @staticmethod
    def task_d(cursor):
        query = \
            "with temp as " \
            "( " \
            "select count(*) as `Total`, city as `City` from real_estate group by city order by 1 desc limit 5 " \
            ") " \
            "select " \
            "t.city as `City`, " \
            "count(*) as `Sell`, " \
            "count(*)/t.`Total`*100 as `Sell pct.`, " \
            "t.`Total`-count(*) as `Rent`, " \
            "(t.`Total`-count(*))/`Total`*100 as `Rent pct.` " \
            "from real_estate r join temp t on r.city = t.city " \
            "where sell_or_rent = 1 group by t.city; "

        print(query)
        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        df += cursor.fetchall()  # data

        DataVisualization.show_visualization_two_charts(df, "task_3_visualization/D_top_5_cities_ratio",
                                                        'top_5_cities_ratio')

    @staticmethod
    def task_e(cursor):
        query = \
            "select '< 50k EUR' as `Price`, count(*) as `Total offers` from real_estate where sell_or_rent = 1 and price < 50000  " \
            "union select '50-100k EUR', count(*) from real_estate where sell_or_rent = 1 and price >= 50000 and price < 100000   " \
            "union select '100-150k EUR', count(*) from real_estate where sell_or_rent = 1 and price >= 100000 and price < 150000 " \
            "union select '150-200k EUR', count(*) from real_estate where sell_or_rent = 1 and price >= 150000 and price < 200000 " \
            "union select '> 200k EUR', count(*) from real_estate where sell_or_rent = 1 and price >= 200000;"

        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        total = 0
        data = cursor.fetchall()
        df += data  # data
        for i in data:
            total += int(i[1])
        bar_labels = [round(int(row[1]) / total * 100) for row in data]

        DataVisualization.show_visualization(df, "task_3_visualization/E_offers_number_by_price",
                                             'offers_number_by_price', bar_labels)

    @staticmethod
    def task_f(cursor):
        query = \
            "select 'With parking' as `real_estate in Belgrade`, count(*) as `Number of offers` " \
            "from real_estate where sell_or_rent = 1 and city = 'Beograd' and parking = 1 union " \
            "select 'Total real_estate', count(*) from real_estate where sell_or_rent = 1 and city = 'Beograd';"

        cursor.execute(query)

        df = [tuple(i[0] for i in cursor.description)]  # headers
        df += cursor.fetchall()  # data

        DataVisualization.show_visualization(df, "task_3_visualization/F_real_estate_in_Belgrade_with_parking",
                                             'real_estate_in_Belgrade_with_parking')

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
