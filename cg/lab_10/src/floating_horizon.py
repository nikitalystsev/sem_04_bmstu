from typing import Callable
from tkinter import Canvas
import math as m


class FloatingHorizon:
    """
    Класс для представления и реализации алгоритма плавающего горизонта
    """

    def __init__(
            self,
            canvas: Canvas,
            border_x: list[int | float, int | float],
            border_z: list[int | float, int | float],
            x_step: int | float,
            z_step: int | float,
            func: Callable[[int | float, int | float], int | float],
            angle_x: int | float,
            angle_y: int | float,
            angle_z: int | float

    ):
        """
        Инициализация атрибутов класса
        """
        self._canvas: Canvas = canvas
        self._border_x: list[int | float, int | float] = border_x
        self._border_z: list[int | float, int | float] = border_z
        self._x_step: int | float = x_step
        self._z_step: int | float = z_step
        self._func: Callable[[int | float, int | float], int | float] = func
        self._angle_x: int | float = angle_x
        self._angle_y: int | float = angle_y
        self._angle_z: int | float = angle_z

        self._angles: list[int | float] = [self._angle_x, self._angle_y, self._angle_z]

        # 1520 - ширина холста plane, 1010 - высота холста plane
        # Инициализируем начальными значениями массивы горизонтов.
        self._top_horizon: list[int | float] = [0 for _ in range(1520)]
        self._bottom_horizon: list[int | float] = [1010 for _ in range(1520)]

    @staticmethod
    def __to_radians(angle: int | float):
        """
        Метод для перевода угла из градусной меры в радианную
        """

        return angle * m.pi / 180

    def __rotate_around_x(
            self,
            x: int | float,
            y: int | float,
            z: int | float,
            angle: int | float
    ):
        """
        Метод позволяет повернуть поверхность вокруг оси Ox
        """
        angle = self.__to_radians(angle)
        # минус ли?
        y = y * m.cos(angle) - m.sin(angle) * z

        return x, y

    def __rotate_around_y(
            self,
            x: int | float,
            y: int | float,
            z: int | float,
            angle: int | float
    ):
        """
        Метод позволяет повернуть поверхность вокруг оси Oy
        """
        angle = self.__to_radians(angle)
        # минус ли?
        x = x * m.cos(angle) - m.sin(angle) * z

        return x, y

    def __rotate_around_z(
            self,
            x: int | float,
            y: int | float,
            z: int | float,
            angle: int | float
    ):
        """
        Метод позволяет повернуть поверхность вокруг оси Oz
        """
        angle = self.__to_radians(angle)

        buf = x
        x = m.cos(angle) * x - m.sin(angle) * y
        y = m.cos(angle) * y + m.sin(angle) * buf

        return x, y

    @staticmethod
    def __scale(x, y):
        """
        Метод позволяет масштабировать поверхность
        """
        x *= 50
        y *= 50
        x += 1520 // 2
        y += 1010 // 2  # - y
        return round(x), round(y)

    def __transform_point(
            self,
            x: int | float,
            y: int | float,
            z: int | float,
            angles: list[int | float]
    ):
        """
        Метод позволяет трансформировать точку
        """
        x, y = self.__rotate_around_x(x, y, z, angles[0])
        x, y = self.__rotate_around_y(x, y, z, angles[1])
        x, y = self.__rotate_around_z(x, y, z, angles[2])

        return self.__scale(x, y)

    def __is_visible(self, x: int | float, y: int | float):
        """
        Метод позволяет определить, видима ли точка
        """
        # Если точка, ниже нижнего горизонта (или на нем),
        # то она видима.
        if y <= self._bottom_horizon[x]:
            return -1

        # Если точка выше верхнего горизонта (или на нем),
        # то она видима.
        if y >= self._top_horizon[x]:
            return 1

        # Иначе она невидима.
        return 0

    def __horizon(
            self,
            x1: int | float,
            y1: int | float,
            x2: int | float,
            y2: int | float
    ):
        """
        Метод для заполнения массивов горизонтов между x1 и x2
        На основе линейной интерполяции.
        """
        # Проверка вертикальности наклона.
        if x2 - x1 == 0:
            self._top_horizon[x2] = max(self._top_horizon[x2], y2)
            self._bottom_horizon[x2] = min(self._bottom_horizon[x2], y2)
            return

        # Иначе вычисляем наклон.
        tg = (y2 - y1) / (x2 - x1)
        # Движемся по x с шагом 1, чтобы заполнить
        # Массивы от x1 до x2.
        for x in range(x1, x2 + 1):
            y = round(tg * (x - x1) + y1)
            self._top_horizon[x] = max(self._top_horizon[x], y)
            self._bottom_horizon[x] = min(self._bottom_horizon[x], y)

    def __process_side(self, x, y, xe, ye):
        """
        Метод для обработки и обновления точек бокового ребра
        """
        if xe != -1:
            # Если кривая не первая
            self._canvas.create_line(xe, ye, x, y, fill="#800080")
            self.__horizon(xe, ye, x, y)

        xe = x
        ye = y

        return xe, ye

    @staticmethod
    def __get_intersection(x1, y1, x2, y2, horizon):
        """
        Метод позволяет вычислить пересечение с горизонтом
        """
        dx = x2 - x1
        dyc = y2 - y1
        dyp = horizon[x2] - horizon[x1]

        if dx == 0:
            xi = x2
            yi = horizon[x2]
            return xi, yi

        if y1 == horizon[x1] and y2 == horizon[x2]:
            return x1, y1

        tg = dyc / dx
        xi = x1 - round(dx * (y1 - horizon[x1]) / (dyc - dyp))
        yi = round((xi - x1) * tg + y1)

        return xi, yi

    def __draw(self):
        """
        Метод позволяет отобразить поверхность
        """
        x_start, x_end = self._border_x
        z_start, z_end = self._border_z

        x_left, y_left = -1, -1
        x_right, y_right = -1, -1

        z = self._border_z[1]

        while z >= z_start - self._z_step / 2:
            x_prev = x_start
            y_prev = self._func(x_start, z)
            x_prev, y_prev = self.__transform_point(x_prev, y_prev, z, self._angles)

            flag_prev = self.__is_visible(x_prev, y_prev)

            x_left, y_left = self.__process_side(x_prev, y_prev, x_left, y_left)
            x = x_start

            while x <= x_end + self._x_step / 2:
                y_curr = self._func(x, z)
                x_curr, y_curr = self.__transform_point(x, y_curr, z, self._angles)

                # Проверка видимости текущей точки.
                flag_curr = self.__is_visible(x_curr, y_curr)

                # Равенство флагов означает, что обе точки находятся
                # Либо выше верхнего горизонта, либо ниже нижнего,
                # Либо обе невидимы.
                if flag_curr == flag_prev:
                    # Если текущая вершина выше верхнего горизонта
                    # Или ниже нижнего (Предыдущая такая же)
                    if flag_curr != 0:
                        # Значит отображаем отрезок от предыдущей до текущей.
                        self._canvas.create_line(x_prev, y_prev, x_curr, y_curr, fill="#800080")
                        self.__horizon(x_prev, y_prev, x_curr, y_curr)
                    # flag_curr == 0 означает, что и flag_prev == 0,
                    # А значит часть от flag_curr до flag_prev невидима. Ничего не делаем.
                else:
                    # Если видимость изменилась, то
                    # Вычисляем пересечение.
                    if flag_curr == 0:
                        if flag_prev == 1:
                            # Сегмент "входит" в верхний горизонт.
                            # Ищем пересечение с верхним горизонтом.
                            xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._top_horizon)
                        else:  # flag_prev == -1 (flag_prev нулю (0) не может быть равен, т.к. мы обработали это выше).
                            # Сегмент "входит" в нижний горизонт.
                            # Ищем пересечение с нижним горизонтом.
                            xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._bottom_horizon)
                        # Отображаем сегмент, от предыдущей точки, до пересечения.
                        self._canvas.create_line(x_prev, y_prev, xi, yi, fill="#800080")
                        self.__horizon(x_prev, y_prev, xi, yi)
                    else:
                        if flag_curr == 1:
                            if flag_prev == 0:
                                # Сегмент "выходит" из верхнего горизонта.
                                # Ищем пересечение с верхним горизонтом.
                                xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._top_horizon)
                                # Отображаем сегмент от пересечения до текущей точки.
                                self._canvas.create_line(xi, yi, x_curr, y_curr, fill="#800080")
                                self.__horizon(xi, yi, x_curr, y_curr)
                            else:  # flag_prev == -1
                                # Сегмент начинается с точки, ниже нижнего горизонта
                                # И заканчивается в точке выше верхнего горизонта.
                                # Нужно искать 2 пересечения.
                                # Первое пересечение с нижним горизонтом.
                                xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._bottom_horizon)
                                # Отображаем сегмент от предыдущей то пересечения.
                                self._canvas.create_line(x_prev, y_prev, xi, yi, fill="#800080")
                                self.__horizon(x_prev, y_prev, xi, yi)
                                # Второе пересечение с верхним горизонтом.
                                xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._top_horizon)
                                # Отображаем сегмент от пересечения до текущей.
                                self._canvas.create_line(xi, yi, x_curr, y_curr, fill="#800080")
                                self.__horizon(xi, yi, x_curr, y_curr)
                        else:  # flag_curr == -1
                            if flag_prev == 0:
                                # Сегмент "выходит" из нижнего горизонта.
                                # Ищем пересечение с нижним горизонтом.
                                xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._bottom_horizon)
                                self._canvas.create_line(xi, yi, x_curr, y_curr, fill="#800080")
                                self.__horizon(xi, yi, x_curr, y_curr)
                            else:
                                # Сегмент начинается с точки, выше верхнего горизонта
                                # И заканчивается в точке ниже нижнего горизонта.
                                # Нужно искать 2 пересечения.
                                # Первое пересечение с верхним горизонтом.
                                xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._top_horizon)
                                # Отображаем сегмент от предыдущей до пересечения.
                                self._canvas.create_line(x_prev, y_prev, xi, yi)
                                self.__horizon(x_prev, y_prev, xi, yi)
                                # Ищем второе пересечение с нижним горизонтом.
                                xi, yi = self.__get_intersection(x_prev, y_prev, x_curr, y_curr, self._bottom_horizon)
                                # Отображаем сегмент от пересечения до текущей.
                                self._canvas.create_line(xi, yi, x_curr, y_curr)
                                self.__horizon(xi, yi, x_curr, y_curr)
                x_prev, y_prev = x_curr, y_curr
                flag_prev = flag_curr
                x += self._x_step
            x_right, y_right = self.__process_side(x_prev, y_prev, x_right, y_right)
            z -= self._z_step

    def draw(self):
        """
        Метод обертка для отображения поверхности
        """
        self.__draw()
