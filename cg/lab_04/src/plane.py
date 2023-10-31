import tkinter as tk
from typing import Union

from canonical_equ import CanonicalCircle, CanonicalEllipse
from parametric_equ import ParametricCircle, ParametricEllipse
from bresenham import BresenhamCircle, BresenhamEllipse
from mid_point import MidPointAlgCircle, MidPointAlgEllipse
from measurements import CompareTimeCircle, CompareTimeEllipse

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


def float_equal(a: int | float, b: int | float):
    """
    Функция сравнивает вещественные числа
    """

    return abs(a - b) < EPS


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, color_figure: str, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self._width = kwargs.get("width")
        self._height = kwargs.get("height")
        self.__draw_axis()
        self._color_figure = color_figure
        self._color_bg = self["bg"]

    def __draw_axis(self) -> None:
        """
        Метод отображает экранные оси
        """
        # по оси ординат
        for i in range(0, self._height, 50):
            self.create_line(0, i, 6, i, width=2)
            if i != 0:
                self.create_text(20, i, text=str(i), font=("Times New Roman", 10))

        # по оси абсцисс
        for i in range(0, self._width, 50):
            self.create_line(i, 0, i, 6, width=2)
            if i != 0:
                self.create_text(i, 20, text=str(i), font=("Times New Roman", 10))

    @property
    def color_bg(self) -> str:
        """
        Метод позволяет получить текущий цвет фона холста
        """

        return self._color_bg

    @color_bg.setter
    def color_bg(self, value: str) -> None:
        """
        Метод позволяет изменить цвет фона холста
        """
        self.config(bg=value)
        self._color_bg = value

    @property
    def color_figure(self) -> str:
        """
        Метод позволяет изменить цвет линии
        """
        return self._color_figure

    @color_figure.setter
    def color_figure(self, value: str) -> None:
        """
        Метод позволяет получить текущий цвет линии
        """

        self._color_figure = value

    def draw_circle(self, alg: Union[CanonicalCircle, ParametricCircle, BresenhamCircle, MidPointAlgCircle]) -> float:
        """
        Метод отобразит окружность одним из алгоритмов
        """
        beg = CompareTimeCircle.time_now()
        points = alg.create_circle(self.color_figure)
        end = CompareTimeCircle.time_now()

        for point in points:
            self.create_point(point.x, point.y, point.color)

        return end - beg

    def draw_ellipse(self,
                     alg: Union[CanonicalEllipse, ParametricEllipse, BresenhamEllipse, MidPointAlgEllipse]) -> float:
        """
        Метод отобразит окружность одним из алгоритмов
        """
        beg = CompareTimeEllipse.time_now()
        points = alg.create_ellipse(self.color_figure)
        end = CompareTimeEllipse.time_now()

        for point in points:
            self.create_point(point.x, point.y, point.color)

        return end - beg

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self.delete(tk.ALL)
        self.__draw_axis()

    def create_point(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости
        """
        # +1 по ординате нужен лишь, чтобы отобразить точку размером в 1 пиксель
        # особенности tkinter
        self.create_line(x0, y0, x0 + 1, y0, fill=color)
