from MultipleIntegral import MultipleIntegral


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
    def __calc_multiple_integral() -> None:
        """
        Метод обертка для вычисления кратного интеграла
        """
        multiple_integral = MultipleIntegral()
        multiple_integral.integral()

    @staticmethod
    def __print_menu() -> None:
        """
        Метод выводит меню взаимодействия с программой
        """
        print("\nМеню взаимодействия с программой:")
        print("1. Найти значение кратного интеграла;",

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
                    self.__calc_multiple_integral()
                case _:
                    print("Неверный пункт меню!")
                    return
