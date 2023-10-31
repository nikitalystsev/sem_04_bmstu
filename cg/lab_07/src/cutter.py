from PointClass import Point


class Cutter:
    """
    Простенький класс для представления прямоугольного регулярного отсекателя
    """

    def __init__(self, point_top_left: Point, point_lower_right: Point = None):
        """
        Инициализация атрибутов класса
        """
        self._point_top_left: Point = point_top_left  # левая верхняя точка
        self._point_lower_right: Point = point_lower_right  # правая нижняя точка
        self._point_lower_left = None
        self._point_top_right = None

        if point_lower_right is not None:
            self._point_lower_left, self._point_top_right = self.calc_other()

    def calc_other(self) -> (Point, Point):
        """
        Метод позволяет вычислить оставшиеся точки регулярного отсекателя после получения
        правой нижней точки
        """
        # оставшиеся точки отсекателя
        point_lower_left: Point = Point(
            x=self._point_top_left.x,
            y=self._point_lower_right.y
        )

        point_top_right: Point = Point(
            x=self._point_lower_right.x,
            y=self._point_top_left.y
        )

        self._point_lower_left = point_lower_left
        self._point_top_right = point_top_right

        return point_lower_left, point_top_right

    @property
    def point_top_left(self) -> Point:
        """
        Метод позволяет получить значение начала отрезка
        """

        return self._point_top_left

    @point_top_left.setter
    def point_top_left(self, value: Point) -> None:
        """
        Метод позволяет изменить значение начала отрезка
        """
        self._point_top_left = value

    @property
    def point_lower_right(self) -> Point:
        """
        Метод позволяет получить значение начала отрезка
        """

        return self._point_lower_right

    @point_lower_right.setter
    def point_lower_right(self, value: Point) -> None:
        """
        Метод позволяет изменить значение начала отрезка
        """
        self._point_lower_right = value

    @property
    def point_lower_left(self) -> Point:
        """
        Метод позволяет получить значение начала отрезка
        """

        return self._point_lower_left

    @point_lower_left.setter
    def point_lower_left(self, value: Point) -> None:
        """
        Метод позволяет изменить значение начала отрезка
        """
        self._point_lower_left = value

    @property
    def point_top_right(self) -> Point:
        """
        Метод позволяет получить значение начала отрезка
        """

        return self._point_top_right

    @point_top_right.setter
    def point_top_right(self, value: Point) -> None:
        """
        Метод позволяет изменить значение начала отрезка
        """
        self._point_top_right = value
