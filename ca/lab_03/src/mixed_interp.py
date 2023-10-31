from newton import NewtonOneVar
from spline import SplineOneVar


class MixedInterpTwoVar:
    """
    Класс смешанной интерполяции функции от 2-х переменных
    """

    def __init__(
            self,
            x: int | float, y: int | float,
            x_s: list[int | float],
            y_s: list[int | float],
            values: list[list[int | float]],
            nx: int,
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        # точка интерполирования
        self.x: int | float = x
        self.y: int | float = y

        # значения
        self.x_s: list[int | float] = x_s
        self.y_s: list[int | float] = y_s
        self.values: list[list[int | float]] = values

        # степени полиномов
        self.nx: int = nx

        self.res = None

    # пусть двумерная интерполяция по X
    # по X (количество значений Y раз) интерполяций проводится полиномами Ньютона
    # финальная интерполяция по Y производится сплайном

    def __get_data_table_for_newton_one_var(
            self,
            ind_y: int
    ) -> list[tuple[int | float, int | float]]:
        """
        Метод позволяет получить таблицу при фиксированном y,
        зависимости x от значения функции от 2-х переменных
        """
        data_table = []

        for j in range(len(self.x_s)):
            f_x_jy = self.values[ind_y][j]
            x_j = self.x_s[j]
            data_table.append((x_j, f_x_jy))

        return data_table

    def interp_two_var(self) -> int | float:
        """
        Интерполяция по двум переменным
        """
        z_s_interp = list()

        for i in range(len(self.y_s)):
            data_table = self.__get_data_table_for_newton_one_var(i)
            newton = NewtonOneVar(self.x, data_table, self.nx)
            curr_z = newton.newton_polynom()
            z_s_interp.append(curr_z)

        data_table = []

        for i in range(len(z_s_interp)):
            data_table.append((self.y_s[i], z_s_interp[i]))

        spline = SplineOneVar(self.y, data_table)

        self.res = spline.spline_interp(0, 0, 0)

        return self.res


class MixedInterpThreeVar:
    """
    Класс смешанной интерполяции функции от 3-х переменных
    """

    def __init__(
            self,
            x: int | float, y: int | float, z: int | float,
            x_s: list[int | float],
            y_s: list[int | float],
            z_s: list[int | float],
            values: list[list[list[int | float]]],
            nx: int,
            nz: int,
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        # точка интерполирования
        self.x: int | float = x
        self.y: int | float = y
        self.z: int | float = z

        # значения
        self.x_s: list[int | float] = x_s
        self.y_s: list[int | float] = y_s
        self.z_s: list[int | float] = z_s
        self.values: list[list[list[int | float]]] = values

        # степени полиномов
        self.nx: int = nx
        self.nz: int = nz

        self.res = None

    def interp_three_var(self) -> int | float:
        """
        Интерполяция сплайном по трем переменным
        """
        u_s_interp = list()

        for i in range(len(self.z_s)):
            spline = MixedInterpTwoVar(self.x, self.y, self.x_s, self.y_s, self.values[i], self.nx)
            curr_u = spline.interp_two_var()
            u_s_interp.append(curr_u)

        data_table = []

        for i in range(len(u_s_interp)):
            data_table.append((self.z_s[i], u_s_interp[i]))

        newton = NewtonOneVar(self.z, data_table, self.nz)

        self.res = newton.newton_polynom()

        return self.res
