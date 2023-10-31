import tkinter as tk
import math as m
from typing import Union

from PointClass import Point
from dda import Dda
from bresenham import BresenhamInt, BresenhamFloat, BresenhamElimAlias
from vu import Vu
from measurements import CompareTime

ORANGE = "#FFA500"
RED = "#FF0000"
DARKCYAN = "DarkCyan"
GREEN = "#008000"
BLUE = "#0000FF"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"
BLACK = "#000000"
Aquamarine = "#7FFFD4"
LightCyan = "#E0FFFF"
SILVER = "#C0C0C0"

EPS = 1e-9


def float_equal(a, b):
    """
    Функция сравнивает вещественные числа
    """

    return abs(a - b) < EPS


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, color_line: str, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.draw_axis()
        self.color_line = color_line

    def draw_axis(self) -> None:
        """
        Метод отображает экранные оси
        """
        # по оси ординат
        for i in range(0, self.height, 50):
            self.create_line(0, i, 6, i, width=2)
            if i != 0:
                self.create_text(20, i, text=str(i), font=("Times New Roman", 10))

        # по оси абсцисс
        for i in range(0, self.width, 50):
            self.create_line(i, 0, i, 6, width=2)
            if i != 0:
                self.create_text(i, 20, text=str(i), font=("Times New Roman", 10))

    def draw_line(self, alg: Union[Dda, BresenhamInt, BresenhamFloat, BresenhamElimAlias, Vu]) -> float:
        """
        Метод будет отображать линию, используя один из алгоритмов
        """
        beg = CompareTime.time_now()
        points = alg.get_points_for_line(self.get_line_color(), self.get_bg_color())
        end = CompareTime.time_now()

        for point in points:
            self.create_point(point.x, point.y, point.color)

        return end - beg

    def get_bg_color(self) -> str:
        """
        Метод позволяет получить текущий цвет фона холста
        """

        return self["bg"]

    def set_bg_color(self, color: str) -> None:
        """
        Метод позволяет изменить цвет фона холста
        """
        self.config(bg=color)

    def get_line_color(self) -> str:
        """
        Метод позволяет получить текущий цвет линии
        """

        return self.color_line

    def set_line_color(self, color: str) -> None:
        """
        Метод позволяет изменить цвет линии
        """
        self.color_line = color

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self.delete(tk.ALL)
        self.draw_axis()

    # @staticmethod
    # def apply_transform(point: Point, matrix) -> Point:
    #     """
    #     Метод применяет операцию к точке
    #     """
    #     # преобразуем точку в однородные координаты
    #     point_np = np.array([point.x, point.y, 1])
    #     transformed_point = np.matmul(matrix, point_np)  # умножаем точку на матрицу
    #     # преобразуем точку из однородных координат в декартовы координаты
    #     transformed_point = transformed_point[:2] / transformed_point[2]
    #
    #     return Point(transformed_point[0], transformed_point[1], point.color)

    # def rotate_line(self, begin_point: Point, end_point: Point, angle: float):
    #     """
    #     Метод поворачивает фигуру
    #     x' = dx * cos(theta) - dy * sin(theta)
    #     y' = dx * sin(theta) + dy * cos(theta),
    #     где dx = x - xc, dy = y - yc
    #                     ( cos(angle) -sin(angle)  0 )
    #     rotate_matrix = ( sin(angle)  cos(angle)  0 )
    #                     (     0           0       1 )
    #     Используем афинные преобразования:
    #     Сначала перенос центра поворота в начало координат,
    #     потом поворот,
    #     потом возвращение центра поворота обратно
    #     Этот метод позволяет сохранить пропорции объекта при повороте для любого центра поворота
    #     """
    #     # определяем координаты центра поворота
    #     xc, yc = begin_point.x, begin_point.y
    #
    #     # ввиду непонятных для меня обстоятельств нужно менять знаки у центров
    #     xc, yc = xc, -yc
    #
    #     # переводим угол в радианы
    #     radians_angle = m.radians(angle)
    #
    #     # записываем последовательно матрицы в порядке их применимости
    #     transfer_matrix = np.array([[1, 0, -xc], [0, 1, -yc], [0, 0, 1]])
    #     rotate_matrix = np.array([[m.cos(radians_angle), -m.sin(radians_angle), 0],
    #                               [m.sin(radians_angle), m.cos(radians_angle), 0],
    #                               [0, 0, 1]])
    #     reverse_transfer_matrix = np.array([[1, 0, xc], [0, 1, yc], [0, 0, 1]])
    #
    #     # получаем результирующую матрицу операции
    #     result_matrix = np.matmul(transfer_matrix, rotate_matrix)
    #     result_matrix = np.matmul(result_matrix, reverse_transfer_matrix)
    #
    #     # применяем марицу операции к конечной точке
    #     end_point = self.apply_transform(end_point, result_matrix)
    #
    #     return begin_point, end_point

    def rotate_line(self, begin_point: Point, end_point: Point, angle: float):

        # переводим угол в радианы
        radians_angle = m.radians(angle)
        cx, cy = begin_point.x, begin_point.y
        px, py = end_point.x, end_point.y

        x = px

        px = round(cx + (x - cx) * m.cos(radians_angle) + (py - cy) * m.sin(radians_angle))
        py = round(cy - (x - cx) * m.sin(radians_angle) + (py - cy) * m.cos(radians_angle))

        return begin_point, Point(px, py, self.color_line)

    def create_point(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости
        """
        # +1 по ординате нужен лишь, чтобы отобразить точку размером в 1 пиксель
        # особенности tkinter
        self.create_line(x0, y0, x0 + 1, y0, fill=color)
