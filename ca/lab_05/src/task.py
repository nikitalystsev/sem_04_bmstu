from nonlinear_system import SystemNonlinearEqu
from laplace_func_half_div import LaplaceFuncHalfDiv
from laplace_func_newton import LaplaceFuncNewton
from diff_equ_sweep import DiffEquSweep


class Task:
    """
    Класс для решения поставленной задачи
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """

        self.__handler()

    @staticmethod
    def __get_solve_system():
        """
        Метод обертка для системы нелинейных уравнений
        """
        system = SystemNonlinearEqu()
        system.get_solve()

    @staticmethod
    def __get_solve_laplace():
        """
        Метод обертка для решения пункта тз с функцией Лапласа
        """
        laplace = LaplaceFuncHalfDiv()
        laplace.get_solve_x()

    @staticmethod
    def __get_solve_laplace_newton():
        """
        Метод обертка для решения пункта тз с функцией Лапласа
        """
        laplace = LaplaceFuncNewton()
        laplace.get_solve_x()

    @staticmethod
    def __get_solve_diff_equ():
        """
        Метод обертка для решения пункта тз с краевой задачей
        """
        diff_equ = DiffEquSweep()
        diff_equ.get_solve_and_plot()

    @staticmethod
    def __print_menu() -> None:
        """
        Метод выводит меню взаимодействия с программой
        """
        print("\nМеню взаимодействия с программой:")
        print("1. Найти решение системы уравнений;",
              "2. Найти значение аргумента функции Лапласа по ее значению;",
              "3. Найти значение аргумента функции Лапласа по ее значению c использованием метода Ньютона;",
              "4. Найти решение краевой задачи;",
              sep='\n')

    @staticmethod
    def __choose_menu_item() -> int:
        """
        Метод для выбора пункта меню
        """

        return int(input("\nВведите пункт меню: "))

    def __handler(self) -> None:
        """
        Метод для обработки действий пользователя
        """

        while True:

            self.__print_menu()
            menu_item = self.__choose_menu_item()

            match menu_item:
                case 1:
                    self.__get_solve_system()
                case 2:
                    self.__get_solve_laplace()
                case 3:
                    self.__get_solve_laplace_newton()
                case 4:
                    self.__get_solve_diff_equ()
                case _:
                    print("Неверный пункт меню!")
                    return
