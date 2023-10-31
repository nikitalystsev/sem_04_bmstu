import numpy as np
import copy as cp
import matplotlib.pyplot as plt

from PointClass import Point


class DiffEquSweep:
    """
    Класс для нахождения приближенного решения дифференциального
    уравнения, используя разностную сетку и решением системы методом прогонки
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """

        """
        имеется уравнение:
        y" - y^3 = x^2
        x = 0, y = 1
        x = 1, y = 3
        """

        """
        Порядок решения: 
        1. Вводим разностную сетку, как множество равноотстоящих точек на оси x (узлов)
        2. Аппроксимируем вторую производную разностным аналогом
        Полученную систему нелинейных уравнений решаем методом Ньютона. В качестве начального приближения
        yn(0), n  = 0,1,…,N, целесообразно принять функцию, удовлетворяющую краевым условиям.
        """

        # Вводим разностную сетку
        self._n: int = 5  # число разбиений (условно)
        self._m = self._n + 1  # число узлов

        self._start_point: Point = Point(x=0, y=1)  # первая краевая точка
        self._end_point: Point = Point(x=1, y=3)  # последняя краевая точка

        self._h: float = (self._end_point.x - self._start_point.x) / self._n  # шаг разбиения

        # как множество равноотстоящих точек на оси x
        self._x_n: np.ndarray = np.array([n * self._h for n in range(self._n + 1)])  # до self._n включительно

        # вектор решений, то есть значения функции в узлах
        self._vector_solve: np.ndarray = np.array(0)

        """
        В данном случае переменными будут являться y0, y1, …,yN
        """

    @staticmethod
    def __input_eps() -> float:
        """
        Метод, позволяющий ввести точность вычисления
        """

        return float(input("\nВведите требуемую точность: "))

    @staticmethod
    def __f0(x: int | float):
        """
        Функция, которая удовлетворяет краевым условиям и является начальным приближением
        """

        return 2 * x + 1

    def __f_n(self, y_var: np.ndarray, x_n: int | float):
        """
        Метод позволяет получить значение строки системы уравнений
        x_n - не неизвестная переменная, передается как параметр для понимания, какой
        именно x брать из множества равноотстоящих точек
        """
        y_n_minus_1, y_n, y_n_plus_1 = y_var

        f_y_s = y_n_minus_1 - 2 * y_n + y_n_plus_1 - self._h ** 2 * (y_n ** 3 + x_n ** 2)

        return f_y_s

    def __f(self, y_s: np.ndarray[int | float]):
        """
        Метод, ака невязка, ака замена переменных для метода Ньютона
        """
        f_y_s = list()

        # это обработка первых self._n - 1 строк системы, без учета краевых условий
        for i in range(1, self._n):
            y_var = np.array([y_s[i - 1], y_s[i], y_s[i + 1]])

            value = self.__f_n(y_var, self._x_n[i])

            f_y_s.append(value)

        # краевые условия
        f_y_s.append(0)
        f_y_s.append(0)

        return np.array(f_y_s)

    def __solve_by_sweep(self, y_var0: np.ndarray[int | float]):
        """
        Метод позволяет получить решение системы методом Ньютона
        """
        # тут лежат значения функции self.__f0 на каждом узле
        self._vector_solve = y_var0
        count_iter = 0

        for _ in range(self._n + 1):
            ksi: list = [0 for _ in range(self._n)]
            et: list = [0 for _ in range(self._n)]

            for i in range(1, len(ksi)):
                a_n = 1
                c_n = 1

                b_n = a_n + c_n + 3 * self._h ** 2 * self._vector_solve[i] - \
                    self._h ** 2 * (self._x_n[i] ** 2 + self._vector_solve[i] ** 3)

                f = self._vector_solve[i - 1] - 2 * self._vector_solve[i] + self._vector_solve[i + 1] - \
                    self._h ** 2 * (self._x_n[i] ** 2 + self._vector_solve[i] ** 3)

                ksi[i] = c_n / (b_n - a_n * ksi[i - 1])
                et[i] = (a_n * et[i - 1] + f) / (b_n - a_n * ksi[i - 1])

            delta_y: list = [0 for _ in range(self._n + 1)]
            for i in range(len(ksi) - 1, 0, -1):
                delta_y[i] = ksi[i] * delta_y[i + 1] + et[i]

            for i in range(len(self._vector_solve)):
                self._vector_solve[i] = self._vector_solve[i] + delta_y[i]

        return count_iter

    def get_solve_and_plot(self):
        """
        Метод позволяет получить решение краевой задачи
        """
        y_var0 = list()  # список значений функции по всем узлам из self._x_n

        for x in self._x_n:
            y0_x = self.__f0(x)  # получаем значение из функции приближения
            y_var0.append(y0_x)

        y_var0 = np.array(y_var0)

        tmp_y_var0 = cp.deepcopy(y_var0)

        count_iter = self.__solve_by_sweep(y_var0)

        self.__print_solve(count_iter)

        plt.grid()
        plt.plot(self._x_n, tmp_y_var0, label="Значения функции приближения 2 * x + 1")
        plt.plot(self._x_n, self._vector_solve, label="Результирующая функция y(x)")
        plt.legend()
        plt.show()

    def __print_solve(self, count_iter: int) -> None:
        """
        Метод выводит результат - решение системы
        """
        if len(self._vector_solve) == 0:
            print(f"\nРешение системы нелинейных уравнений еще не было получено!")
            return

        print("\nРешение краевой задачи вида:")
        print(
            """
            { y" - y^3 = x^2
            { 0 <= x <= 1
            { x = 0, y = 1
            { x = 1, y = 3
            """
        )
        print(f"было успешно получено: ")

        print(f"Для вычисления корней системы потребовалось {count_iter} итераций")
