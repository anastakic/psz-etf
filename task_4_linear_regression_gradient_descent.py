import numpy as np


class MultipleLinearRegression:

    def __init__(self, alpha=0.01, iteration_num=1000):
        self.alpha = alpha
        self.iterations = iteration_num
        self.weight_params = None
        self.w0 = None

    @staticmethod
    def check_attributes(X, Y):
        for x in X:
            if not all(isinstance(attr, (int, float)) for attr in X[x]):
                raise Exception("Error: Invalid datatype for x{} attribute".format(x))
        if not all(isinstance(attr, (int, float)) for attr in Y):
            raise Exception("Error: Invalid datatype for y attribute")

        return len(X.columns), len(X)

    def fit_gradient_descent(self, X, Y):
        try:
            n, m = self.check_attributes(X, Y)

            self.w0 = 0.0
            self.weight_params = np.zeros(n)

            for _ in range(self.iterations):
                hypothesis = np.dot(X, self.weight_params) + self.w0

                temp_w0 = self.w0 - self.alpha * (1 / m) * np.sum(hypothesis - Y)
                temp_weight_params = self.weight_params - self.alpha * (1 / m) * np.dot(X.T, (hypothesis - Y))

                self.w0 = temp_w0
                self.weight_params = temp_weight_params

        except Exception as e:
            print(str(e))

    def predict(self, test):
        return self.w0 + np.dot(test, self.weight_params)
