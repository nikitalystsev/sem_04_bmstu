import numpy as np
from scipy.special import legendre


class Legendre:
    """
    Класс для полинома Лежандра n-й степени
    """

    @staticmethod
    def __polynom(n, x: int | float):
        """
        Вычисляет значение полинома Лежандра n-й степени в точке x.
        """
        if n == 0:
            return 1
        if n == 1:
            return x

        p0 = 1
        p1 = x

        for k in range(2, n + 1):
            p = ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            p0 = p1
            p1 = p

        return p1

    def roots(self, n, eps=1e-12, max_iter=100):
        """
        Находит корни полинома Лежандра n-й степени с помощью метода Ньютона.
        """
        roots = []
        m = int((n + 1) / 2)  # Количество корней

        for i in range(1, m + 1):
            x0 = np.cos(np.pi * (4 * i - 1) / (4 * n + 2))  # Начальное приближение

            for _ in range(max_iter):
                p = self.__polynom(n, x0)
                p_derivative = n * (self.__polynom(n - 1, x0) - x0 * p) / (1 - x0 ** 2)

                x1 = x0 - p / p_derivative

                if abs(x1 - x0) < eps:
                    roots.append(x1)
                    roots.append(-x1)
                    break

                x0 = x1

        if n % 2 != 0:  # почему-то добавляется лишний корень -0.0
            del roots[-1]

        return roots


# функция чисто для сравнения
def roots_legendre(n):
    """
    Находит корни полинома Лежандра n-й степени.
    """
    # Получение коэффициентов полинома Лежандра
    coeffs = legendre(n)

    # Нахождение корней полинома Лежандра
    roots = np.roots(coeffs)

    return roots
