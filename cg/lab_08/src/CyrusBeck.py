from tkinter import Canvas, PhotoImage, messagebox
import math as m

from line import Line
from figure import Figure
from PointClass import Point
from dda import Dda

EPS = 1e-9


class Vector(Point):
    """
    Небольшая надстройка над классом Point, дабы код был более читаемым
    """

    def __init__(self, x: int | float, y: int | float):
        super().__init__(x, y)


class Edge(Line):
    """
    Класс надстройка над классом Line дабы код был более читаемым
    """

    def __init__(self, point_start: Point, point_end: Point = None):
        super().__init__(point_start, point_end)


class CurysBeck:
    """
    Класс для отсечения отрезков произвольным многоугольным отсекателем
    с использованием алгоритма отсечения Кируса-Бека
    """

    def __init__(
            self,
            canvas: Canvas,
            img: PhotoImage,
            list_line: list[Line],
            list_cutter: list[Figure],
            color_result: str
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._canvas: Canvas = canvas
        self._img: PhotoImage = img
        self._list_line: list[Line] = list_line
        self._list_cutter: list[Figure] = list_cutter
        self._color_result: str = color_result

        self._list_edges: list[Edge] = self.__convert_list_points_to_list_edge()
        """
        Как вычислить вектор нормали к отрезку:
        Вычислите вектор, направленный от начальной точки отрезка к конечной точке отрезка. 
        Для этого вычитайте координаты конечной точки отрезка из координат начальной точки.
        Поверните этот вектор на 90 градусов по часовой стрелке или против часовой стрелки, 
        чтобы получить вектор, перпендикулярный отрезку. Можно достичь этого, 
        поменяв местами координаты x и y вектора и умножив одну из них на -1 или поменяв знак 
        (например, если у вектора (x, y), то переведите его в (-y, x) или (y, -x))
        """

    @staticmethod
    def __get_sign_vector_product(edge1: Edge, edge2: Edge):
        """
        Метод позволяет определить знак векторного произведения двух отрезков
        """
        vector1 = Vector(
            x=(edge1.point_end.x - edge1.point_start.x),
            y=(edge1.point_end.y - edge1.point_start.y)
        )
        vector2 = Vector(
            x=(edge2.point_end.x - edge2.point_start.x),
            y=(edge2.point_end.y - edge2.point_start.y)
        )

        vector_product = vector1.x * vector2.y - vector1.y * vector2.x

        if m.fabs(vector_product) <= EPS:
            return 0

        return 1 if vector_product > 0 else -1

    def __is_convex_cutter(self) -> bool:
        """
        Метод позволяет определить, является ли отсекатель выпуклым
        """
        # начальный знак векторного произведения
        sign0 = self.__get_sign_vector_product(self._list_edges[-1], self._list_edges[0])

        for i in range(len(self._list_edges) - 1):
            sign = self.__get_sign_vector_product(self._list_edges[i], self._list_edges[i + 1])
            if sign != sign0:
                return False

        if sign0 == 0:
            return False

        return True

    def __create_point_on_img(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости (на картинке)
        """
        self._img.put(color, (round(x0), round(y0)))

    def __draw_line_on_img(self, point_start: Point, point_end: Point, color: str):
        """
        Метод позволяет отобразить линию на картинке, используя алгоритм
        Брезенхема для вещественных чисел
        """
        builder = Dda(point_start, point_end)
        points = builder.get_points_for_line(color_line=color)

        for i, point in enumerate(points):
            self.__create_point_on_img(point.x, point.y, color=color)

    def __convert_list_points_to_list_edge(self):
        """
        Метод позволит из списка точек отсекателя получить список ребер отсекателя
        """
        cutter = self._list_cutter[0]
        list_edges = list()
        for i in range(len(cutter)):
            if i == len(cutter) - 1:
                edge = Edge(cutter[i], cutter[0])
            else:
                edge = Edge(cutter[i], cutter[i + 1])

            list_edges.append(edge)

        return list_edges

    @staticmethod
    def __get_scalar_product(v1: Vector, v2: Vector):
        """
        Метод для вычисления скалярного произведения двух двумерных векторов
        """

        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def __get_vector(p1: Point, p2: Point):
        """
        Метод, позволяющий найти вектор
        """
        # Чтобы найти координаты вектора AB, зная координаты его начальной точки
        # А и конечной точки В, необходимо из координат конечной точки вычесть
        # соответствующие координаты начальной точки.
        vector = Vector(x=(p2.x - p1.x), y=(p2.y - p1.y))

        return vector

    def __get_normal(self, edge: Edge, edge_next: Edge):
        """
        Метод позволяет вычислить вектор внутренней нормали к отрезку
        """
        normal_x = edge.point_end.y - edge.point_start.y
        normal_y = edge.point_start.x - edge.point_end.x

        normal = Vector(x=normal_x, y=normal_y)
        """
        внутренняя нормаль nв, в произвольной точке a, 
        лежащей на любой границе выпуклой области C, 
        удовлетворяет следующему условию: nв (b - a) >= 0 , 
        где b - любая другая точка на границе отсекающей области
        """
        edge_next_vector = self.__get_vector(edge_next.point_start, edge_next.point_end)

        if self.__get_scalar_product(normal, edge_next_vector) < 0:
            normal.x, normal.y = -normal.x, -normal.y

        return normal

    @staticmethod
    def __get_wi(line: Line, edge: Edge):
        """
        Метод позволяет вычислить коэффициент для второго вектора
        """
        fi = edge.point_start
        p1 = line.point_start

        wi = Vector(x=(p1.x - fi.x), y=(p1.y - fi.y))

        return wi

    @staticmethod
    def __convert_parametric(line: Line, t: int | float):
        """
        Метод позволяет получить точку отрезка в зависимости от параметра t
        """
        # P(t) = P1 + (P2 - P1) * t
        point = line.point_start + (line.point_end - line.point_start) * t

        return point

    def __cut_line(self, line: Line):
        """
        Метод позволяет отсечь один отрезок
        """
        edges = self._list_edges
        d: Vector = line.point_end - line.point_start  # директриса (пусть будет точкой, хотя это вектор)

        t0, t1 = 0, 1  # ограничения на параметр t

        for i in range(len(edges)):
            if i == len(edges) - 1:
                normal = self.__get_normal(edges[i], edges[0])
            else:
                normal = self.__get_normal(edges[i], edges[i + 1])

            wi = self.__get_wi(line, edges[i])

            wi_scalar = self.__get_scalar_product(wi, normal)  # Скалярное произведение W на N.
            d_scalar = self.__get_scalar_product(d, normal)  # Скалярное произведение D на N.

            if d_scalar == 0:  # Если отрезок расположен параллельно i-ой стороне отсекателя
                if wi_scalar < 0:  # И находятся снаружи отсекателя
                    return  # то отрезок невидимый.
            else:
                t = -wi_scalar / d_scalar
                # Если Dск > 0 - то точку пересечения
                # нужно отнести к группе, определяющей начало видимой части.
                if d_scalar > 0:
                    # Если т. пересечения вне отрезка,
                    # Значит отрезок невидим.
                    if t > 1:
                        return
                    else:
                        # Иначе нужно из точек, определяющих
                        # начало, выбрать максимальное.
                        t0 = max(t0, t)
                        # Если Dск < 0 - то точку пересечения нужно отнести к
                        # группе, определяющей конец видимой части.
                elif d_scalar < 0:
                    # Если т. пересечения вне отрезка,
                    # Значит отрезок невидим.
                    if t < 0:
                        return
                    else:
                        # Иначе нужно из точек, определяющих
                        # конец, выбрать минимальное.
                        t1 = min(t1, t)
        # Проверка видимости отрезка
        if t0 > t1:
            return

        # Возвращаем начало и конец видимого отрезка.
        p1, p2 = self.__convert_parametric(line, t0), self.__convert_parametric(line, t1)
        self.__draw_line_on_img(p1, p2, self._color_result)

    def cut(self):
        """
        Метод позволяет отсечь отрезки произвольным выпуклым многоугольным отсекателем
        """
        if not self.__is_convex_cutter():
            messagebox.showwarning("", "Введенный отсекатель не является выпуклым!")
            return

        for line in self._list_line:
            self.__cut_line(line)
