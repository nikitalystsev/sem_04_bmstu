import numpy as np

SIZE_TABLE = 65


class DataInterp:
    """
    Данные для интерполяции
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """
        # точка интерполирования
        self.x = None
        self.y = None
        self.z = None

        # степени возможных полиномов
        self.nx = None
        self.ny = None
        self.nz = None

        self.x_s: list = list()  # массив абсцисс
        self.y_s: list = list()  # массив ординат
        self.z_s: list = list()  # массив аппликат
        self.values = None  # трехмерная матрица значений

    def clear_data(self) -> None:
        """
        Метод очищает все данные
        """
        self.x_s.clear()
        self.y_s.clear()
        self.z_s.clear()
        self.values = None

    def is_empty_all(self) -> bool:
        """
        Метод проверяет, были ли уже собраны данные для интерполяции
        """
        is_empty = \
            len(self.x_s) == 0 and len(self.y_s) == 0 and \
            len(self.z_s) == 0 and self.values is None

        return is_empty

    def read_x(self) -> None:
        """
        Функция считывает значение абсциссы интерполирования
        """
        if self.x is None:
            self.x = float(input("Введите значение абсциссы интерполирования x: "))

    def read_y(self) -> None:
        """
        Функция считывает значение ординаты интерполирования
        """
        if self.y is None:
            self.y = float(input("Введите значение ординаты интерполирования y: "))

    def read_z(self) -> None:
        """
        Функция считывает значение аппликаты интерполирования
        """
        if self.z is None:
            self.z = float(input("Введите значение аппликаты интерполирования z: "))

    def read_nx(self) -> None:
        """
        Функция считывает значение абсциссы интерполирования
        """
        if self.nx is None:
            self.nx = int(input("Введите степень полинома по оси x: "))

    def read_ny(self) -> None:
        """
        Функция считывает значение ординаты интерполирования
        """
        if self.ny is None:
            self.ny = int(input("Введите степень полинома по оси y: "))

    def read_nz(self) -> None:
        """
        Функция считывает значение аппликаты интерполирования
        """
        if self.nz is None:
            self.nz = int(input("Введите степень полинома по оси z: "))

    def read_data(self, filename: str) -> None:
        """
        Метод считывает данные из файла
        """

        # очищаем данные, если уже получали
        self.clear_data()

        with open(filename) as file:
            is_add_y = False
            y_ind, z_ind = 0, 0

            for ind, line in enumerate(file):
                if ind == 0:  # считали размеры трехмерной матрицы
                    sizes = tuple(map(int, line.split()))
                    self.values = np.zeros(sizes)
                    continue

                row = line.split("\n")[0].split("\t")

                if 'z=' in row[0]:  # запоминаем аппликату
                    z_value = float(row[0].replace('z=', ''))
                    self.z_s.append(z_value)
                elif "y\\x" in row[0]:  # запоминаем абсциссу
                    if len(self.x_s) == 0:
                        for i in range(1, len(row)):
                            self.x_s.append(float(row[i]))
                else:  # запоминаем ординату и значение
                    if not row[0].isdigit():
                        y_ind = 0
                        z_ind += 1
                        is_add_y = True
                        continue

                    if not is_add_y:
                        self.y_s.append(float(row[0]))

                    for i in range(1, len(row)):
                        self.values[z_ind][y_ind][i - 1] = float(row[i])
                    y_ind += 1

    def __print_part_data_table(self, z_ind: float, z: int | float) -> None:
        """
        Метод выводит часть таблицы значений
        """
        print("|" + 15 * "-" + "|")
        print(f"| z = {z:^10.3f}|")

        print("|" + SIZE_TABLE * "-" + "|")
        print(f'|{"y / x":^10s}|', end='')

        for x in self.x_s:
            print(f"{x: ^10.3f}|", end='')

        print("\n|" + SIZE_TABLE * "-" + "|", end='')

        for i in range(len(self.values[z_ind])):

            print(f"\n|{self.y_s[i]: ^10.3f}|", end='')
            for val in self.values[z_ind][i]:
                print(f"{val: ^10.3f}|", end='')
            print("\n|" + SIZE_TABLE * "-" + "|", end='')

        print("\n")

    def print_data_table(self) -> None:
        """
        Метод выводит данные на экран
        """
        if self.is_empty_all():
            print("Таблица с точками еще не была получена!")
            return

        print("\nТаблица с точками - узлами интерполяции:")

        for i in range(len(self.values)):
            self.__print_part_data_table(i, self.z_s[i])
