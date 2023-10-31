class Point:
    """
    Точка
    """

    def __init__(
            self,
            x: int | float,
            y: int | float,
            z: int | float = 0,
            color: str = 'red',
            p: int | float = 1,
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._x: int | float = x
        self._y: int | float = y
        self._z: int | float = z
        self._color: str = color
        self._p: int | float = p

    def __str__(self) -> str:
        """
        Вывод информации о точке в виде строки
        """
        return f"Point({self._x: .3f}, {self._y: .3f})"

    def __eq__(self, other: 'Point'):
        """
        Проверка на равенство точек
        """
        is_eq = \
            self._x == other._x and self._y == other._y and \
            self._z == other._z and self._color == self._color and \
            self._p == other._p

        if isinstance(other, Point):
            return is_eq
        else:
            raise TypeError("Неподдерживаемый операнд для операции '=='")

    def __ne__(self, other: 'Point'):
        """
        Не равно
        """
        if isinstance(other, Point):
            return (self.x != other.x) or (self.y != other.y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '!='")

    def __add__(self, other: 'Point'):
        """
        Сложение двух точек
        """
        if isinstance(other, Point):
            new_x = self.x + other.x
            new_y = self.y + other.y
            return Point(new_x, new_y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '+'")

    def __truediv__(self, divisor: int | float):
        """
        Деление точки на число
        """
        if isinstance(divisor, (int, float)):
            new_x = self.x / divisor
            new_y = self.y / divisor
            return Point(new_x, new_y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '/'")

    def __gt__(self, other: 'Point'):
        """
        Больше
        """
        if isinstance(other, Point):
            return (self.x > other.x) and (self.y > other.y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '>'")

    def __lt__(self, other: 'Point'):
        """
        Меньше
        """
        if isinstance(other, Point):
            return (self.x < other.x) and (self.y < other.y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '<'")

    def __ge__(self, other: 'Point'):
        """
        Больше либо равно
        """
        if isinstance(other, Point):
            return (self.x >= other.x) and (self.y >= other.y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '>='")

    def __le__(self, other: 'Point'):
        """
        Меньше либо равно
        """
        if isinstance(other, Point):
            return (self.x <= other.x) and (self.y <= other.y)
        else:
            raise TypeError("Неподдерживаемый операнд для операции '<='")

    @property
    def x(self) -> int | float:
        """
        Метод позволяет получить значение абсциссы
        """

        return self._x

    @x.setter
    def x(self, value: int | float) -> None:
        """
        Метод позволяет изменить значение абсциссы
        """
        self._x = value

    @property
    def y(self) -> int | float:
        """
        Метод позволяет получить значение ординаты
        """

        return self._y

    @y.setter
    def y(self, value: int | float) -> None:
        """
        Метод позволяет изменить значение ординаты
        """
        self._y = value

    @property
    def z(self) -> int | float:
        """
        Метод позволяет получить значение аппликаты
        """

        return self._z

    @z.setter
    def z(self, value: int | float) -> None:
        """
        Метод позволяет изменить значение аппликаты
        """
        self._z = value

    @property
    def color(self) -> str:
        """
        Получение цвета точки
        """

        return self._color

    @color.setter
    def color(self, color: str) -> None:
        """
        Изменение цвета точки
        """
        self._color = color

    @property
    def p(self) -> int | float:
        """
        Получение веса точки
        """

        return self._p

    @p.setter
    def p(self, value: int | float) -> None:
        """
        Изменение веса точки
        """
        self._p = value

    def info(self) -> None:
        """
        Вывод данных о точке
        """
        print(f"Координаты: ({self._x}, {self._y}, {self._z})",
              f"Цвет: {self._color}",
              f"Вес:  {self._p}",
              sep='\n')
