import tkinter as tk

from PointClass import *


def sign(arg):
    """
    Функция определяет знак переданного числа
    """

    return 1 if arg > 0 else -1 if arg < 0 else 0


def get_rgb_intensity(color: str, bg_color: str, intensity: int):
    """
    Метод позволяет получить массив цветов одного оттенка разной интенсивности
    """
    # создали для использования метода winfo_rgb
    canvas = tk.Canvas()

    grad = []
    # разложение цвета линии на составляющие ргб
    r1, g1, b1 = canvas.winfo_rgb(color)
    # разложение цвета фона на составляющие ргб
    (r2, g2, b2) = canvas.winfo_rgb(bg_color)

    # получение шага интенсивности
    r_ratio = float(r2 - r1) / intensity
    g_ratio = float(g2 - g1) / intensity
    b_ratio = float(b2 - b1) / intensity

    for i in range(intensity):
        # заполнение массива разными оттенками
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))

        grad.append("#%4.4x%4.4x%4.4x" % (nr, ng, nb))

    grad.reverse()

    return grad


class BresenhamInt:
    """
    Класс алгоритма Брезенхема с целочисленными значениями
    """

    def __init__(self, point1: Point, point2: Point, stepmode: bool = False):
        """
        Инициализация атрибутов класса
        """
        self.point1: Point = point1
        self.point2: Point = point2
        self.stepmode = stepmode
        self.steps = 0
        self.points: list[Point] = list()

    def get_points_for_line(self, color_line, color_bg):
        """
        Метод получает массив точек для отрисовки линии
        """
        # флаг обмена приращений (пока не меняли)
        exchange = False

        # очищаем список, если уже строили
        self.points.clear()

        # определили длины линии по осям координат
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y

        # определили знак приращений по осям
        sx, sy = sign(dx), sign(dy)

        dx, dy = abs(dx), abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            exchange = True

        # понятие ошибки
        e = 2 * dy - dx

        # начальные значения
        x = self.point1.x
        y = self.point1.y

        # для подсчета количества ступенек
        xb = x
        yb = y

        for _ in range(round(dx) + 1):  # правильный диапазон
            # print(f"Bres_int: x = {x}, y = {y}")
            if not self.stepmode:
                self.points.append(Point(x, y, color_line))

            if e >= 0:
                if not exchange:
                    y += sy
                else:
                    x += sx

                e -= 2 * dx

            if not exchange:
                x += sx
            else:
                y += sy

            e += 2 * dy

            if self.stepmode:
                if xb != x and yb != y:
                    self.steps += 1
                xb = x
                yb = y

        if self.stepmode:
            return self.steps

        return self.points


class BresenhamFloat:
    """
    Класс алгоритма Брезенхема с действительными значениями
    """

    def __init__(self, point1: Point, point2: Point, stepmode: bool = False):
        """
        Инициализация атрибутов класса
        """
        self.point1: Point = point1
        self.point2: Point = point2
        self.stepmode = stepmode
        self.steps = 0
        self.points: list[Point] = list()

    def get_points_for_line(self, color_line, color_bg):
        """
        Метод получает массив точек для отрисовки линии
        """
        # флаг обмена приращений (пока не меняли)
        exchange = False

        # очищаем список, если уже строили
        self.points.clear()

        # определили длины линии по осям координат
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y

        # определили знак приращений по осям
        sx, sy = sign(dx), sign(dy)

        dx, dy = abs(dx), abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            exchange = True

        # понятие ошибки
        m = dy / dx  # тангенс угла наклона отрезка
        # удобнее анализировать знак ошибки, так истинное значение ошибки смещается на -0,5
        e = m - 0.5

        # начальные значения
        x = self.point1.x
        y = self.point1.y

        # для подсчета количества ступенек
        xb = x
        yb = y

        for _ in range(round(dx) + 1):  # правильный диапазон
            # print(f"Bres_float: x = {x}, y = {y}")
            if not self.stepmode:
                self.points.append(Point(x, y, color_line))

            if e >= 0:
                if not exchange:
                    y += sy
                else:
                    x += sx

                e -= 1  # отличие

            if not exchange:
                x += sx
            else:
                y += sy

            e += m  # отличие

            if self.stepmode:
                if xb != x and yb != y:
                    self.steps += 1
                xb = x
                yb = y

        if self.stepmode:
            return self.steps

        return self.points


class BresenhamElimAlias:
    """
    Класс алгоритма Брезенхема с устранением ступенчатости
    """

    def __init__(self, point1: Point, point2: Point, stepmode: bool = False):
        """
        Инициализация атрибутов класса
        """
        self.point1: Point = point1
        self.point2: Point = point2
        self.stepmode = stepmode
        self.steps = 0
        self.points: list[Point] = list()

    def get_points_for_line(self, color_line, color_bg):
        """
        Метод получает массив точек для отрисовки линии
        """
        # флаг обмена приращений (пока не меняли)
        exchange = False

        # очищаем список, если уже строили
        self.points.clear()

        # определили длины линии по осям координат
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y

        # определили знак приращений по осям
        sx, sy = sign(dx), sign(dy)

        dx, dy = abs(dx), abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            exchange = True

        intensity = 255
        fill = get_rgb_intensity(color_line, color_bg, intensity)

        # понятие ошибки
        m = dy / dx  # тангенс угла наклона отрезка
        e = 0.5 * intensity
        m *= intensity
        w = intensity - m

        # начальные значения
        x = self.point1.x
        y = self.point1.y

        # для подсчета количества ступенек
        xb = x
        yb = y

        for _ in range(round(dx) + 1):  # правильный диапазон
            # print(f"Bres_emit_alias: x = {x}, y = {y}")
            if not self.stepmode:
                self.points.append(Point(x, y, fill[round(e) - 1]))

            if e < w:
                if not exchange:
                    x += sx
                else:
                    y += sy

                e += m
            else:
                x += sx
                y += sy
                e -= w

            if self.stepmode:
                if xb != x and yb != y:
                    self.steps += 1
                xb = x
                yb = y

        if self.stepmode:
            return self.steps

        return self.points
