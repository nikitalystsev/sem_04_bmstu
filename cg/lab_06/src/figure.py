import copy as cp

from PointClass import Point


class Figure:
    """
    Класс для представления произвольной многоугольной области на холсте
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """
        self._list_points: list[Point] = list()  # список точек, из которых состоит фигура
        self.is_close = False  # флаг замкнутости фигуры

    def __getitem__(self, item) -> Point:
        """
        Магический метод для обращения по индексу
        """
        if 0 <= item < len(self._list_points):
            return cp.deepcopy(self._list_points[item])
        else:
            raise IndexError("Индекс за границами нашей коллекции!")

    def __len__(self) -> int:
        """
        Магический метод позволяет получить количество точек, из которых состоит фигура
        """

        return len(self._list_points)

    def __str__(self) -> str:
        """
        Магический метод для отображения фигуры в консоли для пользователя
        """
        info_string = f"Список точек (их {len(self)}):\n"

        for point in self._list_points:
            info_string += f"x = {point.x}, y = {point.y}\n"

        return info_string

    def add_point(self, point: Point) -> None:
        """
        Метод для добавления новой точки к фигуре
        """
        self._list_points.append(point)

    def clean(self) -> None:
        """
        Метод позволяет очистить все данные о фигуре
        """
        self._list_points.clear()
        self.is_close = False
