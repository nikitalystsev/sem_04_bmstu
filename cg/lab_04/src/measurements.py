import matplotlib.pyplot as plt
from time import perf_counter
from tkinter import messagebox


class CompareTimeCircle:
    """
    Класс для сравнения времени работы алгоритмов
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self.times = list()
        self.radius_list = list()
        self._dict_algs = {0: "Каноническое уравнение",
                           1: "Параметрическое уравнение",
                           2: "Алгоритм Брезенхема",
                           3: "Алгоритм средней точки",
                           4: "Библиотечный алгоритм"}

    @staticmethod
    def time_now():
        """
        Метод позволит получить текущее значение счетчика производительности
        """

        return perf_counter()

    def print_compare(self):
        """
        Метод выводит результаты сравнения времени работы алгоритма от радиуса
        """
        if len(self.times) == 0 and len(self.radius_list) == 0:
            text = "По непонятной причине время было еще не измерено!"
            messagebox.showinfo("", text)
            return

        plt.figure(figsize=(10, 6))
        plt.title(f"Замеры времени для построения окружности")

        for i in range(5):
            plt.plot(self.radius_list[i], self.times[i], label=self._dict_algs[i])

        print(f"миновал цикл...")

        plt.legend()
        plt.xlabel("Длина радиуса")
        plt.ylabel("Время")

        plt.show()


class CompareTimeEllipse:
    """
    Класс для сравнения времени работы алгоритмов
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self.times = list()
        self.radius_list = list()
        self._dict_algs = {0: "Каноническое уравнение",
                           1: "Параметрическое уравнение",
                           2: "Алгоритм Брезенхема",
                           3: "Алгоритм средней точки",
                           4: "Библиотечный алгоритм"}

    @staticmethod
    def time_now():
        """
        Метод позволит получить текущее значение счетчика производительности
        """

        return perf_counter()

    def print_compare(self):
        """
        Метод выводит результаты сравнения времени работы алгоритма от радиуса
        """
        if len(self.times) == 0 and len(self.radius_list) == 0:
            text = "По непонятной причине время было еще не измерено!"
            messagebox.showinfo("", text)
            return

        plt.figure(figsize=(10, 6))
        plt.title(f"Замеры времени для построения эллипса")

        for i in range(5):
            plt.plot(self.radius_list[i], self.times[i], label=self._dict_algs[i])

        plt.legend()
        plt.xlabel("Длина большой полуоси а")
        plt.ylabel("Время")

        plt.show()
