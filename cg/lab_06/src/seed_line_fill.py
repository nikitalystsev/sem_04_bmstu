import tkinter
from tkinter import PhotoImage

from PointClass import Point


class SeedLineFill:
    """
    Класс для заполнения произвольной многоугольной области,
    а также области, ограниченной произвольной замкнутой кривой
    построчным алгоритмом заполнения с затравкой
    """

    def __init__(
            self,
            canvas: tkinter.Canvas,
            img: PhotoImage,
            color_bg: str,
            color_fill: str,
            seed_point: Point,
            dict_color_fill: dict
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._canvas: tkinter.Canvas = canvas
        self._img: PhotoImage = img
        self._color_bg: str = color_bg
        self._color_fill: str = color_fill
        self._seed_point: Point = seed_point
        self._dict_color_fill: dict = dict_color_fill

    def __get_str_color(self, x: int | float, y: int | float):
        """
        Метод позволяет получить строковое описание цвета через rgb и словарь
        возможных цветов заполнения
        """
        color_pixel = self._img.get(round(x), round(y))  # в rgb
        color_pixel = self._dict_color_fill[color_pixel]  # как строка

        return color_pixel

    def __create_point_on_img(self, x0: int, y0: int, color: str) -> None:
        """
        Метод отображает точку на плоскости (на картинке)
        """
        self._img.put(color, (round(x0), round(y0)))

    def __fill_right(self, x: int | float, y: int | float):
        """
        Метод закрашивает пиксели справа от затравочного, пока не встретит границу
        """

        # Пока что цвет пиксела не равен цвету границы
        while self.__get_str_color(x, y) != self._color_bg:
            # закрашиваем пиксель
            self.__create_point_on_img(x, y, self._color_fill)
            # увеличиваем x (идем вправо)
            x += 1

        # Возвращаем x - 1
        # Т.к. после цикла пиксель с координатами (x, y)
        # Будет равен цвету границы, а нам нужно взять
        # Крайний справа пиксель, т.е. пиксель,
        # Который находится справа от границы.

        return x - 1

    def __fill_left(self, x: int | float, y: int | float):
        """
        Метод закрашивает пиксели слева от затравочного, пока не встретит границу
        """
        # Пока что цвет пиксела не равен цвету границы
        while self.__get_str_color(x, y) != self._color_bg:
            # закрашиваем пиксель
            self.__create_point_on_img(x, y, self._color_fill)
            # Уменьшаем x (Идем влево)
            x -= 1

        # Возвращаем x + 1
        # Т.к. нам нужен крайний слева пиксель.

        return x + 1

    def __fill_right_delay(self, x: int | float, y: int | float):
        """
        Метод закрашивает пиксели справа от затравочного, пока не встретит границу
        С задержкой
        """
        while self.__get_str_color(x, y) != self._color_bg:
            self._canvas.after(0, self.__create_point_on_img(x, y, self._color_fill))
            self._canvas.update()

            x += 1

        return x - 1

    def __fill_left_delay(self, x: int | float, y: int | float):
        """
        Метод закрашивает пиксели слева от затравочного, пока не встретит границу
        """
        while self.__get_str_color(x, y) != self._color_bg:
            self._canvas.after(0, self.__create_point_on_img(x, y, self._color_fill))
            self._canvas.update()

            x -= 1

        return x + 1

    def __find_pixel(self, stack: list, x_right: int | float, x: int | float, y: int | float):
        """
        Метод для нахождения нового затравочного пикселя
        """
        while x <= x_right:
            # Флаг - признак нахождения нового затравочного пикселя.
            is_find_seed = False
            # Пока цвет текущего пикселя не равен цвету заполнения и не равен граничному цвету и x <= x_right
            while self.__get_str_color(x, y) != self._color_bg and \
                    self.__get_str_color(x, y) != self._color_fill and x <= x_right:
                # Нашли затравочный пиксель.
                if is_find_seed is False:
                    is_find_seed = True
                x += 1

            # Если нашли новый пиксель, то помещаем его в стек.
            if is_find_seed:
                if x == x_right and self.__get_str_color(x, y) != self._color_bg and \
                        self.__get_str_color(x, y) != self._color_fill:
                    stack.append(Point(x=x, y=y))
                else:
                    stack.append(Point(x=(x - 1), y=y))
                # is_find_seed = False

            # Продолжаем проверку (Если интервал был прерван)
            x_temp = x
            while self.__get_str_color(x, y) == self._color_bg and \
                    self.__get_str_color(x, y) == self._color_fill and x < x_right:
                x += 1

            if x == x_temp:
                x += 1

        return stack

    def fill(self, delay_mode=False):
        """
        Метод осуществляет заполнение
        """
        stack = [self._seed_point]  # заносим затравочный пиксель в стек

        while stack:
            seed_pixel = stack.pop()  # извлекаем затравочный пиксель из стека

            # закрашиваем его
            self.__create_point_on_img(seed_pixel.x, seed_pixel.y, self._color_fill)

            # Заполняем все пиксели справа от затравочной точки до того момента,
            # Пока что не встретим пиксель с цветом границы.
            # В переменную x_right запоминаем крайний правый пиксель.
            if delay_mode:
                x_right = self.__fill_right_delay(seed_pixel.x + 1, seed_pixel.y)
            else:
                x_right = self.__fill_right(seed_pixel.x + 1, seed_pixel.y)

            # Заполняем все пиксели слева от затравочной точки до того момента,
            # Пока что не встретим пиксель с цветом границы.
            # В переменную x_left запоминаем крайний левый пиксель.
            if delay_mode:
                x_left = self.__fill_left_delay(seed_pixel.x - 1, seed_pixel.y)
            else:
                x_left = self.__fill_left(seed_pixel.x - 1, seed_pixel.y)

            # На строке выше в диапазоне от x_left <= x <= x_right
            # Ищем новые затравочные пиксели и помещаем их в стек.
            stack = self.__find_pixel(stack, x_right, x_left, seed_pixel.y + 1)

            # На строке ниже в диапазоне от x_left <= x <= x_right
            # Ищем новые затравочные пиксели и помещаем их в стек.
            stack = self.__find_pixel(stack, x_right, x_left, seed_pixel.y - 1)
