import numpy as np
import copy as cp
import matplotlib.pyplot as plt

from PointClass import Point
from gauss import GaussMethod


class DiffEquNewton:
    """
    Класс для нахождения приближенного решения дифференциального
    уравнения, используя разностную сетку
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """

        """
        имеется уравнение y" - y^3 = x^2
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
        self._n: int = 4  # число разбиений (условно)
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

    @staticmethod
    def __get_slau_for_gauss(
            jacobian_matrix: np.ndarray,
            f_vector_var: np.ndarray
    ):
        """
        На каждой итерации метода Ньютона происходит решение системы уже линейных АУ
        А получать решение можно с помощью написанного мной же файла с методом Гаусса
        """
        slau = list()

        for i in range(len(jacobian_matrix)):
            tmp_row = list()
            tmp_row.extend(jacobian_matrix[i])
            tmp_row.append(f_vector_var[i])

            slau.append(tmp_row)

        return slau

    def __boundary_conditions(self, jacobian_matrix: list[list[int | float]]):
        """
        Побочный метод для получения частных производных по всем переменным
        в функциях краевых условий для матрицы Якоби
        """
        jacobian_row = list()  # строка матрицы Якоби

        jacobian_row.append(1)
        for i in range(1, self._n + 1):
            jacobian_row.append(0)

        jacobian_matrix.append(jacobian_row)

        jacobian_row = list()  # строка матрицы Якоби

        for i in range(1, self._n + 1):
            jacobian_row.append(0)
        jacobian_row.append(1)

        jacobian_matrix.append(jacobian_row)

        return jacobian_matrix

    def __jacobian_matrix(self, y_s: np.ndarray[int | float]) -> \
            np.ndarray[np.ndarray[int | float]]:
        """
        Метод позволяет получить матрицу Якоби для системы уравнений, заданной по тз
        """
        """
        Матрица Якоби - матрица частных производных, по столбцам идет распределение по всем неизвестным переменным,
        а по строкам по функциям
        В нашем случае, в каждой строке системы, по сути, одна и та же функция, но с разными переменными y0, y1, …,yN, 
        и эта функция есть функция, технически,  от трех переменных. Но мы берем частные производные этой функции про 
        всем переменным y0, y1, …,yN
        """
        jacobian_matrix = list()

        # это обработка первых self._n - 1 строк системы, без учета краевых условий
        # диапазон выбран верно, поскольку необходимо, чтобы i + 1 не превысил self._m - 1, или же self._n
        for i in range(1, self._n):

            jacobian_row = list()  # строка матрицы Якоби

            for j in range(len(y_s)):  # внутренний цикл по переменным
                if j != i - 1 and j != i and j != i + 1:
                    # если переменной нет среди аргументов функции,
                    # частная производная этой функции по этому аргументу равна нулю
                    jacobian_row.append(0)
                elif j == i - 1:
                    # если переменная является первым аргументом функции,
                    # то частная производная этой функции по этому аргументу равна единице
                    jacobian_row.append(1)
                elif j == i:
                    # если переменная является вторым аргументом функции,
                    # то частная производная этой функции по этому аргументу равна value
                    value = -2 - self._h ** 2 * (3 * y_s[j] ** 2)
                    jacobian_row.append(value)
                elif j == i + 1:
                    # если переменная является третьим аргументом функции,
                    # то частная производная этой функции по этому аргументу равна единице
                    jacobian_row.append(1)

            jacobian_matrix.append(jacobian_row)

        jacobian_matrix = self.__boundary_conditions(jacobian_matrix)  # обработка краевых условий

        jacobian_matrix = np.array(jacobian_matrix)

        return jacobian_matrix

    @staticmethod
    def __check_delta(dx: np.ndarray[int | float], eps: float):
        """
        Метод позволяет вычислить точность вычислений
        """
        abs_dx = np.absolute(dx)

        if max(abs_dx) <= eps:
            return True

        return False

    def __solve_by_newton(self, y_var0: np.ndarray[int | float], eps: float):
        """
        Метод позволяет получить решение системы методом Ньютона
        """
        # тут лежат значения функции self.__f0 на каждом узле
        self._vector_solve = y_var0
        count_iter = 0

        condition = True

        while condition:
            f_y_s = self.__f(self._vector_solve)
            j_y_s = self.__jacobian_matrix(self._vector_solve)

            slau = self.__get_slau_for_gauss(j_y_s, -f_y_s)

            dx = GaussMethod(slau).gauss()
            dx = np.array(dx)

            # dx = np.linalg.solve(j_y_s, -f_y_s)

            self._vector_solve += dx

            count_iter += 1

            if self.__check_delta(dx, eps):
                condition = False

            # if np.linalg.norm(dx) < eps:
            #     break

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

        eps = self.__input_eps()

        count_iter = self.__solve_by_newton(y_var0, eps)

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
