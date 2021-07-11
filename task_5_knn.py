import math
import bisect
import numpy as np


class kNN:
    def __init__(self, data_set):
        self.n = 0                  # number of attributes
        self.m = 0                  # number of data
        self.X = []                 # input attributes
        self.Y = []                 # single output parameter
        self.euclidean_dist = []    # array of calculated euclidean distance between x(i) and y(i)
        self.manhattan_dist = []    # array of calculated manhattan distance between x(i) and y(i)

        self.data_set = data_set
        self.k = math.ceil(math.sqrt(len(data_set)))

        # try:
        self.process_data()
        self.process_output()
        # except Exception as e:
        #    print(str(e))

    def process_data(self):
        data = self.data_set.to_dict(orient='list')

        self.X = dict(list(data.items())[:-1])
        self.Y = data[len(self.X)]

        self.n = len(self.X)
        self.m = len(self.X[0])

        self.check_attributes()

    def check_attributes(self):
        for x in self.X:
            if not all(isinstance(attr, (int, float)) for attr in self.X[x]):
                raise Exception("Error: Invalid datatype for x{} attribute".format(x))

    @staticmethod
    def classification(y):
        # class 1   <= 49 999 €
        # class 2   50 000 - 99 999 €
        # class 3   100 000 - 149 999 €
        # class 4   150 000 - 199 999 €
        # class 5   >= 200 000 €
        if y < 50000:
            return 1
        elif 50000 <= y <= 99999:
            return 2
        elif 100000 <= y <= 149999:
            return 3
        elif 150000 <= y <= 199999:
            return 4
        else:
            return 5

    @staticmethod
    def class_value(class_num):
        if class_num == 1:
            return "price less than 50.000,00 €"
        elif class_num == 2:
            return "price between 50.000,00 € and 99.999,00 €"
        elif class_num == 3:
            return "price between 100.000,00 € and 149.999,00 €"
        elif class_num == 4:
            return "price between 150.000,00 € and 199.999,00 €"
        elif class_num == 5:
            return "price larger than 200.000,00 €"

    def process_output(self):
        self.Y = [self.classification(y) for y in self.Y]

    def set_k(self, k):
        self.k = k

    def calculate_distances(self, test):
        # test array
        for j in range(self.m):
            euclidean = 0
            manhattan = 0

            for i in range(self.n):
                euclidean += (self.X[i][j] - float(test[i])) ** 2
                manhattan += abs(self.X[i][j] - float(test[i]))

            bisect.insort(self.euclidean_dist, (math.sqrt(euclidean), self.Y[j]))
            bisect.insort(self.manhattan_dist, (manhattan, self.Y[j]))

        # print(self.euclidean_dist)
        # print(self.manhattan_dist)

    def predict_euclidean(self):
        classes = np.array([dist[1] for dist in self.euclidean_dist[0:self.k]])
        class_num = np.bincount(classes).argmax()
        return class_num, self.class_value(class_num)

    def predict_manhattan(self):
        classes = np.array([dist[1] for dist in self.manhattan_dist[0:self.k]])
        class_num = np.bincount(classes).argmax()
        return class_num, self.class_value(class_num)

