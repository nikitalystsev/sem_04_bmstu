# import matplotlib.pyplot as plt
from time import perf_counter
# from tkinter import messagebox


class CompareTime:
    """
    Класс для сравнения времени работы алгоритмов
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        pass

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
        pass
