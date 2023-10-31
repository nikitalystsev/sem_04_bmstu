import tkinter as tk
from my_figure import *
import numpy as np
from tkinter import messagebox

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

    def __init__(self, y_min, y_max, grid_step=50, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param y_min: желаемая минимальная ордината
        :param y_max: желаемая максимальная ордината
        :param x_min: желаемая минимальная абсцисса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.y_min = y_min
        self.y_max = y_max
        self.x_max, self.x_min = self.get_x_coord()
        self.grid_step = grid_step
        self.figure = MyFigure()
        self.km = self.get_km()
        self.draw_grid()
        self.draw_figure()
        self.history = StateHistory()
        self.history.add_state(self.figure)

    def get_x_coord(self):
        axis_coef = self.width / self.height
        x_max = self.y_max * axis_coef
        x_min = -x_max

        return x_max, x_min

    def draw_grid(self) -> None:
        """
        Метод отображает сетку на плоскости
        """

        # Рисуем вертикальные линии с шагом grid_step
        for x in range(self.width // 2, self.width, self.grid_step):
            self.create_line(x, 0, x, self.height, fill=SILVER)  # вправо
            self.create_line(self.width - x, 0, self.width - x, self.height, fill=SILVER)  # влево
            origin_x_left, origin_x_right = self.to_origin_x(self.width - x), self.to_origin_x(x)
            text_left, text_right = f"{round(origin_x_left, 2)}", f"{round(origin_x_right, 2)}"
            self.create_text(x, self.height // 2 - 10, text=text_right)
            self.create_text(self.width - x, self.height // 2 - 10, text=text_left)

        # Рисуем горизонтальные линии с шагом grid_step
        for y in range(self.height // 2, self.height, self.grid_step):
            self.create_line(0, y, self.width, y, fill=SILVER)
            self.create_line(0, self.height - y, self.width, self.height - y, fill=SILVER)
            origin_y_up, origin_y_down = self.to_origin_y(self.height - y), self.to_origin_y(y)
            text_up, text_dowm = f"{round(origin_y_up, 2)}", f"{round(origin_y_down, 2)}"
            if not float_equal(origin_y_up, 0) and not float_equal(origin_y_down, 0):
                self.create_text(self.width // 2 + 14, y, text=text_dowm)
                self.create_text(self.width // 2 + 14, self.height - y, text=text_up)
        # Рисуем оси координат
        # ось ординат
        self.create_line(self.width / 2, self.height, self.width / 2, 0, width=2, arrow="last", fill=BLACK)
        # ось абсцисс
        self.create_line(0, self.height / 2, self.width, self.height / 2, width=2, arrow="last", fill=BLACK)

    def get_km(self) -> float:
        """
        Функция вычисляет коэффициент масштабирования
        :return: None
        """
        if self.x_max - self.x_min != 0 and self.y_max - self.y_min != 0:
            kx = (self.width - 0) / (self.x_max - self.x_min)
            ky = (self.height - 0) / (self.y_max - self.y_min)
        else:
            kx = ky = self.km

        return min(kx, ky)

    def draw_ellipse_arc(self):
        """
        Метод отображает дугу эллипса
        Формула для вычисления координат точки на эллипсе с центром в точке (h,k),
        большой полуосью a, малой полуосью b и углом поворота φ:
        x = h + a*cos(θ)cos(φ) - b*sin(θ)sin(φ)
        y = k + a*cos(θ)sin(φ) + b*sin(θ)*cos(φ)
        """
        # Уравнение эллипса: x^2 / a^2 + y^2 / b^2 = 1
        # где а - большая полуось, b - малая полуось

        # создаем массив углов от -pi/2 до pi/2 с шагом 0.01
        # Это углы самих точек! Не углы поворота
        t = [i for i in np.arange(-m.pi / 2, m.pi / 2, 0.001)]

        # вычисляем координаты точек на эллипсе
        x = [self.figure.center_ellipse.x + self.figure.b * m.cos(theta) * m.cos(
            self.figure.angle) - self.figure.a * m.sin(theta) * m.sin(self.figure.angle) for theta in t]
        y = [self.figure.center_ellipse.y + self.figure.b * m.cos(theta) * m.sin(
            self.figure.angle) + self.figure.a * m.sin(theta) * m.cos(self.figure.angle) for theta in t]

        # строим эллипс по точкам
        for i in range(len(t) - 1):
            self.create_line(self.to_canvas_x(x[i]), self.to_canvas_y(y[i]),
                             self.to_canvas_x(x[i + 1]), self.to_canvas_y(y[i + 1]), width=3,
                             fill=DARKCYAN)

    def draw_lines(self):
        """
        Метод рисует прямые
        """
        self.create_line(self.to_canvas_x(self.figure.flash_point.x),
                         self.to_canvas_y(self.figure.flash_point.y),
                         self.to_canvas_x(self.figure.point1.x),
                         self.to_canvas_y(self.figure.point1.y), width=3, fill=DARKCYAN)

        self.create_line(self.to_canvas_x(self.figure.flash_point.x),
                         self.to_canvas_y(self.figure.flash_point.y),
                         self.to_canvas_x(self.figure.point2.x),
                         self.to_canvas_y(self.figure.point2.y), width=3, fill=DARKCYAN)

        self.create_line(self.to_canvas_x(self.figure.point1.x),
                         self.to_canvas_y(self.figure.point1.y),
                         self.to_canvas_x(self.figure.point2.x),
                         self.to_canvas_y(self.figure.point2.y), width=3, fill=DARKCYAN)

    def draw_figure(self):
        """
        Метод рисует фигуру
        """
        self.draw_ellipse_arc()
        self.draw_lines()

        canvas_x, canvas_y = self.to_canvas_coords(self.figure.center_figure.x,
                                                   self.figure.center_figure.y)

        self.create_point(canvas_x, canvas_y, color=RED)
        text = f"({round(self.figure.center_figure.x, 2)};" \
               f"{round(self.figure.center_figure.y, 2)})"
        self.create_text(canvas_x + 5, canvas_y + 10, text=text,
                         fill=RED, font=("Courier New", 7))

    def rotate_figure(self, center_rotate: Point, angle: float):
        """
        Метод поворачивает фигуру
        """
        # добавил состояние в историю состояний
        self.history.add_state(self.figure)

        self.delete(tk.ALL)
        self.figure.rotate_figure(center_rotate, angle)
        self.draw_grid()
        self.draw_figure()

        canvas_x, canvas_y = self.to_canvas_coords(center_rotate.x, center_rotate.y)
        self.create_point(canvas_x, canvas_y, color=GREEN)

    def transfer_figure(self, dx: float, dy: float):
        """
        Метод переносит фигуру
        """
        # добавил состояние в историю состояний
        self.history.add_state(self.figure)

        self.delete(tk.ALL)
        self.figure.transfer_figure(dx, dy)
        self.draw_grid()
        self.draw_figure()

    def scaling_figure(self, kx: float, ky: float, xc: float, yc: float):
        """
        Метод масштабирует фигуру
        """
        # добавил состояние в историю состояний
        self.history.add_state(self.figure)

        self.delete(tk.ALL)
        self.figure.scaling_figure(kx, ky, xc, yc)
        self.draw_grid()
        self.draw_figure()

        canvas_x, canvas_y = self.to_canvas_coords(xc, yc)
        self.create_point(canvas_x, canvas_y, color=GREEN)

    def step_back(self):
        """
        Метод возвращает предыдущее состояние фигуры
        """
        if len(self.history.state_history) == 0:
            text = "Фигура в своем первоначальном состоянии!\n"
            messagebox.showinfo("", text)
            return

        self.delete(tk.ALL)
        self.draw_grid()
        self.figure = self.history.state_history.pop()
        self.draw_figure()

    def change_param_figure(self, a: float, b: float, xc_ellipse: float,
                            yc_ellipse: float, x_inters: float):
        """
        Метод изменяет параметры фигуры
        """

        if len(self.history.state_history) > 1:
            text = "Изменить параметры фигуры можно лишь для изначально" \
                   "заданного изображения фигуры!"
            messagebox.showwarning("", text)
            return

        # добавил состояние в историю состояний
        self.history.add_state(self.figure)

        self.figure.a = a
        self.figure.b = b
        self.figure.center_ellipse = Point(xc_ellipse, yc_ellipse)
        self.figure.update_param_figure(x_inters)
        self.delete(tk.ALL)
        self.draw_grid()
        self.draw_figure()

    def to_origin_x(self, canvas_x: float) -> float:
        """
        Метод преобразует абсциссу точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_x: абсцисса холста
        :return: оригинальная абсцисса
        """
        # - 0 потому, что начальная точка поля вывода - это 0
        origin_x = (canvas_x - 0) / self.km + self.x_min

        return origin_x

    def to_origin_y(self, canvas_y: float) -> float:
        """
        Метод преобразует ординату точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_y:  ордината холста
        :return: оригинальная ордината
        """
        # то же самое, что и с абсциссой
        origin_y = self.y_max - (canvas_y - 0) / self.km

        return origin_y

    def to_origin_coords(self, canvas_x: float, canvas_y: float) \
            -> (float, float):
        """
        Метод преобразует координаты точки, ранее преобразованные
        для отображения на холсте, в оригинальные значения
        :param canvas_x: абсцисса холста
        :param canvas_y: ордината холста
        :return: оригинальные координаты
        """

        return self.to_origin_x(canvas_x), self.to_origin_y(canvas_y)

    def to_canvas_x(self, origin_x: float) -> float:
        """
        Метод преобразует полученную с поля ввода абсциссу
        для отображения на холсте
        :param origin_x: оригинальная абсцисса
        :return: абсцисса холста.
        """
        canvas_x = int(0 + (origin_x - self.x_min) * self.km)

        return canvas_x

    def to_canvas_y(self, origin_y: float) -> float:
        """
        Метод преобразует полученную с поля ввода ординату
        для отображения на холсте
        :param origin_y: оригинальная ордината
        :return: ордината холста
        """
        canvas_y = int(0 + (self.y_max - origin_y) * self.km)

        return canvas_y

    def to_canvas_coords(self, x: float, y: float) -> (float, float):
        """
        Метод преобразует полученные с поля ввода координаты
        для отображения на холсте
        :param x: оригинальная абсцисса
        :param y: оригинальная ордината
        :return: координаты точки для холста
        """

        return self.to_canvas_x(x), self.to_canvas_y(y)

    def create_point(self, x0: float, y0: float, color: str = 'red') -> None:
        """
        Метод отображает точку на плоскости
        """
        self.create_oval(x0 - 3, y0 - 3, x0 + 3, y0 + 3,
                         fill=color, outline=color)
