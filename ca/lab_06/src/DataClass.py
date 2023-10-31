import numpy as np
import math as m

SIZE_TABLE = 153


class DataClass:
    """
    Класс для представления данных функции в кратном интеграле
    """

    def __init__(self, file_name: str):
        """
        Инициализация атрибутов класса
        """
        self._file_name: str = file_name

        self._x_s: np.ndarray[int | float] = np.array(0)  # абсциссы
        self._y_s: np.ndarray[int | float] = np.array(0)  # ординаты
        self._z_s: np.ndarray[int | float] = np.array(0)  # матрица значений функции

        self.__read_table_two_dimen()  # считал данные из файла

        # матрица значений выравнивающих переменных: eta_s = ln z_s
        self._eta_s: np.ndarray[int | float] = self.__cacl_eta_s()

    @property
    def x(self) -> np.ndarray:
        """
        Метод позволяет получить значение аппликаты
        """

        return self._x_s

    @property
    def y(self) -> np.ndarray:
        """
        Метод позволяет получить значение аппликаты
        """

        return self._y_s

    @property
    def z(self) -> np.ndarray:
        """
        Метод позволяет получить значение аппликаты
        """

        return self._z_s

    @property
    def eta(self):
        """
        Метод позволяет получить значение выравнивающих переменных
        """

        return self._eta_s

    @staticmethod
    def __parse_str_by_sizes_matrix(sizes_str: str) -> (int | float, int | float):
        """
        Метод будет парсить строку и возвращать размеры матрицы значений функции
        """
        sizes = tuple(map(int, sizes_str.split()))
        print(f"Размеры матрицы значений функции под интегралом: {sizes[0]}x{sizes[1]}")

        return sizes

    def __read_table_two_dimen(self):
        """
        Метод будет парсить файл с таблицей функции от двух переменных
        """
        x_s, y_s = list(), list()

        file = open(self._file_name)
        lines = file.readlines()

        sizes = self.__parse_str_by_sizes_matrix(lines[0])  # размеры матрицы
        z_s = np.zeros(sizes)

        y_ind = 0

        for i in range(1, len(lines)):
            row = lines[i].split("\n")[0].split("\t")

            if "y\\x" in row[0]:  # запоминаем абсциссу
                if len(x_s) == 0:
                    for j in range(1, len(row)):
                        x_s.append(float(row[j]))
            else:  # запоминаем ординату и значения
                y_s.append(float(row[0]))

                for j in range(1, len(row)):
                    z_s[y_ind][j - 1] = float(row[j])
                y_ind += 1

        file.close()

        self._x_s, self._y_s, self._z_s = np.array(x_s), np.array(y_s), z_s

    def __cacl_eta_s(self):
        """
        Метод позволяет получить матрицу значений выравнивающих переменных
        """

        return np.array([[m.log(i) for i in zi] for zi in self.z])

    def table_value(self, x: int | float, y: int | float, use_eta=False):

        x_ind = list(self.x).index(x)
        y_ind = list(self.y).index(y)

        result = self.eta[y_ind][x_ind] if use_eta else self.z[y_ind][x_ind]

        return result

    def __str_row(self, y_ind: float, row_z: np.ndarray[int | float]):
        """
        Отображение данных
        """
        info_row_str = "|" + SIZE_TABLE * "-" + "|\n"

        info_row_str += f"|{self.y[y_ind]: ^10.4f}|"

        for val in row_z:
            info_row_str += f"{val: ^10.4f}|"

        info_row_str += '\n'

        return info_row_str

    def __str__(self):
        """
        Отображение данных
        """
        info_str = "\nТаблица с точками - узлами интерполяции:\n"

        info_str += "|" + SIZE_TABLE * "-" + "|\n"
        info_str += f'|{"y / x":^10s}|'

        for x in self.x:
            info_str += f"{x: ^10.4f}|"

        info_str += '\n'

        for i in range(len(self.z)):
            info_str += self.__str_row(i, self.z[i])

        info_str += "|" + SIZE_TABLE * "-" + "|"

        return info_str
