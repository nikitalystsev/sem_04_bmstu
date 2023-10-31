from typing import Callable


class SimpsonIntegral:
    """
    Класс для вычисления интеграла методом Симпсона
    """

    def __init__(self, func: Callable[[int | float], int | float], a: int, b: int, n: int) -> None:
        """
        Инициализация атрибутов класса
        """
        # должно быть четным
        self._n: int = n  # число узлов
        self._a: int = a  # нижний предел интегрирования
        self._b: int = b  # верхний предел интегрирования
        self._h: int | float = (self._b - self._a) / (self._n * 2)  # шаг разбиения
        self._func: Callable[[int | float], int | float] = func  # функция, которую нужно проинтегрировать

    def __get_x_s(self) -> list[int | float]:
        """
        Метод получает список узлов, на которые разбивается интервал интегрирования  [a, b]
        """
        a, b = self._a, self._b

        x_s = [a + i * self._h for i in range(self._n * 2 + 1)]

        return x_s

    def __get_y_s(self, x_s: list[int | float]) -> list[int | float]:
        """
        Метод позволяет получить значение подынтегральной функции в узлах разбиения
        """
        y_s = [self._func(x) for x in x_s]

        return y_s

    def __calc_sum_odd(self, y_s: list[int | float]) -> int | float:
        """
        Метод суммирует значения в нечетных узлах внутри интервала интегрирования
        """
        sum_odd = 4 * sum([y_s[2 * i - 1] for i in range(1, self._n)])

        return sum_odd

    def __calc_sum_even(self, y_s: list[int | float]) -> int | float:
        """
        Метод суммирует значения в четных узлах внутри интервала интегрирования
        """
        sum_even = 2 * sum([y_s[2 * i] for i in range(1, self._n - 1)])

        return sum_even

    def integral(self) -> int | float:
        """
        Метод позволяет получить значение интеграла
        """
        x_s = self.__get_x_s()
        y_s = self.__get_y_s(x_s)

        sum_odd = self.__calc_sum_odd(y_s)
        sum_even = self.__calc_sum_even(y_s)

        integral = (self._h / 3) * (y_s[0] + sum_odd + sum_even + y_s[-1])

        return integral
