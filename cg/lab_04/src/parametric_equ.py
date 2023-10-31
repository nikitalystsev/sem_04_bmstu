import math as m
import numpy as np

from PointClass import Point


class ParametricCircle:
    """
    Класс алгоритма построения окружности на основе его параметрического  уравнения:
    { x = xc + r * cos(t)
    { y = yc + r * sin(t)
    1/8 окружности в методе create_circle, но симметричные точки дают полную окружность
    """

    def __init__(
            self,
            point_center: Point,  # центр окружности
            r: int | float,  # радиус окружности
    ):
        """
        Инициализация атрибутов класса
        """
        self._point_center: Point = point_center
        self._r: int | float = r

    def __get_symmetrical_points(self, point: Point, color: str) -> list[Point]:
        """
        Метод позволяет получить симметричные данной точке точки
        """
        x_c, y_c = self._point_center.x, self._point_center.y
        x, y = point.x, point.y

        list_point = list()

        list_point.append(Point(x=(y - y_c + x_c), y=(x - x_c + y_c), color=color))
        list_point.append(Point(x=(-y + y_c + x_c), y=(x - x_c + y_c), color=color))
        list_point.append(Point(x=(y - y_c + x_c), y=(-x + x_c + y_c), color=color))
        list_point.append(Point(x=(-y + y_c + x_c), y=(-x + x_c + y_c), color=color))
        list_point.append(Point(x=x, y=y, color=color))
        list_point.append(Point(x=(-x + 2 * x_c), y=y, color=color))
        list_point.append(Point(x=x, y=(-y + 2 * y_c), color=color))
        list_point.append(Point(x=(-x + 2 * x_c), y=(-y + 2 * y_c), color=color))

        return list_point

    def create_circle(self, color: str) -> list[Point]:
        """
        Метод для отображения окружности
        """
        x_c, y_c = self._point_center.x, self._point_center.y

        step = 1 / self._r

        points = list()
        for t in np.arange(0, m.pi / 4 + step, step):
            x = x_c + self._r * m.cos(t)
            y = y_c + self._r * m.sin(t)

            point = Point(x=x, y=y, color=color)

            list_point = self.__get_symmetrical_points(point, color)
            points.extend(list_point)

        return points


class ParametricEllipse:
    """
    Класс алгоритма построения эллипса на основе его параметрического уравнения:
    { x = xc + ra * cos(t)
    { y = yc + rb * sin(t)
    1\4 эллипса в методе create_ellipse, но симметричные точки дают полный эллипс
    """

    def __init__(
            self,
            point_center: Point,  # центр эллипса
            a: int | float,  # большая полуось
            b: int | float,  # малая полуось
    ):
        """
        Инициализация атрибутов класса
        """
        self._point_center: Point = point_center
        self._a: int | float = a
        self._b: int | float = b

    def __get_symmetrical_points(self, point: Point, color: str) -> list[Point]:
        """
        Метод позволяет получить симметричные данной точке точки
        """
        x_c, y_c = self._point_center.x, self._point_center.y
        x, y = point.x, point.y

        list_point = list()

        list_point.append(Point(x=x, y=y, color=color))
        list_point.append(Point(x=(-x + 2 * x_c), y=y, color=color))
        list_point.append(Point(x=x, y=(-y + 2 * y_c), color=color))
        list_point.append(Point(x=(-x + 2 * x_c), y=(-y + 2 * y_c), color=color))

        return list_point

    def create_ellipse(self, color: str) -> list[Point]:
        """
        Метод для отображения окружности
        """
        x_c, y_c = self._point_center.x, self._point_center.y

        step = 1 / self._a if self._a > self._b else 1 / self._b

        points = list()
        for t in np.arange(0, m.pi / 2 + step, step):
            x = x_c + self._a * m.cos(t)
            y = y_c + self._b * m.sin(t)

            point = Point(x=x, y=y, color=color)

            list_point = self.__get_symmetrical_points(point, color)
            points.extend(list_point)

        return points
