import tkinter as tk
from tkinter import messagebox

from PointClass import Point
from figure import Figure
from measurements import CompareTime
from bresenham import BresenhamFloat, BresenhamEllipse
from seed_line_fill import SeedLineFill

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


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, color_fill: str, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self._width = kwargs.get("width")
        self._height = kwargs.get("height")
        self._color_fill: str = color_fill
        self._color_bg: str = self["bg"]

        self._list_figure: list[Figure] = [Figure()]  # список фигур
        self._item: int = 0  # индекс текущей обрабатываемой фигуры
        self._seed_point: Point = Point(0, 0)  # первая затравочная точка

        # определим возможные цвета заполнения (используя словарь)
        self.dict_colors_figure = {
            (0, 139, 139): "DarkCyan",
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

        # Привязываем функцию left_click к событию нажатия правой кнопки мыши на холсте
        self.bind("<Button-3>", self.get_point_by_click)  # правая кнопка мыши
        self.bind("<Shift-Button-1>", self.get_seed_point)  # Shift и левая кнопка мыши
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
    def color_fill(self) -> str:
        """
        Метод позволяет изменить цвет линии
        """
        return self._color_fill

    @color_fill.setter
    def color_fill(self, value: str) -> None:
        """
        Метод позволяет получить текущий цвет линии
        """
        self._color_fill = value

    @property
    def seed_point(self) -> Point:
        """
        Метод позволяет получить затравочную точку
        """

        return self._seed_point

    @seed_point.setter
    def seed_point(self, value: Point):
        """
        Метод позволяет установить значение затравочной точки
        """
        self._seed_point = value

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self.delete(tk.ALL)
        self._img = self.__create_image()

        for figure in self._list_figure:
            figure.clean()
        self._list_figure.clear()
        self._list_figure.append(Figure())
        self._item = 0
        self.seed_point = Point(x=0, y=0)

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

    def create_point_on_img(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости (на картинке)
        """
        self._img.put(color, (round(x0), round(y0)))

    def get_rgb_pixel(self, x: int | float, y: int | float) -> (int, int, int):
        """
        Метод позволяет получить кортеж rgb значений цвета пикселя на холсте
        """

        return self._img.get(round(x), round(y))

    def draw_ellipse(self, alg: BresenhamEllipse) -> None:
        """
        Метод отобразит окружность одним из алгоритмов
        """
        points = alg.create_ellipse(BLACK)
        ellipse_figure = Figure()

        for point in points:
            ellipse_figure.add_point(point)
            self.create_point_on_img(point.x, point.y, point.color)

        self._item += 1
        ellipse_figure.is_close = True
        self._list_figure.append(ellipse_figure)

    @staticmethod
    def get_point_by_click(event) -> (int, int):
        """
        Метод для получения координат точки с помощью мыши
        """
        x, y = event.x, event.y

        return x, y

    def get_seed_point(self, event) -> (int, int):
        """
        Метод для получения первой затравочной точки
        """
        x, y = event.x, event.y

        self._seed_point = Point(x=x, y=y)
        messagebox.showinfo("", f"Затравочная точка с координатами ({event.x}, {event.y}) была успешно добавлена!")

        return self._seed_point

    def add_point(self, point: Point) -> None:
        """
        Метод обертка для добавления точки
        """
        if self._list_figure[self._item].is_close:
            new_figure = Figure()
            self._list_figure.append(new_figure)
            self._item += 1

        # добавляется точка в какую то конкретную фигуру
        self._list_figure[self._item].add_point(point)

    def is_close(self) -> bool:
        """
        Метод, позволяющий определить, замкнута ли какая-то конкретная фигура
        """

        return self._list_figure[self._item].is_close

    def draw_edge(self):
        """
        Метод отображает ребро при получении точек
        """
        curr_figure = self._list_figure[self._item]

        if len(curr_figure) < 2:
            return

        point_last = curr_figure[len(curr_figure) - 1]
        point_prev = curr_figure[len(curr_figure) - 2]

        builder = BresenhamFloat(point_prev, point_last)
        points = builder.get_points_for_line(color_line=self.color_fill)  # тут неважно какой цвет

        for point in points:
            self.create_point_on_img(point.x, point.y, color=BLACK)

    def close(self):
        """
        Метод позволяет замкнуть фигуру
        """
        curr_figure = self._list_figure[self._item]

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

        self._list_figure[self._item].is_close = True

        builder = BresenhamFloat(point_start, point_last)
        points = builder.get_points_for_line(color_line=self.color_fill)  # тут неважно какой цвет

        for point in points:
            self.create_point_on_img(point.x, point.y, color=BLACK)

    def all_is_close(self):
        """
        Метод позволяет определить замкнуты ли все фигуры
        """
        for figure in self._list_figure:
            if not figure.is_close:
                return False

        return True

    def fill(self, delay_mode=False) -> float:
        """
        Метод обертка для заполнения фигуры
        """

        filler = SeedLineFill(self, self._img, BLACK, self.color_fill, self._seed_point, self.dict_colors_figure)

        work_time = 0

        if delay_mode:
            filler.fill(delay_mode=delay_mode)
        else:
            work_time = CompareTime.time_now()
            filler.fill()
            work_time = CompareTime.time_now() - work_time

        return work_time
