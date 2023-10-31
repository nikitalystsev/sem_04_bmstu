from typing import Callable

from Legendre import Legendre
from GaussSlau import GaussSlau


class GaussIntegral:
    """
    Класс для вычисления интеграла методом Гаусса
    """

    def __init__(self, func: Callable[[int | float], int | float], a: int, b: int, n: int) -> None:
        """
        Инициализация атрибутов класса
        """
        self._n: int = n  # число узлов, он же размер матрицы данных из файла
        self._a: int = a  # нижний предел интегрирования
        self._b: int = b  # верхний предел интегрирования
        self._func: Callable[[int | float], int | float] = func  # функция, которую нужно проинтегрировать

        self._roots = Legendre().roots(self._n)  # находим корни полинома Лежандра степени n

    @staticmethod
    def __get_right_part_for_system(k: int) -> int | float:
        """
        Метод позволяет получить правую часть k-го уравнения системы
        """

        return 2 / (k + 1) if k % 2 == 0 else 0

    def __get_all_right_part_for_system(self) -> list[int | float]:
        """
        Метод позволяет получить правые части всех уравнений системы
        """
        right_parts = list()

        for k in range(2 * self._n):
            right_part = self.__get_right_part_for_system(k)
            right_parts.append(right_part)

        return right_parts

    def __get_left_part_for_system(self, k: int) -> list[int | float]:
        """
        Метод позволяет получить левую часть k-го уравнения системы
        """
        left_part = list()

        for i in range(self._n):
            left_part.append(self._roots[i] ** k)  # self._roots[i] ** k - это коэффициенты системы

        return left_part

    def __get_all_left_part_for_system(self) -> list[list[int | float]]:
        """
        Метод позволяет получить левые части всех уравнений системы
        """

        left_parts = list()

        for k in range(self._n):
            left_part = self.__get_left_part_for_system(k)
            left_parts.append(left_part)

        return left_parts

    def __get_slau_for_gauss_slau(self) -> list[list[int | float]]:
        """
        Метод позволяет сформировать расширенную матрицу для решения ее методом Гаусса
        решения систем уравнений
        """
        left_parts = self.__get_all_left_part_for_system()
        right_parts = self.__get_all_right_part_for_system()

        for i in range(self._n):
            left_parts[i].append(right_parts[i])

        return left_parts

    def __get_x_s(self) -> list[int | float]:
        """
        Метод позволяет получить xi из корней полинома Лежандра
        переходя к произвольным пределам интегрирования
        с помощью линейных преобразований
        """
        x_s = list()

        a, b = self._a, self._b

        for i in range(len(self._roots)):
            xi = (b - a) * self._roots[i] / 2 + (a + b) / 2
            x_s.append(xi)

        return x_s

    def integral(self) -> int | float:
        """
        Метод позволяет получить значение интеграла
        """
        slau = self.__get_slau_for_gauss_slau()

        gauss_slau = GaussSlau(matrix_slau=slau)
        coeff = gauss_slau.gauss()

        x_s = self.__get_x_s()

        a, b = self._a, self._b

        integral = (b - a) * sum([coeff[i] * self._func(x_s[i]) for i in range(self._n)]) / 2

        return integral
