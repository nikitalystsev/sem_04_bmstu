import math as m

EPS = 1e-9


def float_equal(a, b):
    """
    Функция сравнивает числа с плавающей запятой
    """
    return m.fabs(a - b) < EPS


class NewtonOneVar:
    """
    Полином Ньютона
    """

    def __init__(
            self,
            x: int | float,
            data_table: list[tuple[int | float, int | float]],
            n: int
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.x: int | float = x
        self.data_table: list[tuple[int | float, int | float]] = data_table
        self.n: int = n
        self.diff_table = None
        self.config_points = list()
        self.res = None

    def get_table_value_for_x(self) -> int:
        """
        Функция ищет ближайшее к x табличное значение
        """
        diff = m.fabs(self.x - self.data_table[0][0])

        index = 0

        for ind, val in enumerate(self.data_table):
            if m.fabs(self.x - val[0]) < diff:
                diff = m.fabs(self.x - val[0])
                index = ind

        return index

    def collect_config(self) -> list[tuple[int | float, int | float]]:
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

        print(f"Конфигурация по X:", self.data_table[left:right + 1])

        return self.data_table[left:right + 1]

    def get_diff_table(self) -> None:
        """
        Функция получает таблицу разделенных разностей
        для полиномов Ньютона
        """
        self.config_points = self.collect_config()

        count_points = len(self.config_points)

        self.diff_table = [[0] * count_points for _ in range(count_points)]

        for i in range(count_points):
            self.diff_table[i][0] = self.config_points[i][1]

        for i in range(1, count_points):
            for j in range(i, count_points):
                self.diff_table[j][i] = \
                    (self.diff_table[j][i - 1] - self.diff_table[j - 1][i - 1]) / \
                    (self.config_points[j][0] - self.config_points[j - i][0])

    def get_diagonal(self) -> list:
        """
        Функция получает нужные разделенные разности
        (находятся на главной диагонали)
        :return: список нужных разностей
        """
        diagonal = []

        for i in range(len(self.diff_table)):
            diagonal.append(self.diff_table[i][i])

        return diagonal

    def newton_polynom(self) -> int | float:
        """
        Функция строит полином Ньютона
        и вычисляет значение при фиксированном x
        """
        self.get_diff_table()

        diff = self.get_diagonal()

        self.res = diff[0]

        for i in range(1, len(diff)):
            p = diff[i]
            for j in range(i):
                p *= (self.x - self.config_points[j][0])
            self.res += p

        return self.res


class NewtonTwoVar:
    """
    Класс для интерполяции полиномом ньютона функции от 2-х переменных
    """

    def __init__(
            self,
            x: int | float, y: int | float,
            x_s: list[int | float],
            y_s: list[int | float],
            values: list[list[int | float]],
            nx: int,
            ny: int
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        # точка интерполирования
        self.x: int | float = x
        self.y: int | float = y

        # значения
        self.x_s: list[int | float] = x_s
        self.y_s: list[int | float] = y_s
        self.values: list[list[int | float]] = values

        # степени полиномов
        self.nx: int = nx
        self.ny: int = ny

        self.res = None

    # пусть двумерная интерполяция по x
    def get_table_value_for_y(self) -> int:
        """
        Функция ищет ближайшее к y табличное значение
        """
        diff = m.fabs(self.y - self.y_s[0])

        index = 0

        for ind, y in enumerate(self.y_s):
            if m.fabs(self.y - y) < diff:
                diff = m.fabs(self.y - y)
                index = ind

        return index

    def collect_config(self) -> list[int]:
        """
        Функция собирает конфигурацию по y
        """
        index = self.get_table_value_for_y()

        left = right = index

        for i in range(self.ny):
            if i % 2 == 0:
                if left == 0:
                    right += 1
                else:
                    left -= 1
            else:
                if right == len(self.y_s) - 1:
                    left -= 1
                else:
                    right += 1

        print(f"Конфигурация по Y:", list(range(left, right + 1)))

        return list(range(left, right + 1))

    def __get_data_table_for_newton_one_var(
            self,
            ind_y: int
    ) -> list[tuple[int | float, int | float]]:
        """
        Метод позволяет получить таблицу при фиксированном y,
        зависимости x от значения функции от 2-х переменных
        """
        data_table = []

        for j in range(len(self.x_s)):
            f_x_jy = self.values[ind_y][j]
            x_j = self.x_s[j]
            data_table.append((x_j, f_x_jy))

        return data_table

    def interp_two_var(self) -> int | float:
        """
        Интерполяция по двум переменным
        """
        config_points = self.collect_config()

        z_s_interp = list()

        for i in config_points:
            data_table = self.__get_data_table_for_newton_one_var(i)
            newton = NewtonOneVar(self.x, data_table, self.nx)
            curr_z = newton.newton_polynom()
            z_s_interp.append(curr_z)

        data_table = []

        print(f"z_interp = {z_s_interp}")

        for i, ind in enumerate(config_points):
            data_table.append((self.y_s[ind], z_s_interp[i]))

        print(f"data_table = {data_table}")

        newton = NewtonOneVar(self.y, data_table, self.ny)

        self.res = newton.newton_polynom()

        return self.res


