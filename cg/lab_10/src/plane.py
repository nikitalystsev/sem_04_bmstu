import tkinter as tk
from typing import Callable

from floating_horizon import FloatingHorizon

BLACK = "#000000"
WHITE = "#FFFFFF"
ORANGE = "#FFA500"
RED = "#FF0000"
DARKCYAN = "DarkCyan"
GREEN = "#008000"
BLUE = "#0000FF"
VIOLET = "#800080"
YELLOW = "#FFFF00"
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

    def __init__(self, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self._width = kwargs.get("width")
        self._height = kwargs.get("height")

        self._color_bg: str = self["bg"]
        self._angle_x = 0
        self._angle_y = 0
        self._angle_z = 0

        # self.__draw_axis()

    # def __draw_axis(self) -> None:
    #     """
    #     Метод отображает экранные оси
    #     """
    #     # по оси ординат
    #     for i in range(0, self._height, 50):
    #         self.create_line(0, i, 6, i, width=2)
    #         # if i != 0:
    #         #     self.create_text(20, i, text=str(i), font=("Times New Roman", 10))
    #
    #     # по оси абсцисс
    #     for i in range(0, self._width, 50):
    #         self.create_line(i, 0, i, 6, width=2)
    #         # if i != 0:
    #         #     self.create_text(i, 20, text=str(i), font=("Times New Roman", 10))

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

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self.delete(tk.ALL)

        # self.__draw_axis()

    def create_point(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости
        """
        # +1 по абсциссе нужен лишь, чтобы отобразить точку размером в 1 пиксель
        # особенности tkinter
        self.create_line(x0, y0, x0 + 1, y0, fill=color)

    # методы конкретно для лабораторной работы

    def draw_func(
            self,
            border_x: list[int | float, int | float],
            border_z: list[int | float, int | float],
            x_step: int | float,
            z_step: int | float,
            func: Callable[[int | float, int | float], int | float],
    ):
        """
        Метод позволяет отобразить график
        """
        self.clean_plane()
        # когда первый раз отображаем график, целесообразно сбросить углы
        self._angle_x = 0
        self._angle_y = 0
        self._angle_z = 0

        alg = FloatingHorizon(
            self,
            border_x,
            border_z,
            x_step,
            z_step,
            func,
            self._angle_x,
            self._angle_y,
            self._angle_z
        )

        alg.draw()

    def rotate_around_x(
            self,
            border_x: list[int | float, int | float],
            border_z: list[int | float, int | float],
            x_step: int | float,
            z_step: int | float,
            func: Callable[[int | float, int | float], int | float],
            angle_x: int | float):
        """
        Метод позволяет повернуть фигуру по оси OX
        """
        self.clean_plane()
        self._angle_x += angle_x

        alg = FloatingHorizon(
            self,
            border_x,
            border_z,
            x_step,
            z_step,
            func,
            self._angle_x,
            self._angle_y,
            self._angle_z
        )

        alg.draw()

    def rotate_around_y(
            self,
            border_x: list[int | float, int | float],
            border_z: list[int | float, int | float],
            x_step: int | float,
            z_step: int | float,
            func: Callable[[int | float, int | float], int | float],
            angle_y: int | float):
        """
        Метод позволяет повернуть фигуру по оси OX
        """
        self.clean_plane()
        self._angle_y += angle_y

        alg = FloatingHorizon(
            self,
            border_x,
            border_z,
            x_step,
            z_step,
            func,
            self._angle_x,
            self._angle_y,
            self._angle_z
        )

        alg.draw()

    def rotate_around_z(
            self,
            border_x: list[int | float, int | float],
            border_z: list[int | float, int | float],
            x_step: int | float,
            z_step: int | float,
            func: Callable[[int | float, int | float], int | float],
            angle_z: int | float):
        """
        Метод позволяет повернуть фигуру по оси OX
        """
        self.clean_plane()
        self._angle_z += angle_z

        alg = FloatingHorizon(
            self,
            border_x,
            border_z,
            x_step,
            z_step,
            func,
            self._angle_x,
            self._angle_y,
            self._angle_z
        )

        alg.draw()



