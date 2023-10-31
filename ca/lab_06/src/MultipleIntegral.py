import numpy as np
import math as m

from DataClass import DataClass
from SplineInterpolation import SplineOneVar
from SimpsonIntegral import SimpsonIntegral
from GaussIntegral import GaussIntegral
from PointClass import Point
from NewtonInterpolation import NewtonOneVar

EPS = 1e-7


def float_equal(a: int | float, b: int | float):
    """
    Функция сравнивает вещественные числа
    """
    return abs(a - b) < EPS


class MultipleIntegral:
    """
    Класс для вычисления кратного интеграла
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self._data: DataClass = DataClass("../data/data_lab6.txt")

    @staticmethod
    def __g(x: int | float, y: int | float):
        """
        Область интегрирования
        """

        return x >= 0 and y >= 0 and (x + y) <= 1

    def __get_g_points(self, use_eta=False) -> list[Point]:
        """
        Метод позволяет отобрать из всей талицы точки, принадлежащие области G
        """
        g_points = list()

        for x in self._data.x:
            for y in self._data.y:
                if self.__g(x, y):
                    g_points.append(Point(x=x, y=y, z=self._data.table_value(x, y, use_eta=use_eta)))

        return g_points

    def __points_by_y(self, y: int | float) -> list[Point]:
        """
        Метод позволяет получить точки из области интегрирования, у которых одно и то же значение у,
        переданное в эту функцию как параметр
        """
        points = list()

        for point in self._g_points:
            if point.y == y:
                points.append(point)

        return points

    def __integral(self, use_eta=False) -> int | float:
        """
        Метод позволяет получить значение кратного интеграла
        """
        self._g_points: list[Point] = self.__get_g_points(use_eta=use_eta)

        y_s = np.unique(list(map(lambda p: p.y, self._g_points)))

        """
        пусть двумерная интерполяция по х
        это значит, что для каждого y будет выбираться количество x, соответствующее
        этому y, по всем этим x будет проводится (количество y) раз одномерных интерполяций
        а потом в конце один раз одномерная интерполяция по y c уже полученными интерполированными значениями функции
        """

        integrals_by_y = list()
        _y_s = list()

        for y in y_s:  # идем по каждому y
            points = self.__points_by_y(y)  # получаем точки, соответствующие этому y
            x_s_by_y = [p.x for p in points]  # получаем иксы, соответствующие этому y
            # получаем значения функции от 2-х переменных, соответствующие этому y
            f_xy_by_y = [p.z for p in points]

            if len(x_s_by_y) > 1:
                data_table = list(zip(x_s_by_y, f_xy_by_y))  # получили таблицу данных для интерполяции

                def func(_x: int | float):  # тут как раз количество y раз проводится одномерная интерполяция
                    result = m.exp(SplineOneVar(_x, data_table).spline_interp(0, 0, 0)) if use_eta else \
                        SplineOneVar(_x, data_table).spline_interp(0, 0, 0)
                    return result

                integr_simps = SimpsonIntegral(func, min(x_s_by_y), max(x_s_by_y), n=30).integral()

                integrals_by_y.append(integr_simps)
                _y_s.append(y)

        data_table = list(zip(_y_s, integrals_by_y))  # получили таблицу данных последней интерполяции

        def func(_y: int | float):  # тут как раз количество y раз проводится одномерная интерполяция
            return SplineOneVar(_y, data_table).spline_interp(0, 0, 0)

        return GaussIntegral(func, min(_y_s), max(_y_s), n=60).integral()

    def integral(self):
        """
        Метод обертка для вычисления интеграла и вывода результата на экран
        """
        result_integral = self.__integral(use_eta=False)

        print(f"Значение кратного интеграла = {result_integral}")
