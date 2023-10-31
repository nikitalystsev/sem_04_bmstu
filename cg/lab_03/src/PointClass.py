class Point:
    """
    Точка
    """

    def __init__(self, x, y, color):
        """
        Инициализация атрибутов класса
        """
        self.x = x
        self.y = y
        self.color = color

    def __eq__(self, other):
        """
        Проверка на равенство точек
        """

        return self.x == other.x and self.y == other.y
