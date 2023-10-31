from spline import *
from Newton_polynom import *


class Task:
    """
    Класс для решения поставленной задачи
    """

    def __init__(self, filename: str, n: int = 3):
        """
        Инициализация атрибутов класса
        """
        # создал экземпляр класса данных,
        # прочитал таблицу с точками и
        # прочитал точку интерполирования
        self.data = Data()
        self.data.read_data(filename)
        self.data.print_data_table()
        self.data.read_x()

        # создал экземпляр класса Сплайн и Полинома Ньютона
        self.spline = Spline(self.data)
        self.newton = Newton(self.data, n)

        self.print_task_res()

    def calc_condition(self, condition: int):
        """
        Метод позволяет посчитать начальные значения
        прогоночных коэффициентов в зависимости от краевых условий
        """
        # посчитал начальные значения прогоночных коэффициентов
        # для третьего краевого условия
        theta2 = self.newton.derivative2_newton_polynom(self.data.data_table[0].x, 0.001)

        # нашел в общем из 3-х краевых условий значение С из фиктивного интервала
        cn_plus1 = self.newton.derivative2_newton_polynom(self.data.data_table[-1].x, 0.001)

        # из формул вытекает деление на 2
        cn_plus1 /= 2
        theta2 /= 2

        # запускаю проверку условий
        match condition:
            case 1:
                print("\nКраевые условия 1:        0 and 0")
                return 0, 0, 0
            case 2:
                print("\nКраевые условия 2:  P''(x0) and 0")
                return 0, theta2, 0
            case _:
                print("\nКраевые условия 3:  P''(x0) and P''(xN)")
                return 0, theta2, cn_plus1

    def print_task_res(self):
        """
        Метод выводит все результаты по заданию
        """
        # Интерполирую полиномом ньютона
        self.newton.newton_polynom()
        self.newton.print_newton_res()

        for i in [1, 2, 3]:
            ksi2, theta2, cn_plus1 = self.calc_condition(i)

            print(f"ksi2 = {ksi2: .3f}, theta2 = {theta2: .3f}, cn_plus1 = {cn_plus1: .3f}")

            self.spline.spline_interpolation(ksi2, theta2, cn_plus1)
            self.spline.print_spline_res()
