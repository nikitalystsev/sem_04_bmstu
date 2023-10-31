import tkinter as tk
from tkinter import messagebox

from PointClass import Point
from figure import Figure
from dda import Dda
from SutherlandHodgman import SutherlandHodgman

# from bresenham import BresenhamInt
# from bresenham import BresenhamFloat

BLACK = "#000000"
WHITE = "#FFFFFF"
ORANGE = "#FFA500"
RED = "#FF0000"
DARKCYAN = "DarkCyan"
GREEN = "#008000"
BLUE = "#0000FF"
VIOLET = "#800080"
YELLOW = "#FFFF00"
Aquamarine = "#7FFFD4"
LightCyan = "#E0FFFF"
SILVER = "#C0C0C0"

EPS = 1e-9


def float_equal(a: int | float, b: int | float):
    """
    Функция сравнивает вещественные числа
    """

    return abs(a - b) < EPS


class Cutter(Figure):
    """
    Небольшая надстройка над классом Figure, дабы удобнее было различать, где фигура,
    а где отсекатель
    """

    def __init__(self):
        super().__init__()


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, color_cutter: str, color_figure: str, color_result: str, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self._width = kwargs.get("width")
        self._height = kwargs.get("height")

        self._list_figure: list[Figure] = [Figure()]  # массив пользовательских отсекаемых фигур
        self._list_cutter: list[Cutter] = [Cutter()]  # массив отсекателей

        self._color_figure: str = color_figure  # цвет пользовательских отрезков
        self._color_cutter: str = color_cutter  # цвет отсекателя
        self._color_result: str = color_result  # цвет результата
        self._color_bg: str = self["bg"]

        # определим возможные цвета заполнения (используя словарь)
        self.dict_colors_figure = {
            (255, 255, 255): "#FFFFFF",
            (0, 0, 0): "#000000",
            (255, 0, 0): "#FF0000",
            (255, 165, 0): "#FFA500",
            (255, 255, 0): "#FFFF00",
            (0, 128, 0): "#008000",
            (0, 0, 255): "#0000FF",
            (128, 0, 128): "#800080"
        }

        # чтобы получать цвет пикселя на холсте, необходимо использовать изображения
        self._img = self.__create_image()

        # Привязываем функцию self.get_line_by_click к событию нажатия правой кнопки мыши на холсте
        self.bind("<Button-1>", self.__add_mouse_point_figure)  # левая кнопка мыши
        self.bind("<Button-3>", self.__add_mouse_point_cutter)  # правая кнопка мыши

        self.__draw_axis()

    def __draw_axis(self) -> None:
        """
        Метод отображает экранные оси
        """
        # по оси ординат
        for i in range(0, self._height, 50):
            self.create_line(0, i, 6, i, width=2)
            if i != 0:
                self.create_text(20, i, text=str(i), font=("Times New Roman", 10))

        # по оси абсцисс
        for i in range(0, self._width, 50):
            self.create_line(i, 0, i, 6, width=2)
            if i != 0:
                self.create_text(i, 20, text=str(i), font=("Times New Roman", 10))

    @property
    def color_bg(self) -> str:
        """
        Метод позволяет получить текущий цвет фона холста
        """

        return self._color_bg

    @color_bg.setter
    def color_bg(self, value: str) -> None:
        """
        Метод позволяет изменить цвет фона холста
        """
        self.config(bg=value)
        self._color_bg = value

    @property
    def color_figure(self) -> str:
        """
        Метод позволяет получить текущий цвет пользовательских отрезков
        """

        return self._color_figure

    @color_figure.setter
    def color_figure(self, value: str) -> None:
        """
        Метод позволяет изменить цвет пользовательских отрезков
        """
        self._color_figure = value

    @property
    def color_cutter(self) -> str:
        """
        Метод позволяет изменить цвет линии
        """
        return self._color_cutter

    @color_cutter.setter
    def color_cutter(self, value: str) -> None:
        """
        Метод позволяет получить текущий цвет линии
        """
        self._color_cutter = value

    @property
    def color_result(self) -> str:
        """
        Метод позволяет изменить цвет линии
        """
        return self._color_result

    @color_result.setter
    def color_result(self, value: str) -> None:
        """
        Метод позволяет получить текущий цвет линии
        """
        self._color_result = value

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self.delete(tk.ALL)
        self._img = self.__create_image()

        self._list_cutter[0].clean()
        self._list_figure[0].clean()

        self.__draw_axis()

    def create_point(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости
        """
        # +1 по абсциссе нужен лишь, чтобы отобразить точку размером в 1 пиксель
        # особенности tkinter
        self.create_line(x0, y0, x0 + 1, y0, fill=color)

    # методы конкретно для лабораторной работы

    def __create_image(self) -> tk.PhotoImage:
        """
        Метод будет создавать изображение на холсте и заполнять пиксели цветом фона холста
        Изображение нужно для того, чтобы можно было удобно получать цвет любого пикселя на холсте
        """
        # создали изображение
        img = tk.PhotoImage(width=self._width, height=self._height)
        # расположили его по центру холста
        self.create_image((self._width / 2, self._height / 2), image=img, state="normal")

        # в циклах по всему холсту устанавливаем каждый пиксель в цвет фона на изображении
        img.put(self.color_bg, to=(0, 0, self._width, self._height))

        return img

    def get_rgb_pixel(self, x: int | float, y: int | float) -> (int, int, int):
        """
        Метод позволяет получить кортеж rgb значений цвета пикселя на холсте
        """

        return self._img.get(round(x), round(y))

    def create_point_on_img(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости (на картинке)
        """
        self._img.put(color, (round(x0), round(y0)))

    def draw_line_on_img(self, point_start: Point, point_end: Point, color: str):
        """
        Метод позволяет отобразить линию на картинке, используя алгоритм
        Брезенхема для вещественных чисел
        """
        builder = Dda(point_start, point_end)
        points = builder.get_points_for_line(color_line=color)

        for point in points:
            self.create_point_on_img(point.x, point.y, color=color)

    def add_point_by_cutter(self, point: Point) -> None:
        """
        Метод обертка для добавления точки
        """
        if self._list_cutter[0].is_close:
            self.__update_cutter()

        # добавляется точка в отсекатель
        self._list_cutter[0].add_point(point)

    def add_point_by_figure(self, point: Point) -> None:
        """
        Метод обертка для добавления точки
        """
        if self._list_figure[0].is_close:
            self.__update_figure()

        # добавляется точка в отсекатель
        self._list_figure[0].add_point(point)

    def is_close_cutter(self) -> bool:
        """
        Метод, позволяющий определить, замкнут ли отсекатель
        """

        return self._list_cutter[0].is_close

    def is_close_figure(self) -> bool:
        """
        Метод, позволяющий определить, замкнута ли фигура
        """

        return self._list_figure[0].is_close

    def draw_edge_by_cutter(self):
        """
        Метод отображает ребро при получении точек отсекателя
        """
        curr_cutter = self._list_cutter[0]

        if len(curr_cutter) < 2:
            return

        point_last = curr_cutter[len(curr_cutter) - 1]
        point_prev = curr_cutter[len(curr_cutter) - 2]

        builder = Dda(point_prev, point_last)
        points = builder.get_points_for_line(color_line=BLACK)  # тут неважно какой цвет

        for point in points:
            self.create_point_on_img(point.x, point.y, color=self.color_cutter)

    def draw_edge_by_figure(self):
        """
        Метод отображает ребро при получении точек фигуры
        """
        curr_figure = self._list_figure[0]

        if len(curr_figure) < 2:
            return

        point_last = curr_figure[len(curr_figure) - 1]
        point_prev = curr_figure[len(curr_figure) - 2]

        builder = Dda(point_prev, point_last)
        points = builder.get_points_for_line(color_line=BLACK)  # тут неважно какой цвет

        for point in points:
            self.create_point_on_img(point.x, point.y, color=self.color_figure)

    def close_cutter(self):
        """
        Метод позволяет замкнуть фигуру
        """
        curr_cutter = self._list_cutter[0]

        if len(curr_cutter) == 0:
            text = "Точки не введены!"
            messagebox.showwarning("", text)
            return

        if len(curr_cutter) < 3:
            text = "Такую фигуру нельзя замкнуть!\n" \
                   "Необходимо как минимум, чтобы у фигуры было 3 точки!"
            messagebox.showwarning("", text)
            return

        point_last = curr_cutter[len(curr_cutter) - 1]
        point_start = curr_cutter[0]

        self._list_cutter[0].is_close = True

        builder = Dda(point_start, point_last)
        points = builder.get_points_for_line(color_line=BLACK)  # тут неважно какой цвет

        for point in points:
            self.create_point_on_img(point.x, point.y, color=self.color_cutter)

    def close_figure(self):
        """
        Метод позволяет замкнуть фигуру
        """
        curr_figure = self._list_figure[0]

        if len(curr_figure) == 0:
            text = "Точки не введены!"
            messagebox.showwarning("", text)
            return

        if len(curr_figure) < 3:
            text = "Такую фигуру нельзя замкнуть!\n" \
                   "Необходимо как минимум, чтобы у фигуры было 3 точки!"
            messagebox.showwarning("", text)
            return

        point_last = curr_figure[len(curr_figure) - 1]
        point_start = curr_figure[0]

        self._list_figure[0].is_close = True

        builder = Dda(point_start, point_last)
        points = builder.get_points_for_line(color_line=BLACK)  # тут неважно какой цвет

        for point in points:
            self.create_point_on_img(point.x, point.y, color=self.color_figure)

    def __update_cutter(self):
        """
        Вспомогательный метод для переопределения отсекателя
        """
        self.delete(tk.ALL)
        self._img = self.__create_image()

        self._list_cutter[0].clean()

        figure = self._list_figure[0]

        for i in range(len(figure)):
            if i == len(figure) - 1:
                self.draw_line_on_img(figure[i], figure[0], self.color_figure)
            else:
                self.draw_line_on_img(figure[i], figure[i + 1], self.color_figure)

        self.__draw_axis()

    def __update_figure(self):
        """
        Вспомогательный метод для переопределения отсекателя
        """
        self.delete(tk.ALL)
        self._img = self.__create_image()

        self._list_figure[0].clean()

        cutter = self._list_cutter[0]

        for i in range(len(cutter)):
            if i == len(cutter) - 1:
                self.draw_line_on_img(cutter[i], cutter[0], self.color_cutter)
            else:
                self.draw_line_on_img(cutter[i], cutter[i + 1], self.color_cutter)

        self.__draw_axis()

    def __add_mouse_point_cutter(self, event):
        """
        Метод позволяет добавить точку к отсекателю
        """
        x, y = self.get_point_by_click(event)

        point = Point(x=x, y=y)

        self.add_point_by_cutter(point)
        self.create_point_on_img(x, y, self.color_cutter)

        self.draw_edge_by_cutter()

    def __add_mouse_point_figure(self, event):
        """
        Метод позволяет добавить точку к фигуре
        """
        x, y = self.get_point_by_click(event)

        point = Point(x=x, y=y)

        self.add_point_by_figure(point)
        self.create_point_on_img(x, y, self.color_figure)

        self.draw_edge_by_figure()

    @staticmethod
    def get_point_by_click(event) -> (int, int):
        """
        Метод для получения координат точки с помощью мыши
        """
        x, y = event.x, event.y

        return x, y

    def cut(self):
        """
        Метод позволяет выполнить отсечение отрезков
        """
        if not self.is_close_cutter():
            messagebox.showwarning("", "Отсекатель не является замкнутым!")
            return

        if not self.is_close_figure():
            messagebox.showwarning("", "Фигура не является замкнутой!")
            return

        cutter_alg = SutherlandHodgman(self, self._img, self._list_figure, self._list_cutter, self._color_result)

        cutter_alg.cut()
