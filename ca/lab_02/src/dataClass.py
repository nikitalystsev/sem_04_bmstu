SIZE_TABLE = 31


class Point:
    """
    Точка
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        Инициализация атрибутов класса
        """
        self.x = x
        self.y = y


class Data:
    """
    Данные для интерполяции
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self.data_table: list[Point] = list()
        self.x = None

    def read_data(self, filename: str) -> None:
        """
        Метод считывает данные из файла
        """
        with open(filename) as file:
            for line in file:
                data = list(map(float, line.split()))
                point = Point(data[0], data[1])
                self.data_table.append(point)

    def read_x(self) -> None:
        """
        Функция считывает значение аргумента x, для которого выполняется интерполяция
        """
        if self.x is None:
            self.x = float(input("Введите значение аргумента x, "
                                 "для которого выполняется интерполяция: "))

    def set_x(self, x: float):
        """
        Метод устанавливает значение аргумента интерполяции
        """
        self.x = x

    def get_data_table(self):
        """
        Метод возвращает таблицу с точками
        """

        return self.data_table

    def get_x(self):
        """
        Метод возвращает точку интерполирования
        """

        return self.x

    def del_data(self) -> None:
        """
        Метод позволяет удалить данные для интерполяции
        """
        self.data_table.clear()
        self.x = None

    def print_data_table(self):
        """
        Метод выводит данные на экран
        """
        if len(self.data_table) == 0:
            print("Таблица с точками еще не была получена!")
            return

        print("\nТаблица с точками - узлами интерполяции:")
        print("|" + SIZE_TABLE * "-" + "|")
        print(f"|{'x':^15s}|{'y':^15s}|")
        print("|" + SIZE_TABLE * "-" + "|")

        for point in self.data_table:
            print("| {:^13.3f} | {:^13.3f} |".format(
                point.x,
                point.y)
            )

        print("|" + SIZE_TABLE * "-" + "|")

    def print_x(self):
        """
        Метод выводит аргумент интерполирования
        """
        if self.x is None:
            print("Точка интерполирования еще не была получена!")
            return

        print(f"\nТочка интерполирования x = {self.x: <15.3f}")
