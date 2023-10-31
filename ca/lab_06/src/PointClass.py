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

    def __eq__(self, other: 'Point') -> bool:
        """
        Проверка на равенство точек
        """
        is_eq = \
            self._x == other._x and self._y == other._y and \
            self._z == other._z and self._color == self._color and \
            self._p == other._p

        return is_eq

    def __str__(self) -> str:
        """
        Вывод информации о точке в виде строки
        """
        return f"Point({self._x}, {self._y}, {self._y} {self._color}, {self._p})"

    def __repr__(self):
        """
        Вывод информации о точке в виде строки
        """
        return f"Point({self._x}, {self._y}, {self._y} {self._color}, {self._p})"

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
