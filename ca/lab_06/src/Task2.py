class Task2:
    """
    Класс для решения второй задачи лабораторной работы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        # прямиком из таблицы
        self._x_s: list[int | float] = [1, 2, 3, 4, 5, 6]
        self._y_s: list[int | float] = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]

    @staticmethod
    def __left_derivative(y1: int | float, y0: int | float, h: int | float) -> int | float:
        """
        Левая разностная производная
        """

        return (y1 - y0) / h

    @staticmethod
    def __center_derivative(y2: int | float, y0: int | float, h: int | float) -> int | float:
        """
        Центральная разностная производная
        """

        return (y2 - y0) / (2 * h)

    def __second_form_runge(self, y2: int | float, y1: int | float, y0: int | float, h: int | float):
        """
        Первая производная по второй формуле Рунге с использованием односторонней производной
        """
        der1 = self.__left_derivative(y2, y1, h)
        der2 = self.__left_derivative(y2, y0, 2 * h)

        return der1 + (der1 - der2) / (2 ** 1 - 1)

    def __align_vars(self):
        """
        Первая производная с введением выравнивающих переменных
        """
        eta = [1 / y for y in self._y_s]
        psi = [1 / x for x in self._x_s]

        eta_by_psi = [(eta[i + 1] - eta[i]) / (psi[i + 1] - psi[i]) for i in range(len(eta) - 1)]
        psi_by_x = [-(psi[i] / self._x_s[i]) for i in range(len(eta_by_psi))]
        eta_by_y = [-(eta[i] / self._y_s[i]) for i in range(len(eta_by_psi))]

        list_y_by_x = [eta_by_psi[i] * psi_by_x[i] / eta_by_y[i] for i in range(len(eta_by_psi))]

        return list_y_by_x

    @staticmethod
    def __second_der(y2: int | float, y1: int | float, y0: int | float, h: int | float):
        """
        Вторая разностная производная
        """

        return (y2 - 2 * y1 + y0) / (h ** 2)

    def __solve(self):
        """
        Метод, формирующий массивы решений второго задания
        """
        h = (self._x_s[1] - self._x_s[0])

        one_side_der = [self.__left_derivative(self._y_s[i], self._y_s[i - 1], h) for i in range(1, len(self._y_s))]

        center_der = [self.__center_derivative(self._y_s[i + 1], self._y_s[i - 1], h) for i in
                      range(1, len(self._y_s) - 1)]

        runge_der = [self.__second_form_runge(self._y_s[i], self._y_s[i - 1], self._y_s[i - 2], h) for i in
                     range(2, len(self._y_s))]

        align_der = self.__align_vars()

        second_dir = [self.__second_der(self._y_s[i - 1], self._y_s[i], self._y_s[i + 1], h) for i in
                      range(1, len(self._y_s) - 1)]


    def solve(self):
        """
        Метод обертка для получения решения
        """
        self.__solve()


tz = Task2()
tz.solve()
