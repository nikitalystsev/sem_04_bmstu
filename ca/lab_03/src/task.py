from dataClass import DataInterp
from newton import NewtonThreeVar
from spline import SplineThreeVar
from mixed_interp import MixedInterpThreeVar


class Task:
    """
    Класс для решения поставленной задачи
    """

    def __init__(self, filename: str) -> None:
        """
        Инициализация атрибутов класса
        """
        self.data = DataInterp()

        self.data.read_x()
        self.data.read_y()
        self.data.read_z()
        self.data.read_data(filename)

        way_interp = self.choice_way_interp()
        self.interpolation(way_interp)

    def interp_newton(self) -> None:
        """
        Интерполяция полиномом Ньютона
        """
        self.data.read_nx()
        self.data.read_ny()
        self.data.read_nz()

        newton = NewtonThreeVar(
            self.data.x,
            self.data.y,
            self.data.z,
            self.data.x_s,
            self.data.y_s,
            self.data.z_s,
            self.data.values,
            self.data.nx,
            self.data.ny,
            self.data.nz
        )

        res_u = newton.interp_three_var()

        print(f"Интерполяция Ньютоном: u = {res_u}")

    def interp_spline(self) -> None:
        """
        Интерполяция сплайном
        """
        spline = SplineThreeVar(
            self.data.x,
            self.data.y,
            self.data.z,
            self.data.x_s,
            self.data.y_s,
            self.data.z_s,
            self.data.values,
        )

        res_u = spline.interp_three_var()

        print(f"Интерполяция Сплайнами: u = {res_u}")

    def interp_mixed(self) -> None:
        """
        Интерполяция полиномом Ньютона
        """
        self.print_info_mixed_interp()

        self.data.read_nx()
        self.data.read_nz()

        mixed_interp = MixedInterpThreeVar(
            self.data.x,
            self.data.y,
            self.data.z,
            self.data.x_s,
            self.data.y_s,
            self.data.z_s,
            self.data.values,
            self.data.nx,
            self.data.nz,
        )

        res_u = mixed_interp.interp_three_var()

        print(f"Смешанная интерполяция: u = {res_u}")

    @staticmethod
    def choice_way_interp() -> int:
        """
        Метод позволяет выбрать способ интерполяции
        """
        print("\nВыберите способ интерполяции:",
              "1. Полиномами Ньютона;",
              "2. Сплайнами;",
              "3. Смешанная интерполяция - по одному направлению сплайн, по другому - полином.",
              sep='\n')

        return int(input("Выберите пункт меню: "))

    @staticmethod
    def print_info_mixed_interp() -> None:
        """
        Метод выводит информацию о том, как производится смешанная интерполяция
        """
        print("\nСмешанная интерполяция работает следующим образом:",
              "- По X (количество значений Y раз) интерполяций проводится полиномами Ньютона;",
              "- Финальная интерполяция по Y производится сплайном;",
              "- Конечная одномерная интерполяция по Z проводится полиномом Ньютона.",
              sep='\n')

    def interpolation(self, way_interp: int) -> None:
        """
        Интерполяция
        """
        match way_interp:
            case 1:
                self.interp_newton()
            case 2:
                self.interp_spline()
            case 3:
                self.interp_mixed()
            case _:
                print("Неверный выбор пункта меню!")
