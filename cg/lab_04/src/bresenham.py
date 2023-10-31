from PointClass import *


class BresenhamCircle:
    """
    Класс алгоритма Брезенхема для построения окружности
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

        x, y = 0, self._r

        points = list()

        point = Point(x=(x_c + x), y=(y_c + y), color=color)

        list_points = self.__get_symmetrical_points(point, color)
        points.extend(list_points)

        delta_i = 2 * (1 - self._r)  # начальное значение

        while y >= x:
            d1 = 2 * (delta_i + y) - 1
            x += 1

            if d1 >= 0:
                y -= 1
                delta_i += 2 * (x - y + 1)
            else:
                delta_i += 2 * x + 1

            point = Point(x=(x_c + x), y=(y_c + y), color=color)

            list_points = self.__get_symmetrical_points(point, color)
            points.extend(list_points)

        return points


class BresenhamEllipse:
    """
    Класс алгоритма Брезенхема для построения эллипса
    1/4 части
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
        Метод для отображения эллипса
        """
        x_c, y_c = self._point_center.x, self._point_center.y

        x, y = 0, self._b

        points = list()

        point = Point(x=(x_c + x), y=(y_c + y), color=color)

        list_points = self.__get_symmetrical_points(point, color)
        points.extend(list_points)

        a_squared, b_squared = self._a ** 2, self._b ** 2
        delta_i = b_squared - a_squared * (2 * self._b + 1)

        while y >= 0:
            if delta_i < 0:
                d1 = 2 * delta_i + a_squared * (2 * y + 2)
                x += 1
                if d1 < 0:
                    delta_i += b_squared * (2 * x + 1)
                else:
                    y -= 1
                    delta_i += b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)
            elif delta_i > 0:
                d2 = 2 * delta_i + b_squared * (2 - 2 * x)
                y -= 1
                if d2 > 0:
                    delta_i += a_squared * (1 - 2 * y)
                else:
                    x += 1
                    delta_i += b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)
            else:
                x += 1
                y -= 1
                delta_i += b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)

            point = Point(x=(x_c + x), y=(y_c + y), color=color)

            list_points = self.__get_symmetrical_points(point, color)
            points.extend(list_points)

        return points
