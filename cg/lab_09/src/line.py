from PointClass import Point


class Line:
    """
    Простенький класс для представления линии
    """

    def __init__(self, point_start: Point, point_end: Point = None):
        """
        Инициализация атрибутов класса
        """
        self._point_start: Point = point_start
        self._point_end: Point = point_end

    @property
    def point_start(self) -> Point:
        """
        Метод позволяет получить значение начала отрезка
        """

        return self._point_start

    @point_start.setter
    def point_start(self, value: Point) -> None:
        """
        Метод позволяет изменить значение начала отрезка
        """
        self._point_start = value

    @property
    def point_end(self) -> Point:
        """
        Метод позволяет получить значение конца отрезка
        """

        return self._point_end

    @point_end.setter
    def point_end(self, value: Point) -> None:
        """
        Метод позволяет изменить значение конца отрезка
        """
        self._point_end = value

    def __str__(self):
        """
        Вывод на экран
        """
        return f"Ребро: {self._point_start}, {self.point_end}"
