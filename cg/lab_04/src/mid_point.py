import math as m

from PointClass import Point


class MidPointAlgCircle:
    """
    Класс алгоритма построения окружности алгоритмом средней точки
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

        x, y = self._r, 0

        points = list()

        point = Point(x=(x_c + x), y=(y_c + y), color=color)

        list_points = self.__get_symmetrical_points(point, color)
        points.extend(list_points)
        # points.extend([point])

        # F(X, Y) = X^2 + Y^2 - R^2 - параметр принятия решения, это и есть delta_i
        delta_i = 1 - self._r  # начальное значение исходя из подставляемой точки

        while x >= y:
            if delta_i < 0:  # если точка внутри окружности, то след. точка (X + 1 , Y)
                y += 1
                delta_i += 2 * y + 1
            else:  # иначе следующей точкой на окружности будет (X + 1, Y – 1)
                y += 1
                x -= 1
                delta_i += 2 * y + 1 - 2 * x

            point = Point(x=(x_c + x), y=(y_c + y), color=color)

            list_points = self.__get_symmetrical_points(point, color)
            points.extend(list_points)
            # points.extend([point])

        return points


class MidPointAlgEllipse:
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

        border_x = round(self._a / m.sqrt(1 + b_squared / a_squared))
        delta_i = b_squared - a_squared * (self._b - 1 / 4)

        while x <= border_x:
            if delta_i < 0:
                x += 1
                delta_i += 2 * b_squared * x
            else:
                x += 1
                y -= 1
                delta_i += 2 * b_squared * x - 2 * a_squared * y

            point = Point(x=(x_c + x), y=(y_c + y), color=color)

            list_points = self.__get_symmetrical_points(point, color)
            points.extend(list_points)

        x, y = self._a, 0

        border_y = round(self._b / m.sqrt(1 + a_squared / b_squared))
        delta_i = a_squared - b_squared * (self._a - 1 / 4)

        point = Point(x=(x_c + x), y=(y_c + y), color=color)

        list_points = self.__get_symmetrical_points(point, color)
        points.extend(list_points)

        while y <= border_y:
            if delta_i < 0:
                y += 1
                delta_i += 2 * a_squared * y
            else:
                x -= 1
                y += 1
                delta_i += 2 * a_squared * y - 2 * b_squared * x

            point = Point(x=(x_c + x), y=(y_c + y), color=color)

            list_points = self.__get_symmetrical_points(point, color)
            points.extend(list_points)

        return points
