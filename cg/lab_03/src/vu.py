import tkinter as tk
import math

from PointClass import *


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


class Vu:
    """
    Класс алгоритма Ву
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
        # очищаем список, если уже строили
        self.points.clear()

        intensity = 255
        fill = get_rgb_intensity(color_line, color_bg, intensity)

        steep = abs(self.point2.y - self.point1.y) > abs(self.point2.x - self.point1.x)

        if steep:
            self.point1.x, self.point1.y = self.point1.y, self.point1.x
            self.point2.x, self.point2.y = self.point2.y, self.point2.x

        if self.point1.x > self.point2.x:
            self.point1.x, self.point2.x = self.point2.x, self.point1.x
            self.point1.y, self.point2.y = self.point2.y, self.point1.y

        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y

        m = dy / dx if dx else 1

        # первая точка (начальная)
        xend = round(self.point1.x)
        yend = self.point1.y + m * (xend - self.point1.x)
        # xgap = 1 - math.modf(self.point1.x + 0.5)[0]
        xpxl1 = xend
        ypxl1 = math.floor(yend)
        if not self.stepmode:
            self.points.append(Point(xpxl1, ypxl1, color_line))

        # вторая точка (конечная)
        xend = round(self.point2.x)
        yend = self.point2.y + m * (xend - self.point2.x)
        # xgap = math.modf(self.point2.x + 0.5)[0]
        xpxl2 = xend
        ypxl2 = math.floor(yend)

        intery = self.point1.y + m

        # основной цикл
        for x in range(xpxl1 + 1, xpxl2):
            if steep:
                first = Point(math.floor(intery), x,
                              fill[round((intensity - 1) * (abs(1 - intery + math.floor(intery))))])
                second = Point(math.floor(intery) + 1, x,
                               fill[round((intensity - 1) * (abs(intery - math.floor(intery))))])
            else:
                first = Point(x, math.floor(intery),
                              fill[round((intensity - 1) * (abs(1 - intery + math.floor(intery))))])
                second = Point(x, math.floor(intery) + 1,
                               fill[round((intensity - 1) * (abs(intery - math.floor(intery))))])

            if not self.stepmode:
                self.points.append(first)
                self.points.append(second)
            elif x < round(self.point2.x) and int(intery) != int(intery + m):
                self.steps += 1

            intery += m

        if not self.stepmode:
            self.points.append(Point(xpxl2, ypxl2, color_line))

        # for point in self.points:
        #     print(f"Vu: x = {point.x}, y = {point.y}")

        if self.stepmode:
            return self.steps

        return self.points
