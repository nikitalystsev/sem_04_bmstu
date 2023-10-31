import tkinter as tk
from tkinter import ttk

from PointClass import Point


class ListPoints(ttk.Treeview):
    """
    Таблица со списком точек
    """

    def __init__(self, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        style_head = ttk.Style()
        style_head.configure("Treeview.Heading", font=("Courier New", 12))
        style_head.configure("Treeview", font=("Courier New", 9))

        self.heading(column="number", text="№")
        self.heading(column="point_x", text="X")
        self.heading(column="point_y", text="Y")
        self.column("#1", width=30, anchor='center')
        self.column("#2", width=100, anchor='center')
        self.column("#3", width=100, anchor='center')

    def add_point(self, point: Point) -> None:
        """
        Метод добавляет точку в таблицу
        :param point: точка
        :return: None
        """
        index = len(self.get_children()) + 1
        self.insert("", tk.END, values=(index, point.x, point.y))

    def clear_points(self) -> None:
        """
        Метод очищает таблицу
        :return: None
        """
        for item in self.get_children():
            self.delete(item)
