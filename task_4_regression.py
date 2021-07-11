import pyodbc
import math
import numpy as np
import pandas as pd

from task_4_linear_regression_gradient_descent import MultipleLinearRegression
from task_4_distance_calculation import DistanceCalculation
from task_1_database_connection import DataBase


class HelperMLR:

    def __init__(self):
        self.distances = dict()
        self.dc = DistanceCalculation()
        self.regression = None
        self.dataframe = None
        self.X_min = self.X_max = self.Y_min = self.Y_max = 0

    def get_distance(self, part_to):
        # potential problems (can be uncommented)
        # parentheses in url
        # if part_to.find('(') > 0:
        #    part_to = part_to[:part_to.find('(')]
        # special characters
        # part_to = part_to.replace('ž', 'z')
        # part_to = part_to.replace('š', 's')

        if part_to not in self.distances.keys():
            self.distances[part_to] = self.dc.collect_data(part_to)

        print('INFO', part_to.lower() + ':', str(self.distances[part_to]) + ' m')
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
                             "and price is not null;"

            data = pd.read_sql(for_sale_query, connection)
            data['distance'] = data.apply(lambda row: self.get_distance(row['part_of_city']), axis=1)
            data = data.filter(items=['distance', 'size', 'year_built', 'num_of_rooms', 'floor', 'price'])
            print(len(data))
            data.dropna(subset=['distance', 'size', 'year_built', 'num_of_rooms', 'floor', 'price'], inplace=True)
            print(len(data))

            # for few parameters changed default value
            data.to_csv(path_or_buf=r'data.csv', sep=',', na_rep='',
                        float_format=None, columns=None, header=True,
                        index=False, index_label=None, mode='w', encoding=None,
                        compression='infer', quoting=None, quotechar='"',
                        line_terminator=None, chunksize=None, date_format=None,
                        doublequote=True, escapechar=None, decimal='.',
                        errors='strict', storage_options=None)

        except (Exception, pyodbc.DatabaseError) as error:
            print("Error: ", error)
        finally:
            if connection:
                connection.close()

    @staticmethod
    def root_mean_squared_error(y_real_values, y_predicted_values):
        val = (y_real_values - y_predicted_values) ** 2
        return math.sqrt(sum(val.array) / len(val.array))

    def count_rmse(self, X1_train, X1_test, Y_train, Y_test, Y_min, Y_max):
        Y_train_predictions = self.regression.predict(X1_train)
        Y_test_predictions = self.regression.predict(X1_test)

        Y_train_predictions = self.un_normalize(Y_train_predictions, Y_min, Y_max)
        Y_test_predictions = self.un_normalize(Y_test_predictions, Y_min, Y_max)

        Y_train_real = self.un_normalize(Y_train, Y_min, Y_max)
        Y_test_real = self.un_normalize(Y_test, Y_min, Y_max)

        rmse_train = self.root_mean_squared_error(Y_train_real, Y_train_predictions)
        rmse_test = self.root_mean_squared_error(Y_test_real, Y_test_predictions)
        print("INFO RMSE training data set:", rmse_train)
        print("INFO RMSE testing data set:", rmse_test)

    @staticmethod
    def normalize(x, x_min, x_max):
        return ((x - x_min) * 2) / (x_max - x_min) - 1

    @staticmethod
    def un_normalize(x, x_min, x_max):
        return (x + 1) * (x_max - x_min) / 2 + x_min

    @staticmethod
    def split_data_set(df, test_size=0.2):
        # random order in data set
        shuffle_df = df.sample(frac=1)

        # define a size for training set
        train_size = int((1 - test_size) * len(df))

        # split dataset
        train_set = shuffle_df[:train_size]
        test_set = shuffle_df[train_size:]

        return train_set, test_set

    def predict_output_value(self, test):
        X = pd.DataFrame(test)
        X = np.amin(X)

        X = self.normalize(X, self.X_min, self.X_max)
        prediction_of_input = self.regression.predict(X)
        prediction = self.un_normalize(prediction_of_input, self.Y_min, self.Y_max)
        print('Prediction: ' + str(prediction))
        return prediction

    def start_linear_regression(self):
        # self.prepare_data()
        # read data
        self.dataframe = pd.read_csv('data.csv')
        df = self.dataframe

        # df.dropna(subset=['distance', 'size', 'year_built', 'num_of_rooms', 'floor', 'price'], inplace=True)
        # df.to_csv(path_or_buf=r'data.csv', header=True, index=False)

        Y = df['price'].astype(float)
        self.Y_min = np.amin(Y)
        self.Y_max = np.amax(Y)

        X1 = df[['distance', 'size', 'year_built', 'num_of_rooms', 'floor']].astype(float)
        self.X_min = np.amin(X1)
        self.X_max = np.amax(X1)

        # divide data to test and train sets
        df_train, df_test = self.split_data_set(df, test_size=0.2)

        Y_train = self.normalize(df_train['price'].astype(float), self.Y_min, self.Y_max)
        Y_test = self.normalize(df_test['price'].astype(float), self.Y_min, self.Y_max)

        X1_train = self.normalize(
            df_train[['distance', 'size', 'year_built', 'num_of_rooms', 'floor']].astype(float),
            self.X_min, self.X_max)
        X1_test = self.normalize(
            df_test[['distance', 'size', 'year_built', 'num_of_rooms', 'floor']].astype(float),
            self.X_min, self.X_max)

        # normalize values
        self.regression = MultipleLinearRegression(alpha=0.001, iteration_num=10000)

        # fit model using gradient descent
        self.regression.fit_gradient_descent(X1_train, Y_train)

        # calculate root mean squared error for both test and training sets
        # self.count_rmse(X1_train, X1_test, Y_train, Y_test, self.Y_min, self.Y_max)
