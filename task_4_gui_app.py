import pandas as pd
from tkinter import *
from task_4_regression import HelperMLR
from task_5_knn import kNN

REGRESSION = 0
KNN = 1

EUCLIDEAN = 0
MANHATTAN = 1


class LinearRegressionApp:

    def __init__(self):
        self.regression = HelperMLR()
        self.regression.start_linear_regression()
        self.window = Tk()
        self.mode = REGRESSION          # linear regression as default mode

        self.knn_dist = IntVar()
        self.knn_dist.set(EUCLIDEAN)    # for kNN use euclidean distance as default

        self.background = '#55aaff'
        self.inputs = []
        self.buttons = []
        self.k_param = 1
        self.k_input = None
        self.k_label = None
        self.kNN_euclidean = None
        self.kNN_manhattan = None
        self.window_settings()
        self.set_title('Apartments in Belgrade')
        self.set_padding(1)
        self.set_labels()
        self.set_inputs()
        self.add_button_reg('Linear Regression')
        self.add_button_knn('kNN algorithm')
        self.set_padding(11)
        self.add_submit('Run')
        self.set_padding(13)
        self.message = self.set_message()
        self.start_app()

    def start_app(self):
        self.window.mainloop()

    def window_settings(self, bgd='#55aaff'):
        self.background = bgd
        self.window.configure(background=bgd)

    def set_title(self, title):
        self.window.title(title)

    def set_padding(self, row, text=''):
        Label(self.window, text=text, background=self.background, width='30').\
            grid(row=row, column=0, pady=5)

    def set_labels(self):
        self.add_label('Distance from center [m]', 2, 0)
        self.add_label('Apartment size [m²]', 3, 0)
        self.add_label('Year built', 4, 0)
        self.add_label('Number of rooms', 5, 0)
        self.add_label('Floor number', 6, 0)
        self.set_padding(7)
        self.k_label = self.add_label('Set K manually (uses default value if empty)', 9, 0, '#777777')

    def set_inputs(self):
        for i in range(2, 7):
            self.add_input(i, 1)
        self.set_knn_inputs()

    def set_knn_inputs(self):
        entry_var = StringVar()
        self.k_input = Entry(self.window, textvariable=entry_var, width=30)
        self.k_input.grid(row=9, column=1, padx=5, pady=5)
        self.k_input.configure(disabledbackground='#aeb4bd', state='disable')

        self.k_param = entry_var
        self.kNN_euclidean = Radiobutton(self.window, text='Euclidean distance',
                                         bg=self.background, activebackground=self.background,
                                         variable=self.knn_dist, value=EUCLIDEAN)
        self.kNN_manhattan = Radiobutton(self.window, text='Manhattan distance',
                                         bg=self.background, activebackground=self.background,
                                         variable=self.knn_dist, value=MANHATTAN)
        self.kNN_euclidean.grid(row=10, column=0)
        self.kNN_manhattan.grid(row=10, column=1)
        self.kNN_euclidean.select()

        self.kNN_euclidean.configure(state='disable')
        self.kNN_manhattan.configure(state='disable')

    def add_label(self, title, row, column, text_color='black'):
        label = Label(self.window, text=title, background=self.background, foreground=text_color)
        label.grid(row=row, column=column, padx=15, pady=5)
        return label

    def add_input(self, row, column):
        entry_var = StringVar()
        Entry(self.window, textvariable=entry_var, width=30).grid(row=row, column=column, padx=5, pady=5)
        self.inputs.append(entry_var)

    def add_button_reg(self, title):
        btn = Button(self.window, text=title, command=self.run_reg, bg='#55aaff', activebackground='#4444ff',
                     fg="white", width=30, borderwidth=0, pady=8, foreground="white", font=15)
        btn.grid(row=0, column=0)
        self.buttons.append(btn)

    def add_button_knn(self, title):
        btn = Button(self.window, text=title, command=self.run_knn, bg='#18297e', activebackground='#4444ff',
                     fg="white", width=30, borderwidth=0, pady=8, foreground="white", font=15)
        btn.grid(row=0, column=1)
        self.buttons.append(btn)

    def add_submit(self, title):
        btn = Button(self.window, text=title, command=self.check_inputs, bg='#18297e', activebackground='#4444ff',
                     fg="white", width=20, borderwidth=0, pady=5, foreground="white")
        btn.grid(row=12, column=1)
        self.buttons.append(btn)

    def set_message(self, color='#aa0000'):
        err = Label(self.window, text='', background=self.background, foreground=color, font=15)
        err.grid(row=13, columnspan=2, padx=15, pady=15)
        return err

    def check_inputs(self):
        if len(self.inputs) > 0:
            for i in self.inputs:
                if i.get() == '' or not str(i.get()).isdigit():
                    self.message.configure(text='Invalid field values!', foreground='#aa0000')
                    return False
            self.message.configure(text=" ")
            try:
                df = pd.read_csv('data.csv')
                df = df[['distance', 'size', 'year_built', 'num_of_rooms', 'floor', 'price']].astype(float)
                df.columns = range(df.shape[1])

                test = [float(val.get()) for val in self.inputs]
                if self.mode == REGRESSION:
                    data = dict(distance=[test[0]],
                                size=[test[1]],
                                year_built=[test[2]],
                                num_of_rooms=[test[3]],
                                floor=[test[4]])
                    self.message.configure(
                        text="Predicted price {} €.".format(self.regression.predict_output_value(data)),
                        foreground='green'
                    )

                elif self.mode == KNN:
                    knn = kNN(df)

                    # if parameter K is manually set
                    if self.k_input.get() != '' and str(self.k_input.get()).isdigit():
                        knn.set_k(int(self.k_input.get()))

                    # does calculations for both metrics
                    knn.calculate_distances(test)

                    if self.knn_dist.get() == EUCLIDEAN:
                        class_num, class_name = knn.predict_euclidean()
                        self.message.configure(text="Class: {}, {}.".format(class_num, class_name), foreground='green')

                    elif self.knn_dist.get() == MANHATTAN:
                        class_num, class_name = knn.predict_manhattan()
                        self.message.configure(text="Class: {}, {}.".format(class_num, class_name), foreground='green')

            except Exception as e:
                self.message.configure(text=str(e), foreground='#aa0000')

    def run_reg(self):
        self.buttons[KNN].configure(bg='#18297e')
        self.buttons[REGRESSION].configure(bg='#55aaff')
        self.mode = REGRESSION

        # if mode is REGRESSION disable input fields for kNN
        self.k_input.configure(disabledbackground='#aeb4bd', state='disable')
        self.kNN_euclidean.configure(state='disable')
        self.kNN_manhattan.configure(state='disable')
        self.k_label.configure(foreground='#777777')

    def run_knn(self):
        self.buttons[KNN].configure(bg='#55aaff')
        self.buttons[REGRESSION].configure(bg='#18297e')
        self.mode = KNN

        # if mode is kNN enable input fields for kNN
        self.k_input.configure(state='normal')
        self.kNN_euclidean.configure(state='normal')
        self.kNN_manhattan.configure(state='normal')
        self.k_label.configure(foreground='black')


if __name__ == '__main__':
    window = LinearRegressionApp()
