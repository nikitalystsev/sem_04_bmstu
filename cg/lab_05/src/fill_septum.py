from tkinter import PhotoImage, Canvas

from PointClass import Point
from figure import Figure
from measurements import CompareTime
from bresenham import BresenhamFloat

BLACK = "#000000"


class FillSeptum:
    """
    Класс заполнения произвольной многоугольной области c
    помощью алгоритма заполнения с перегородкой
    """

    def __init__(
            self,
            canvas: Canvas,
            img: PhotoImage,
            list_figure: list[Figure],
            color_bg: str,
            color_fill: str,
            dict_color_fill: dict
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._canvas: Canvas = canvas
        self._img: PhotoImage = img
        self._list_figure: list[Figure] = list_figure
        self._color_bg: str = color_bg
        self._color_fill: str = color_fill
        self._dict_color_fill: dict = dict_color_fill

    @staticmethod
    def __find_inters_with_edge(start_point: Point, end_point: Point):
        """
        Метод позволяет найти пересечения всех сканирующих строк
        с очередным ребром многоугольника
        """
        list_inters_with_edge = list()

        if start_point.y == end_point.y:  # горизонтальное ребро
            return []

        if start_point.y > end_point.y:
            start_point, end_point = end_point, start_point

        dy = 1
        dx = (end_point.x - start_point.x) / (end_point.y - start_point.y)

        x = start_point.x
        y = start_point.y

        while y < end_point.y:
            list_inters_with_edge.append(Point(x=int(x), y=int(y)))

            y += dy
            x += dx

        return list_inters_with_edge

    def __reverse_pixel(self, x: int | float, y: int | float):
        """
        Метод для закраски пикселя в алгоритме заполнения с перегородкой
        """
        color_pixel = self._img.get(round(x), round(y))  # в rgb
        # color_pixel = self.__get_str_color(x, y)  # получили цвет пикселя

        if color_pixel == self._dict_color_fill[self._color_fill]:  # если цвет пикселя равен цвету фона
            # инвертируем его цвет на цвет фигуры
            # self.create_point(x, y, self.color_figure)
            self._img.put(self._color_bg, (round(x), round(y)))
        elif color_pixel == self._dict_color_fill[self._color_bg]:  # если цвет пикселя равен цвету линии
            # инвертируем его на цвет фона
            # self.create_point(x, y, self.color_bg)
            self._img.put(self._color_fill, (round(x), round(y)))

    def __create_point_on_img(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости (на картинке)
        """
        self._img.put(color, (round(x0), round(y0)))

    def __get_septum_x(self) -> int | float:
        """
        Метод позволяет определить значение абсциссы для перегородки
        В качестве такой абсциссы принимается медианное значение всего списка точек
        """
        points = list()

        for figure in self._list_figure:
            for i in range(len(figure)):
                points.append(figure[i].x)

        n = len(points)
        sorted_points = sorted(points)

        return sorted_points[n // 2]

    def __draw_septum(self, x: int | float):
        """
        Метод позволяет отобразить перегородку
        """
        point_prev = Point(x=x, y=0)
        point_last = Point(x=x, y=1000)

        builder = BresenhamFloat(point_prev, point_last)
        points = builder.get_points_for_line(color_line=BLACK)

        for point in points:
            self.__create_point_on_img(point.x, point.y, color=BLACK)

    def __fill(self, list_inters: list[Point], delay_mode=False) -> None:
        """
        Метод позволяет заполнить произвольной многоугольной области с помощью
        алгоритма заполнения с перегородкой
        """
        # Проводим перегородку через первую вершину многоугольника.
        septum = self.__get_septum_x()
        self.__draw_septum(septum)

        for i in range(len(list_inters)):
            # если пересечение находится слева от перегородки
            if list_inters[i].x < septum:
                # то перекрасить все пиксели, центры которых лежат справа
                # или на пересечении сканирующей строки с ребром и
                # слева от перегородки
                for j in range(list_inters[i].x + 1, septum + 1):
                    if delay_mode:
                        self._canvas.after(0, self.__reverse_pixel(j, list_inters[i].y))
                        self._canvas.update()
                    else:
                        self.__reverse_pixel(j, list_inters[i].y)
            # если пересечение находится справа от перегородки
            elif list_inters[i].x > septum:
                # то перекрасить все пиксели, центры которых лежат слева
                # от пересечения сканирующей строки с ребром
                # и справа от перегородки
                for j in range(list_inters[i].x, septum, -1):
                    if delay_mode:
                        self._canvas.after(0, self.__reverse_pixel(j, list_inters[i].y))
                        self._canvas.update()
                    else:
                        self.__reverse_pixel(j, list_inters[i].y)

    def fill(self, delay_mode=False) -> float:
        """
        Метод обертка для заполнения фигуры
        """
        general_list_inters = list()

        # обрабатываем все фигуры
        for figure in self._list_figure:
            # обрабатываем все ребра
            for i in range(len(figure) - 1):
                point_curr = figure[i]
                point_next = figure[i + 1]

                general_list_inters.extend(self.__find_inters_with_edge(point_curr, point_next))

            # замыкающее ребро
            point_last = figure[len(figure) - 1]
            point_start = figure[0]

            general_list_inters.extend(self.__find_inters_with_edge(point_start, point_last))

        work_time = 0

        if delay_mode:
            self.__fill(general_list_inters, delay_mode=True)
        else:
            work_time = CompareTime.time_now()
            self.__fill(general_list_inters)
            work_time = CompareTime.time_now() - work_time

        return work_time
