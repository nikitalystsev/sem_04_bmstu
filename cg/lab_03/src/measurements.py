import matplotlib.pyplot as plt
from time import perf_counter
from tkinter import messagebox
import numpy as np


class CompareTime:
    """
    Класс для сравнения времени работы алгоритмов
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """

        self.times = list()
        self.len_line = 0

    @staticmethod
    def time_now():
        """
        Метод позволит получить текущее значение счетчика производительности
        """

        return perf_counter()

    def clean_times(self) -> None:
        """
        Метод очищает список времен
        """
        self.times.clear()

    def print_compare(self):
        """
        Метод выводит результаты сравнения времени в виде гистограммы
        """
        if len(self.times) == 0 and self.len_line == 0:
            text = "По непонятной причине время было еще не измерено!"
            messagebox.showinfo("", text)
            return

        plt.figure("Исследование времени работы алгоритмов построения.", figsize=(10, 7))

        ordinate = range(len(self.times))

        algs = (
            'ЦДА',
            'Брезенхем с\nцелыми\nкоэффициентами',
            'Брезенхем с\nдействительными\nкоэффициентами',
            'Брезенхем с\nс устранением\nступенчатости',
            'Ву',
            'Библиотечный\nалгоритм'
        )

        plt.bar(ordinate, self.times, align='center')
        plt.xticks(ordinate, algs)
        plt.ylabel(f"Секунды (длина линии в пикселях - {self.len_line})")
        plt.show()


class CompareStepping:
    """
    Класс для сравнения ступенчатости в работе алгоритмов
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self.angles = list()
        self.dda_steps = list()
        self.bres_int_steps = list()
        self.bres_float_steps = list()
        self.bres_elim_alias = list()
        self.vu_steps = list()
        self.len_line = 0

    def clean_steps(self) -> None:
        """
        Метод очищает списки ступенчатости
        """
        self.angles.clear()
        self.dda_steps.clear()
        self.bres_int_steps.clear()
        self.bres_float_steps.clear()
        self.bres_elim_alias.clear()
        self.vu_steps.clear()
        self.len_line = 0

    def all_is_empty(self):
        """
        Метод позволяет узнать, посчитаны ли ступеньки
        """
        is_empty = len(self.angles) == 0 and \
            len(self.dda_steps) == 0 and \
            len(self.bres_int_steps) == 0 and \
            len(self.bres_float_steps) == 0 and \
            len(self.bres_elim_alias) == 0 and \
            len(self.vu_steps) == 0 and \
            self.len_line == 0

        return is_empty

    def print_compare(self):
        """
        Метод выводит сравнения ступенчатости в виде графиков зависимости
        количества ступенек от угла наклона прямой при заданной длине линии
        """
        if self.all_is_empty():
            text = "По непонятной причине ступеньки еще не были посчитаны!"
            messagebox.showinfo("", text)
            return

        # размеры в дюймах (1 дюйм = 2.54 см)
        plt.figure("Исследование ступенчатости алгоритмов построение.", figsize=(18, 10))

        plt.subplot(2, 3, 1)
        plt.plot(self.angles, self.dda_steps, label="ЦДА")
        plt.plot(self.angles, self.bres_int_steps, '--', label="Брезенхем с целыми или\nдействительными коэффицентами")
        plt.plot(self.angles, self.bres_elim_alias, '.', label="Брезенхем с устр.\nступенчатости")
        plt.plot(self.angles, self.vu_steps, '-.', label="By")
        plt.title(f"Исследование ступенчатости.\n{self.len_line} - длина отрезка (пиксели)")
        plt.xticks(np.arange(91, step=5))
        plt.legend()
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.subplot(2, 3, 2)
        plt.title("ЦДА")
        plt.plot(self.angles, self.dda_steps)
        plt.xticks(np.arange(91, step=5))
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.subplot(2, 3, 3)
        plt.title("Брезенхем с целыми коэффицентами")
        plt.plot(self.angles, self.bres_int_steps)
        plt.xticks(np.arange(91, step=5))
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.subplot(2, 3, 4)
        plt.title("Брезенхем с действительными коэффицентами")
        plt.plot(self.angles, self.bres_float_steps)
        plt.xticks(np.arange(91, step=5))
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.subplot(2, 3, 5)
        plt.title("Брезенхем с действительными коэффицентами")
        plt.plot(self.angles, self.bres_elim_alias)
        plt.xticks(np.arange(91, step=5))
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.subplot(2, 3, 6)
        plt.title("ВУ")
        plt.plot(self.angles, self.vu_steps)
        plt.xticks(np.arange(91, step=5))
        plt.ylabel("Количество ступенек")
        plt.xlabel("Угол в градусах")

        plt.show()
