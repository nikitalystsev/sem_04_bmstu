import math as m
import numpy as np

N_REPS = 1000  # константа, отвечающая за число интервалов разбиения в методе трапеций


class LaplaceFuncNewton:
    """
    Класс для нахождения аргумента функции Лапласа при заданном значении функции
    """
    """
    Функция Лапласа нечетная
    Согласно таблицам значений этой функции, для метода половинного деления можно взять отрезок 
    от -5 до 5, поскольку для x > 5 можно принять f(x) = 0.5
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self._solve_x: int | float = 0  # значение по умолчанию для инициализации
        self._is_solve: bool = False  # флаг, определяющий, было ли получено решение

    @staticmethod
    def __input_var0() -> float:
        """
        Метод, позволяющий ввести начальное приближение
        """

        return float(input("\nВведите начальное приближение: "))

    @staticmethod
    def __input_eps() -> float:
        """
        Метод, позволяющий ввести точность вычисления
        """

        return float(input("\nВведите требуемую точность: "))

    @staticmethod
    def __input_func_value() -> float:
        """
        Метод, позволяющий ввести значение функции Лапласа
        """

        return float(input("\nВведите значение функции Лапласа, для которого требуется найти аргумент: "))

    @staticmethod
    def __x_by_func(func_value: int | float):
        """
        Как то для моего собственного понимания я это сделал
        """

        def laplace(x: int | float):
            """
            Собственно, сама функция Лапласа
            """

            def f(_x: int | float):
                """
                Подынтегральное выражение функции Лапласа
                """
                f_x = (2 / m.sqrt(2 * m.pi)) * m.exp(-(_x ** 2) / 2)

                return f_x

            #  интеграл вычисляется методом трапеций
            n = N_REPS
            h = (x - 0) / n  # шаг разбиения
            integr = (f(0) + f(x)) / 2  # суммируем значения функции на концах интервала

            for i in range(1, n):
                x = 0 + i * h  # вычисляем x на текущем интервале
                integr += f(x)  # добавляем значение функции на текущем интервале к интегралу
            integr *= h  # умножаем сумму значений на шаг

            return func_value - integr

        return laplace

    @staticmethod
    def laplace(x: int | float):
        """
        Собственно, сама функция Лапласа
        """

        def f(_x: int | float):
            """
            Подынтегральное выражение функции Лапласа
            """
            f_x = (2 / m.sqrt(2 * m.pi)) * m.exp(-(_x ** 2) / 2)

            return f_x

        #  интеграл вычисляется методом трапеций
        n = N_REPS
        h = (x - 0) / n  # шаг разбиения
        integr = (f(0) + f(x)) / 2  # суммируем значения функции на концах интервала

        for i in range(1, n - 1):
            x = 0 + i * h  # вычисляем x на текущем интервале
            integr += f(x)  # добавляем значение функции на текущем интервале к интегралу
        integr *= h  # умножаем сумму значений на шаг

        return integr

    @staticmethod
    def derivative_laplace(_x: int | float):
        """
        Подынтегральное выражение функции Лапласа
        """
        f_x = (2 / m.sqrt(2 * m.pi)) * m.exp(-(_x ** 2) / 2)

        return f_x

    @staticmethod
    def __check_delta(dx: np.ndarray[int | float], eps: float):
        """
        Метод позволяет вычислить точность вычислений
        """
        abs_dx = np.absolute(dx)

        if max(abs_dx) <= eps:
            return True

        return False

    def __solve_by_newton(self, x0: int | float, eps: float):
        """
        Метод позволяет получить решение системы уравнений, заданной по тз
        """
        func_value = self.__input_func_value()
        # if func_value >= 0.5:
        #     print(f"\nЗначение функции Лапласа не может превышать 0.5")
        #     return

        my_f = self.__x_by_func(func_value)  # получил функцию, для которой будем искать корень

        self._solve_x = x0

        count_iter = 0

        condition = True

        while condition:
            # делитель - это производная функции my_f
            dx = -(my_f(self._solve_x) / -self.laplace(self._solve_x))

            self._solve_x += dx

            count_iter += 1

            if abs(dx) < eps:
                condition = False

        print(f"\nЗначение функции: {func_value}, найденный по этому значению x = {self._solve_x: .3f}")
        print(f"Функция Лапласа от этого x, вычисленный методом трапеций: {self.laplace(self._solve_x): .3f}")
        print(f"Для вычисления корня потребовалось {count_iter} итераций")

    def get_solve_x(self):
        """
        Метод позволяет получить решение уравнения, заданного по тз
        """
        var0 = self.__input_var0()
        eps = self.__input_eps()

        self.__solve_by_newton(var0, eps)
