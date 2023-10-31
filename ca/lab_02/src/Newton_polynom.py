import math as m
from dataClass import *

EPS = 1e-9


def float_equal(a, b):
    """
    Функция сравнивает числа с плавающей запятой
    """
    return m.fabs(a - b) < EPS


class Newton:
    """
    Полином Ньютона
    """

    def __init__(self, data: Data, n: int = 3):
        """
        Инициализация атрибутов класса
        """
        self.x = data.get_x()
        self.data_table = data.get_data_table()
        self.n = n
        self.diff_table = None
        self.config_points = list()
        self.res = None

    def get_table_value_for_x(self):
        """
        Функция ищет ближайшее к x табличное значение
        """
        diff = m.fabs(self.x - self.data_table[0].x)

        index = 0

        for ind, val in enumerate(self.data_table):
            if m.fabs(self.x - val.x) < diff:
                diff = m.fabs(self.x - val.x)
                index = ind

        return index

    def collect_config(self):
        """
        Функция собирает конфигурацию
        """
        index = self.get_table_value_for_x()

        left = right = index

        for i in range(self.n):
            if i % 2 == 0:
                if left == 0:
                    right += 1
                else:
                    left -= 1
            else:
                if right == len(self.data_table) - 1:
                    left -= 1
                else:
                    right += 1

        return self.data_table[left:right + 1]

    def get_diff_table(self):
        """
        Функция получает таблицу разделенных разностей
        для полиномов Ньютона
        """
        self.config_points = self.collect_config()

        count_points = len(self.config_points)

        self.diff_table = [[0] * count_points for _ in range(count_points)]

        for i in range(count_points):
            self.diff_table[i][0] = self.config_points[i].y

        for i in range(1, count_points):
            for j in range(i, count_points):
                self.diff_table[j][i] = \
                    (self.diff_table[j][i - 1] - self.diff_table[j - 1][i - 1]) / \
                    (self.config_points[j].x - self.config_points[j - i].x)

    def get_diagonal(self):
        """
        Функция получает нужные разделенные разности
        (находятся на главной диагонали)
        :return: список нужных разностей
        """
        diagonal = []

        for i in range(len(self.diff_table)):
            diagonal.append(self.diff_table[i][i])

        return diagonal

    def newton_polynom(self):
        """
        Функция строит полином Ньютона или Эрмита
        и вычисляет значение при фиксированном x
        """
        self.get_diff_table()

        diff = self.get_diagonal()

        self.res = diff[0]

        for i in range(1, self.n):
            p = diff[i]
            for j in range(i):
                p *= (self.x - self.config_points[j].x)
            self.res += p

    def derivative2_newton_polynom(self, x: float, eps: float):
        """
        Метод вычисляет вторую производную полинома Ньютона
        f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h^2
        где h - шаг дискретизации.
        """
        self.x = x + eps
        self.newton_polynom()
        res_plus_h = self.res

        self.x = x
        self.newton_polynom()
        res = self.res

        self.x = x - eps
        self.newton_polynom()
        res_minus_h = self.res

        return (res_plus_h - 2 * res + res_minus_h) / (eps ** 2)

    def print_newton_res(self):
        """
        Метод выводит результат интерполяции полиномом Ньютона
        """
        if self.res is None:
            print("Интерполяция еще не была произведена!")
            return

        print(f"Результат интерполяции полиномом Ньютона {self.n}-й степени: y = {self.res: <15.3f}\n")
