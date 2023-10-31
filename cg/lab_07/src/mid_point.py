from tkinter import Canvas, PhotoImage
import math as m
import copy as cp

from line import Line
from cutter import Cutter
from PointClass import Point
from dda import Dda

# from bresenham import BresenhamInt
# from bresenham import BresenhamFloat

EPS = 1e-8


class MidPointMethod:
    """
    Класс для алгоритма средней точки отсечения прямоугольным регулярным отсекателем
    """

    def __init__(
            self,
            canvas: Canvas,
            img: PhotoImage,
            list_line: list[Line],
            list_cutter: list[Cutter],
            color_result: str
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._canvas: Canvas = canvas
        self._img: PhotoImage = img
        self._list_line: list[Line] = list_line
        self._list_cutter: list[Cutter] = list_cutter
        self._color_result: str = color_result

    @staticmethod
    def __sort_points(p1, p2, p3, p4):
        """
        Сортировка точек по возрастанию
        """
        points = [p1, p2, p3, p4]  # Создаем список из переданных точек
        sorted_points = sorted(points, key=lambda p: p.x)  # Сортируем список точек по возрастанию
        sorted_points = sorted(sorted_points, key=lambda p: p.y)  # Сортируем список точек по возрастанию

        return tuple(sorted_points)  # Возвращаем отсортированные точки в виде кортежа

    def __update_points_cutter(self):
        """
        Метод позволяет получить точки отсекателя
        """
        cutter = self._list_cutter[0]
        p1, p2, p3, p4 = cutter.point_top_left, cutter.point_top_right, \
            cutter.point_lower_left, cutter.point_lower_right

        p1, p2, p3, p4 = self.__sort_points(p1, p2, p3, p4)

        self._list_cutter[0].point_top_left = p1
        self._list_cutter[0].point_top_right = p2
        self._list_cutter[0].point_lower_left = p3
        self._list_cutter[0].point_lower_right = p4

    def __create_point_on_img(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости (на картинке)
        """
        self._img.put(color, (m.floor(x0), m.floor(y0)))

    def __draw_line_on_img(self, point_start: Point, point_end: Point, color: str):
        """
        Метод позволяет отобразить линию на картинке, используя алгоритм
        Брезенхема для вещественных чисел
        """
        builder = Dda(point_start, point_end)
        points = builder.get_points_for_line(color_line=color)

        for i, point in enumerate(points):
            self.__create_point_on_img(point.x, point.y, color=color)

    def __calc_point_codes(self, point: Point) -> (int, int, int, int):
        """
        Метод позволяет вычислить коды переданной точки
        """
        x, y = point.x, point.y
        cutter = self._list_cutter[0]

        # абсциссы и ординаты отсекателя
        xl, xr = cutter.point_lower_left.x, cutter.point_lower_right.x
        yt, yb = cutter.point_lower_left.y, cutter.point_top_left.y

        # коды точки
        t1 = 1 if x < xl else 0
        t2 = 1 if x > xr else 0
        t3 = 1 if y < yb else 0
        t4 = 1 if y > yt else 0

        return t1, t2, t3, t4

    @staticmethod
    def __calc_codes_sum(tuple_codes: (int, int, int, int)) -> int:
        """
        Метод позволяет посчитать суму кодов для точки
        """

        return sum(tuple_codes)

    @staticmethod
    def __calc_codes_line_sum(
            tuple_codes1: (int, int, int, int),
            tuple_codes2: (int, int, int, int)
    ) -> int:
        """
        Метод позволяет посчитать логическое произведение суммы кодов отрезка
        """
        p = 0

        for i in range(4):
            p += tuple_codes1[i] * tuple_codes2[i]

        return p

    def __is_full_line_visibility(
            self,
            tuple_codes1: (int, int, int, int),
            tuple_codes2: (int, int, int, int)
    ) -> bool:
        """
        Метод позволяет определить полную видимость отрезка
        """
        sum1 = self.__calc_codes_sum(tuple_codes1)
        sum2 = self.__calc_codes_sum(tuple_codes2)

        if sum1 == 0 and sum2 == 0:
            return True

        return False

    def __is_full_line_invisibility(
            self,
            tuple_codes1: (int, int, int, int),
            tuple_codes2: (int, int, int, int)
    ) -> bool:
        """
        Метод позволяет определить полную невидимость отрезка
        """
        line_sum = self.__calc_codes_line_sum(tuple_codes1, tuple_codes2)

        if line_sum != 0:
            return True

        return False

    @staticmethod
    def __line_length(ps: Point, pe: Point):
        """
        Метод возвращает длину линии
        """

        return m.sqrt(pow(ps.x - pe.x, 2) + pow(ps.y - pe.y, 2))

    def __find_intersection(self, ps: Point, pe: Point):
        """
        Метод найти точку пересечения
        """
        ps, pe = cp.deepcopy(ps), cp.deepcopy(pe)

        i = 0  # по алгоритму надо
        while self.__line_length(ps, pe) > EPS:
            t_ps, t_pe = self.__calc_point_codes(ps), self.__calc_point_codes(pe)

            if self.__is_full_line_visibility(t_ps, t_pe):
                self.__draw_line_on_img(ps, pe, self._color_result)
                return

            if self.__is_full_line_invisibility(t_ps, t_pe):
                return

            if i > 1:
                if self.__is_full_line_invisibility(t_ps, t_pe):
                    return
                else:
                    self.__draw_line_on_img(ps, pe, self._color_result)
                    return

            if t_pe == 0:  # точка pe видима
                ps, pe = pe, ps
                i += 1
            else:  # точка pe невидима
                while self.__line_length(ps, pe) > EPS:
                    p_mid = (ps + pe) / 2
                    p = ps
                    ps = p_mid
                    t_ps = self.__calc_point_codes(ps)

                    if self.__is_full_line_invisibility(t_ps, t_pe):
                        ps = p
                        pe = p_mid
                else:
                    ps, pe = pe, ps
                    i += 1

        return ps

    def __cut_line(self, line: Line):
        """
        Метод позволяет отсечь один отрезок
        """
        obj = self.__find_intersection(line.point_start, line.point_end)
        if obj is None:
            return
        p1 = obj

        obj = self.__find_intersection(line.point_end, line.point_start)
        if obj is None:
            return
        p2 = obj

        self.__draw_line_on_img(p1, p2, self._color_result)

    def cut(self):
        """
        Метод, позволяющий произвести отсечение отрезков
        """
        # переопределяем точки отсекателя, если был задан не слева сверку в направлении вправо вниз
        self.__update_points_cutter()

        for line in self._list_line:
            self.__cut_line(line)
