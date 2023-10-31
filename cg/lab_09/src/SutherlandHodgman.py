from tkinter import Canvas, PhotoImage, messagebox
import copy as cp
import math as m

from line import Line
from PointClass import Point
from figure import Figure
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


class Cutter(Figure):
    """
    Небольшая надстройка над классом Figure, дабы удобнее было различать, где фигура,
    а где отсекатель
    """

    def __init__(self):
        super().__init__()


class SutherlandHodgman:
    """
    Класс для отсечения произвольной многоугольной области произвольным выпуклым отсекателем
    с помощью алгоритма Сазерленда - Ходжмана
    """

    def __init__(
            self,
            canvas: Canvas,
            img: PhotoImage,
            list_figure: list[Figure],
            list_cutter: list[Cutter],
            color_result: str
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._canvas: Canvas = canvas
        self._img: PhotoImage = img
        self._list_figure: list[Figure] = list_figure
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

        # если многоугольник вырожденный
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

    def __get_normal(self, p1: Point, p2: Point, p3: Point):
        """
        Метод позволяет вычислить вектор внутренней нормали к отрезку
        """
        normal_x = p2.y - p1.y
        normal_y = p1.x - p2.x

        normal = Vector(x=normal_x, y=normal_y)

        edge_next_vector = self.__get_vector(p2, p3)

        # Если скалярное произведение вектора нормали
        # На вектор, который является следующим ребром
        # Многоугольника, дает нам отрицательное значение,
        # То вектор нормали нужно домножить на -1
        # Чтобы он был направлен внутрь многоугольника.

        if self.__get_scalar_product(edge_next_vector, normal) < 0:
            normal.x, normal.y = -normal.x, -normal.y

        return normal

    def __is_visible_point(self, point: Point, p1: Point, p2: Point, p3: Point):
        """
        Метод позволяет определить видимость точки
        """
        # Находим нормаль к ребру (p1, p2)
        # p3 нужно, чтобы проверить нормаль (Внутренняя ли она).
        normal = self.__get_normal(p1, p2, p3)
        vector = self.__get_vector(p2, point)

        if self.__get_scalar_product(normal, vector) < 0:
            return False

        return True

    @staticmethod
    def __convert_parametric(line: Line, t: int | float):
        """
        Метод позволяет получить точку отрезка в зависимости от параметра t
        """
        # P(t) = P1 + (P2 - P1) * t
        point = line.point_start + (line.point_end - line.point_start) * t

        return point

    @staticmethod
    def __get_wi(line: Line, edge: Edge):
        """
        Метод позволяет вычислить коэффициент для второго вектора
        """
        fi = edge.point_start
        p1 = line.point_start

        wi = Vector(x=(p1.x - fi.x), y=(p1.y - fi.y))

        return wi

    def __is_intersection(self, edge1: Edge, edge2: Edge, p3: Point):
        # edge1 - ребро отсекаемого многоугольника.
        # edge2 - ребро отсекателя.
        # p3 - след. вершина отсекателя, нужна для
        # корректного определения нормали

        # Определяем видимость вершин относительно рассматриваемого ребра.
        visible1 = self.__is_visible_point(edge1.point_start, edge2.point_start, edge2.point_end, p3)
        visible2 = self.__is_visible_point(edge1.point_end, edge2.point_start, edge2.point_end, p3)
        # Если одна вершина видна, а вторая нет (Есть пересечение).
        # Иначе пересечения нет.
        if not (visible1 ^ visible2):
            return False

        # Ищем пересечение
        normal = self.__get_normal(edge2.point_start, edge2.point_end, p3)
        d_x = edge1.point_end.x - edge1.point_start.x
        d_y = edge1.point_end.y - edge1.point_start.y
        d = Vector(d_x, d_y)  # директриса
        wi = self.__get_wi(edge1, edge2)
        # Скалярное произведение D на N.
        d_scalar = self.__get_scalar_product(d, normal)
        # Скалярное произведение W на N.
        wi_scalar = self.__get_scalar_product(wi, normal)
        # d_scalar может быть равен нулю в двух случаях:
        # 1. Если ребро отсекателя вырождается в точку
        # Т.е. p1 == p2. В интерфейсе обработан данный случай
        # (Пользователь не может ввести ребро у которого начало и конец совпадают)
        # 2. Если текущее ребро отсекаемого многоугольника параллельно
        # Ребру отсекателя. Такие ребра не дойдут до этого момента -
        # Они будут обработаны выше. Т.к. в этом случае нет пересечения
        # Обе вершины отсекаемого многоугольника будут либо по видимую сторону
        # Отсекателя, либо по невидимую.
        t = -(wi_scalar / d_scalar)

        return self.__convert_parametric(edge1, t)

    def __cut(self):
        """
        Метод позволяет отсечь произвольную многоугольную область выпуклым отсекателем
        """
        cutter = cp.deepcopy(self._list_cutter[0])
        figure = cp.deepcopy(self._list_figure[0])

        # Для удобства работы алгоритма первая вершина
        # отсекателя заносится в массив дважды (В начало и конец).
        # Т.к. последнее ребро отсекателя образуется
        # последней и первой вершинами многоугольника.
        cutter.add_point(cutter[0])
        # Также, т.к. для поиска нормали для ребра i и i+1
        # Мне нужна вершина i+2. Поэтому я дублирую еще вторую вершину.
        # (Чтобы мог в цикле отправлять i+2).
        cutter.add_point(cutter[1])
        # цикл по всем вершинам отсекателя
        for i in range(len(cutter) - 2):
            result_figure = Figure()  # обнуление количества вершин результирующего многоугольника
            # Особым образом нужно обрабатывать первую
            # точку многоугольника: для нее требуется определить
            # только видимость. Если точка видима, то она заносится
            # В результирующий список и становится начальной точкой первого ребра.
            # Если же она невидима, то она просто становится начальной точкой ребра
            # И в результирующий список не заносится.
            f = figure[0]  # запоминаем начальную вершину
            if self.__is_visible_point(f, cutter[i], cutter[i + 1], cutter[i + 2]):
                result_figure.add_point(f)

            s = figure[0]
            # цикл по всем вершинам многоугольника
            for j in range(1, len(figure)):
                # Определяем факт пересечения текущего ребра отсекателя (cutter[i], cutter[i + 1])
                # И рассматриваемого ребра отсекаемого многоугольника (s, polygon[j]),
                # Где s = figure[j - 1]. cutter[i + 2] нам нужно, чтобы корректно найти нормаль.
                t = self.__is_intersection(Edge(s, figure[j]), Edge(cutter[i], cutter[i + 1]), cutter[i + 2])
                # Если есть пересечение, то заносим его в новый массив вершин.
                if t and isinstance(t, Point):  # проверка на тип переменной t
                    result_figure.add_point(t)
                # Запоминаем в s текущую вершину. (Чтобы на следующем шаге
                # Искать пересечение polygon[j - 1] и polygon[j])
                s = figure[j]
                # Проверяем, видна ли текущая вершина
                if self.__is_visible_point(s, cutter[i], cutter[i + 1], cutter[i + 2]):
                    # Если видна, то заносим ее в новый массив вершин.
                    result_figure.add_point(s)

            # Можно убедиться в полной невидимости многоугольника,
            # относительно текущей границы отсекателя. При анализе
            # последнего замыкающего ребра отсутствие результата означает невидимость
            # многоугольника относительно текущей границы отсекателя, а значит многоугольник невидимый.
            if not len(result_figure):
                return False
            # Проверка факта пересечения ребра многоугольника SF с ребром отсекателя CjCj+1.
            t = self.__is_intersection(Edge(s, f), Edge(cutter[i], cutter[i + 1]), cutter[i + 2])
            if t and isinstance(t, Point):
                result_figure.add_point(t)

            figure = cp.deepcopy(result_figure)

        return figure

    def cut(self):
        """
        Метод обертка для отсечения
        """
        if not self.__is_convex_cutter():
            messagebox.showwarning("", "Введенный отсекатель не является выпуклым!")
            return

        result_figure = self.__cut()

        for i in range(len(result_figure)):
            if i == len(result_figure) - 1:
                self.__draw_line_on_img(result_figure[len(result_figure) - 1], result_figure[0], self._color_result)
            else:
                self.__draw_line_on_img(result_figure[i], result_figure[i + 1], self._color_result)
