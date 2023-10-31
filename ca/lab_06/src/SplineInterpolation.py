class SplineOneVar:
    """
    Сплайн
    """

    def __init__(
            self,
            x: int | float,
            data_table: list[tuple[int | float, int | float]]
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.x: int | float = x
        self.data_table = data_table

        self.a_n = list()
        self.b_n = list()
        self.c_n = list()
        self.d_n = list()

        self.h_n = list()
        self.ksi_n = list()
        self.theta_n = list()

        self.res = None

    def calc_a_n_coef(self) -> None:
        """
        Метод позволяет вычислить первые коэффициенты сплайна
        Формула 2
        """
        # очищаем список, если ранее уже были посчитаны первые коэффициенты
        self.a_n.clear()

        # в цикле в соответствии с формулой 2 определяется n-й первый коэффициент
        # сплайна и добавляется в список первых коэффициентов
        for n in range(0, len(self.data_table)):
            an = self.data_table[n][1]
            self.a_n.append(an)

    def calc_diff_h(self) -> None:
        """
        Метод вычисляет все разности между узлами таблицы
        интерполяции
        """
        # очищаем список, если ранее были уже посчитаны разности
        self.h_n.clear()

        # в цикле в соответствии с определением h как
        # разности аргументов в узлах таблицы интерполяции
        # вычисляем эти разности и добавляем в список разностей
        for n in range(1, len(self.data_table)):
            hn = self.data_table[n][0] - self.data_table[n - 1][0]
            self.h_n.append(hn)

    def calc_ksi_theta(self, ksi2: float, theta2: float) -> None:
        """
        Метод позволяет вычислить прогоночные коэффициенты кси и тета при прямом ходе
        в методе прогонки
        """
        if len(self.a_n) == 0:
            print("Первые коэффициенты сплайна еще не посчитаны")
            return

        if len(self.h_n) == 0:
            print("Разности еще не посчитаны")
            return

        # сначала очистим списки
        self.ksi_n.clear()
        self.theta_n.clear()

        # добавим None для соблюдения индексации, ведь при вычислении
        # прогоночных коэффициентов 2 <= n <= N, ноль добавляется потому,
        # что кси2 и тета2 равны нулю из условия С_1 равно ноль системы 12
        self.ksi_n.extend([None, ksi2])
        self.theta_n.extend([None, theta2])

        for n in range(1, len(self.data_table) - 1):  # правильный диапазон
            # считаем левый прогоночный коэффициент (правильно)
            ksin_plus_1 = -(self.h_n[n]) / (self.h_n[n - 1] * self.ksi_n[n] + 2 * (self.h_n[n - 1] + self.h_n[n]))

            # считаем правую часть уравнения системы (правильно)
            fn = 3 * ((self.a_n[n + 1] - self.a_n[n]) / self.h_n[n] -
                      (self.a_n[n] - self.a_n[n - 1]) / self.h_n[n - 1])

            # считаем правый прогоночный коэффициент (правильно)
            thetan_plus_1 = (fn - self.h_n[n - 1] * self.theta_n[n]) / \
                            (self.h_n[n - 1] * self.ksi_n[n] + 2 * (self.h_n[n - 1] + self.h_n[n]))

            # добавляем в списки коэффициентов
            self.ksi_n.append(ksin_plus_1)
            self.theta_n.append(thetan_plus_1)

    def calc_c_n_coef(self, cn_plus1: float) -> None:
        """
        Метод вычисляет коэффициенты С_n для сплайна по формуле 13
        в обратном ходе метода прогонки
        """
        if len(self.ksi_n) == 0 or len(self.theta_n) == 0:
            print("Прогоночные коэффициенты еще не были посчитаны!")
            return

        # сначала очищаю список коэффициентов С_n, если ранее они были посчитаны
        self.c_n.clear()

        # иду в цикле по прогоночным коэффициентам
        for n in range(len(self.ksi_n) - 2, -1, -1):  # правильный диапазон
            if n == len(self.ksi_n) - 2:
                # тут участвует cn+1
                cn = self.ksi_n[n + 1] * cn_plus1 + self.theta_n[n + 1]  # правильно
            else:
                # правильно
                cn = self.ksi_n[n + 1] * self.c_n[len(self.ksi_n) - 2 - n - 1] + self.theta_n[n + 1]

            self.c_n.append(cn)

        self.c_n.reverse()

    def calc_b_n_coef(self) -> None:
        """
        Метод вычисляет значения вторых
        коэффициентов кубического сплайна
        """
        if len(self.a_n) == 0 or len(self.h_n) == 0 or len(self.c_n) == 0:
            print("Не все посчитано для определения вторых коэффициентов!")
            return

        # сначала очищаю список коэффициентов B_n, если ранее они были посчитаны
        self.b_n.clear()

        for n in range(len(self.data_table) - 2):  # правильно
            bn = (self.a_n[n + 1] - self.a_n[n]) / self.h_n[n] - self.h_n[n] * ((self.c_n[n + 1] + 2 * self.c_n[n]) / 3)
            self.b_n.append(bn)

        n = len(self.data_table) - 2
        bn = (self.a_n[n + 1] - self.a_n[n]) / self.h_n[n] - self.h_n[n] * ((2 * self.c_n[n]) / 3)

        self.b_n.append(bn)

    def calc_d_n_coef(self) -> None:
        """
        Метод позволяет вычислить значения четвертых
        коэффициентов кубического сплайна
        """
        if len(self.c_n) == 0 or len(self.h_n) == 0:
            print("Не все посчитано для определения четвертых коэффициентов!")
            return

        # сначала очищаю список коэффициентов B_n, если ранее они были посчитаны
        self.d_n.clear()

        for n in range(len(self.data_table) - 2):
            dn = (self.c_n[n + 1] - self.c_n[n]) / (3 * self.h_n[n])
            self.d_n.append(dn)

        n = len(self.data_table) - 2
        dn = -(self.c_n[n] / (3 * self.h_n[n]))

        self.d_n.append(dn)

    def find_interval(self, x: float) -> tuple[int, int | float, int | float]:
        """
        Метод находит наиболее подходящий интервал для интерполируемого аргумента
        """
        # Шаг 2. Проверяем, находится ли значение x за пределами диапазона аргументов
        if x <= self.data_table[0][0]:
            return 0, self.data_table[0][0], self.data_table[1][0]
        elif x > self.data_table[-1][0]:
            return len(self.data_table) - 2, self.data_table[-2][0], self.data_table[-1][0]

        index = 0
        # Шаг 3. Ищем первый элемент в списке x, который больше value
        for i in range(len(self.data_table)):
            if self.data_table[i][0] >= x:
                index = i
                break

        # Шаг 5. Возвращаем номер интервала и информацию о границах этого интервала
        return index - 1, self.data_table[index - 1][0], self.data_table[index][0]

    def spline_interp(self, ksi2: float, theta2: float, cn_plus1: float) -> int | float:
        """
        Метод выполняет интерполяцию сплайном
        """
        self.calc_a_n_coef()
        self.calc_diff_h()
        self.calc_ksi_theta(ksi2, theta2)
        self.calc_c_n_coef(cn_plus1)
        self.calc_b_n_coef()
        self.calc_d_n_coef()

        num, x0, x1 = self.find_interval(self.x)

        self.res = \
            self.a_n[num] + self.b_n[num] * (self.x - x0) + self.c_n[num] * (self.x - x0) ** 2 + \
            self.d_n[num] * (self.x - x0) ** 3

        return self.res


class SplineTwoVar:
    """
    Класс для интерполяции сплайном функции от 2-х переменных
    """

    def __init__(
            self,
            x: int | float, y: int | float,
            x_s: list[int | float],
            y_s: list[int | float],
            values: list[list[int | float]],
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

        self.res = None

    # пусть двумерная интерполяция по x

    def __get_data_table_for_spline_one_var(
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
        Интерполяция сплайном по двум переменным
        """
        z_s_interp = list()

        for i in range(len(self.y_s)):
            data_table = self.__get_data_table_for_spline_one_var(i)
            spline = SplineOneVar(self.x, data_table)
            curr_z = spline.spline_interp(0, 0, 0)
            z_s_interp.append(curr_z)

        data_table = []

        for i in range(len(z_s_interp)):
            data_table.append((self.y_s[i], z_s_interp[i]))

        spline = SplineOneVar(self.y, data_table)

        self.res = spline.spline_interp(0, 0, 0)

        return self.res


