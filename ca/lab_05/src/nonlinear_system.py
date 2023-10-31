import numpy as np

from gauss import GaussMethod


class SystemNonlinearEqu:
    """
    Класс для решения систем нелинейных уравнений с помощью метода Ньютона
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """
        """
        система по тз:
        { x^2 + y^2 + z^2 = 1
        { 2 * x^2 + y^2 - 4 * z = 0
        { 3 * x^2 - 4 * y + z^2 = 0
        """

        """
        Алгоритм метода Ньютона для решения систем нелинейных уравнений:
        1. Задать начальное приближение var0.  он же x0
        2. Вычислить значение функции F(x0).
        3. Вычислить матрицу Якоби J(x0) функции F(x) в точке x0.
        4. Решить систему линейных уравнений J(x0) * Δx = -F(x0), где Δx - это вектор приращения x.
        5. Обновить приближение x1 = x0 + Δx.
        6. Если достигнуто условие остановки (например, сходимость по норме разности между x0 и x1), то остановиться. 
           Иначе, вернуться к шагу 2, используя x1 как новое начальное приближение.
        """
        # число в скобках, например, (0), обозначает номер итерации

        self._n: int = 3  # число уравнений, число неизвестных
        # вектор, в который будут записаны вычисленные значения при получении решения
        self._vector_solve: np.ndarray[float] = np.array(0)

    @staticmethod
    def __input_var0() -> np.ndarray[float]:
        """
        Метод, позволяющий ввести в строку через пробел
        начальное приближение для метода Ньютона
        """

        return np.array(list(map(float, input("\nВведите начальное приближение: ").split())))

    @staticmethod
    def __input_eps() -> float:
        """
        Метод, позволяющий ввести точность вычисления
        """

        return float(input("\nВведите требуемую точность: "))

    @staticmethod
    def __f1(vector_var: np.ndarray[int | float]) -> int | float:
        """
        Метод - первая функция системы от трех переменных
        """
        x, y, z = vector_var

        return x ** 2 + y ** 2 + z ** 2 - 1

    @staticmethod
    def __f2(vector_var: np.ndarray[int | float]) -> int | float:
        """
        Метод - вторая функция системы от трех переменных
        """
        x, y, z = vector_var

        return 2 * x ** 2 + y ** 2 - 4 * z

    @staticmethod
    def __f3(vector_var: np.ndarray[int | float]) -> int | float:
        """
        Метод - третья функция системы от трех переменных
        """
        x, y, z = vector_var

        return 3 * x ** 2 - 4 * y + z ** 2

    def __f(self, vector_var: np.ndarray[int | float]) -> np.ndarray[int | float]:
        """
        Метод, ака невязка, ака замена переменных для метода Ньютона
        """
        f_vector_var = np.array([
            self.__f1(vector_var),
            self.__f2(vector_var),
            self.__f3(vector_var)
        ])

        return f_vector_var

    @staticmethod
    def __get_slau_for_gauss(
            jacobian_matrix: np.ndarray,
            f_vector_var: np.ndarray
    ):
        """
        На каждой итерации метода Ньютона происходит решение системы уже линейных АУ
        А получать решение можно с помощью написанного мной же файла с методом Гаусса
        """
        slau = list()

        for i in range(len(jacobian_matrix)):
            tmp_row = list()
            tmp_row.extend(jacobian_matrix[i])
            tmp_row.append(f_vector_var[i])

            slau.append(tmp_row)

        return slau

    @staticmethod
    def __jacobian_matrix(vector_var: np.ndarray[int | float]) -> \
            np.ndarray[np.ndarray[int | float]]:
        """
        Метод позволяет получить матрицу Якоби для системы уравнений, заданной по тз
        """
        x, y, z = vector_var

        # матрица Якоби она же матрица первых частных производных
        jacobian_matrix = np.array([
            [2 * x, 2 * y, 2 * z],  # частные производные по каждой из переменных первой функции
            [4 * x, 2 * y, -4],  # частные производные по каждой из переменных второй функции
            [6 * x, -4, 2 * x]  # частные производные по каждой из переменных третьей функции
        ])

        return jacobian_matrix

    @staticmethod
    def __check_delta(dx: np.ndarray[int | float], eps: float):
        """
        Метод позволяет вычислить точность вычислений
        """
        abs_dx = np.absolute(dx)

        if max(abs_dx) <= eps:
            return True

        return False

    def __solve_by_newton(self, var0: np.ndarray[int | float], eps: float) -> int:
        """
        Метод позволяет получить решение системы уравнений, заданной по тз
        """
        self._vector_solve = var0

        count_iter = 0

        condition = True

        while condition:
            f_vector_var = self.__f(self._vector_solve)
            j_vector_var = self.__jacobian_matrix(self._vector_solve)

            slau = self.__get_slau_for_gauss(j_vector_var, -f_vector_var)
            dx = GaussMethod(slau).gauss()
            dx = np.array(dx)

            # dx = np.linalg.solve(j_vector_var, neg_f_vector_var)

            self._vector_solve += dx

            count_iter += 1

            if self.__check_delta(dx, eps):
                condition = False

            # if np.linalg.norm(dx) < eps:
            #     break

        return count_iter

    def get_solve(self):
        """
        Метод позволяет получить решение системы уравнений, заданной по тз
        """
        var0 = self.__input_var0()
        eps = self.__input_eps()

        count_iter = self.__solve_by_newton(var0, eps)

        self.__print_solve(count_iter)

    def __print_solve(self, count_iter: int) -> None:
        """
        Метод выводит результат - решение системы
        """
        if len(self._vector_solve) == 0:
            print(f"\nРешение системы нелинейных уравнений еще не было получено!")
            return

        print("\nРешение системы вида:")
        print(
            """
            { x^2 + y^2 + z^2 = 1
            { 2 * x^2 + y^2 - 4 * z = 0
            { 3 * x^2 - 4 * y + z^2 = 0
            """
        )
        print(f"было успешно получено: ",
              f"x = {self._vector_solve[0]}",
              f"y = {self._vector_solve[1]}",
              f"z = {self._vector_solve[2]}", sep='\n')

        print(f"Для вычисления корней системы потребовалось {count_iter} итераций")
