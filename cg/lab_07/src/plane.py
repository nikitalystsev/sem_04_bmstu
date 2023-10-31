import tkinter as tk

from PointClass import Point
from cutter import Cutter
from line import Line
from mid_point import MidPointMethod
from dda import Dda

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


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, color_cutter: str, color_line: str, color_result: str, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self._width = kwargs.get("width")
        self._height = kwargs.get("height")

        self._list_line: list[Line] = list()  # массив пользовательских отрезков
        self._list_cutter: list[Cutter] = list()  # массив отсекателей

        self._color_line: str = color_line  # цвет пользовательских отрезков
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
        self.bind("<Button-3>", self.get_line_by_click)  # правая кнопка мыши
        self.bind("<Button-1>", self.get_cutter_by_click)  # левая кнопка мыши

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
    def color_line(self) -> str:
        """
        Метод позволяет получить текущий цвет пользовательских отрезков
        """

        return self._color_line

    @color_line.setter
    def color_line(self, value: str) -> None:
        """
        Метод позволяет изменить цвет пользовательских отрезков
        """
        self._color_line = value

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

        self._list_cutter.clear()
        self._list_line.clear()

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

    def draw_line_on_img(self, point_start: Point, point_end: Point, color: str):
        """
        Метод позволяет отобразить линию на картинке, используя алгоритм
        Брезенхема для вещественных чисел
        """
        builder = Dda(point_start, point_end)
        points = builder.get_points_for_line(color_line=color)

        for point in points:
            self.create_point_on_img(point.x, point.y, color=color)

    def draw_cutter_on_img(self, cutter: Cutter, color: str):
        """
        Метод позволяет отобразить регулярный отсекатель на картинке
        """
        self.draw_line_on_img(cutter.point_top_left, cutter.point_top_right, color)
        self.draw_line_on_img(cutter.point_top_right, cutter.point_lower_right, color)
        self.draw_line_on_img(cutter.point_lower_right, cutter.point_lower_left, color)
        self.draw_line_on_img(cutter.point_lower_left, cutter.point_top_left, color)

    def get_rgb_pixel(self, x: int | float, y: int | float) -> (int, int, int):
        """
        Метод позволяет получить кортеж rgb значений цвета пикселя на холсте
        """

        return self._img.get(round(x), round(y))

    def add_line(self, ps: Point, pe: Point):
        """
        Метод позволяет добавить линию
        """
        self.draw_line_on_img(ps, pe, self.color_line)

        new_line = Line(ps, pe)
        self._list_line.append(new_line)

    def __update_cutter(self):
        """
        Вспомогательный метод для переопределения отсекателя
        """
        self.delete(tk.ALL)
        self._img = self.__create_image()

        self._list_cutter.clear()

        for line in self._list_line:
            self.draw_line_on_img(line.point_start, line.point_end, self.color_line)

        self.__draw_axis()

    def add_cutter(self, ptl: Point, plr: Point):
        """
        Метод позволяет добавить линию
        """
        cutter = Cutter(ptl, plr)
        self.__update_cutter()
        self._list_cutter.append(cutter)
        self.draw_cutter_on_img(cutter, color=self._color_cutter)

    def get_line_by_click(self, event) -> None:
        """
        Метод для получения линии с помощью мыши
        """
        x, y = event.x, event.y

        if len(self._list_line) == 0:  # если список линий пуст (добавляется самая первая линия)
            line = Line(point_start=Point(x=x, y=y))
            self._list_line.append(line)
        else:
            if self._list_line[-1].point_end is None:  # если добавили только начала отрезка
                self._list_line[-1].point_end = Point(x=x, y=y)  # то завершаем его
                self.draw_line_on_img(self._list_line[-1].point_start, self._list_line[-1].point_end, self.color_line)
            else:  # иначе создаем новый отрезок
                line = Line(point_start=Point(x=x, y=y))
                self._list_line.append(line)

    def get_cutter_by_click(self, event) -> None:
        """
        Метод для получения линии с помощью мыши
        """
        x, y = event.x, event.y

        if len(self._list_cutter) == 0:  # если список отсекателей пуст (добавляется первый отсекатель)
            cutter = Cutter(point_top_left=Point(x=x, y=y))
            self._list_cutter.append(cutter)
        else:
            if self._list_cutter[-1].point_lower_right is None:  # если добавили только начало отсекателя
                self._list_cutter[-1].point_lower_right = Point(x=x, y=y)  # то завершаем его
                self._list_cutter[-1].calc_other()  # вычисляем оставшиеся точки
                self.draw_cutter_on_img(self._list_cutter[-1], color=self.color_cutter)
            else:  # иначе создаем новый отрезок
                self.__update_cutter()
                cutter = Cutter(point_top_left=Point(x=x, y=y))
                self._list_cutter.append(cutter)

    def cut(self):
        """
        Метод позволяет выполнить отсечение отрезков
        """
        cutter_alg = MidPointMethod(self, self._img, self._list_line, self._list_cutter, self._color_result)

        cutter_alg.cut()
