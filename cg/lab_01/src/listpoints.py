import tkinter as tk
from tkinter import ttk


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
        self.heading(column="point", text="Точка")
        self.column("#1", width=30, anchor='center')
        self.column("#2", width=148, anchor='center')

    def is_valid_number(self, n: int) -> bool:
        """
        Метод проверяет валидность номера точки
        :param n: номер точки
        :return: True - номер валидный, False иначе
        """
        for k in self.get_children(""):
            if int(self.set(k, 0)) == n:
                return True
        return False

    def add_point(self, point: tuple[float, float]) -> None:
        """
        Метод добавляет точку в таблицу
        :param point: точка
        :return: None
        """
        index = len(self.get_children()) + 1
        self.insert("", tk.END, values=(index, str(point)))

    def del_point(self, n: int) -> None:
        """
        Метод удаляет точку из таблицы
        :param n: номер точки
        :return: None
        """
        for k in self.get_children(""):
            if int(self.set(k, 0)) == n:
                self.delete(k)

        self.recalc_index()

    def change_point(self, n: int, new_x: float, new_y: float) -> None:
        """
        Метод изменяет координаты точки в таблице
        :param n: номер точки
        :param new_x: новая абсцисса
        :param new_y: новая ордината
        :return: None
        """
        for k in self.get_children(""):
            if int(self.set(k, 0)) == int(n):
                self.item(k, values=(n, str((new_x, new_y))))

    def recalc_index(self) -> None:
        """
        Метод пересчитывает номера точек после удаления очередной
        :return: None
        """
        i = 1
        for k in self.get_children(""):
            self.set(k, 0, i)
            i += 1

    def clear_points(self) -> None:
        """
        Метод очищает таблицу
        :return: None
        """
        for item in self.get_children():
            self.delete(item)
