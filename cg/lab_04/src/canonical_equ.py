import math as m

from PointClass import Point


class CanonicalCircle:
    """
    Класс алгоритма построения окружности на основе его канонического уравнения вида:
    (x - xc) ** 2 + (y - yc) ** 2 = R**2
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

        # описание симметричных точек такое, будто не экранные, а обычные оси
        list_point.append(Point(x=x, y=y, color=color))  # сама точка
        # симметрия относительно вертикальной оси, тобишь x = xc
        list_point.append(Point(x=(-x + 2 * x_c), y=y, color=color))
        # симметрия относительно горизонтальной оси, тобишь y = yc
        list_point.append(Point(x=x, y=(-y + 2 * y_c), color=color))

        # симметрия относительно прямой, идущей под углом 45 градусов к оси абсцисс
        list_point.append(Point(x=(y - y_c + x_c), y=(x - x_c + y_c), color=color))
        # симметрия прямой, идущей под углом 135 градусов к оси абсцисс
        list_point.append(Point(x=(-y + y_c + x_c), y=(x - x_c + y_c), color=color))
        # симметрия прямой, идущей под углом 225 градусов к оси абсцисс
        list_point.append(Point(x=(y - y_c + x_c), y=(-x + x_c + y_c), color=color))
        # симметрия прямой, идущей под углом 315 градусов к оси абсцисс
        list_point.append(Point(x=(-y + y_c + x_c), y=(-x + x_c + y_c), color=color))
        # симметрия относительно центра окружности
        list_point.append(Point(x=(-x + 2 * x_c), y=(-y + 2 * y_c), color=color))

        return list_point

    def create_circle(self, color: str) -> list[Point]:
        """
        Метод для отображения окружности
        """
        r_squared = self._r ** 2
        x_c, y_c = self._point_center.x, self._point_center.y

        # находим область определения x для 1/8 окружности
        border_x = round(x_c + self._r / m.sqrt(2))

        points = list()

        for x in range(round(x_c), border_x + 1):  # включая границу
            # y = yc + sqrt(R**2 - (x - xc)**2)
            y = y_c + m.sqrt(r_squared - (x - x_c) ** 2)

            point = Point(x=x, y=y, color=color)

            list_point = self.__get_symmetrical_points(point, color)
            points.extend(list_point)

        return points


class CanonicalEllipse:
    """
    Класс алгоритма построения эллипса на основе его канонического уравнения вида:
    (x - xc) ** 2 / (a ** 2) + (y - yc) ** 2 / (b ** 2) = 1
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
        Метод для отображения эллипса
        """
        a_squared = self._a ** 2
        b_squared = self._b ** 2

        x_c, y_c = self._point_center.x, self._point_center.y

        border_x = round(x_c + self._a / m.sqrt(1 + b_squared / a_squared))
        border_y = round(y_c + self._b / m.sqrt(1 + a_squared / b_squared))

        points = list()

        for x in range(round(x_c), border_x + 1):  # большая часть полуоси
            y = y_c + m.sqrt(a_squared * b_squared - (x - x_c) ** 2 * b_squared) / self._a

            point = Point(x=x, y=y, color=color)

            list_point = self.__get_symmetrical_points(point, color)
            points.extend(list_point)

        for y in range(border_y, round(y_c) - 1, -1):  # малая часть полуоси
            x = x_c + m.sqrt(a_squared * b_squared - (y - y_c) ** 2 * a_squared) / self._b

            point = Point(x=x, y=y, color=color)

            list_point = self.__get_symmetrical_points(point, color)
            points.extend(list_point)

        return points
