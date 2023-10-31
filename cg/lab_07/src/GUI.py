# from tkinter import ttk
from tkinter import messagebox

from plane import *
from checks import *

# from PointClass import Point

FONT = "Times New Roman"

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
SteelBlue = "#4682B4"


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()
        self.title("Лабораторная №7, Лысцев Никита ИУ7-43Б")

        root_width = self.winfo_screenwidth()
        root_height = self.winfo_screenheight() - 65
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # self.bind("<Button-3>", self.__add_mouse_point)  # правая кнопка мыши
        # создал фреймы для всего
        # -----------------------------------------------
        self._frame_plane = self.__create_frame_plane()
        self._frame_plane.pack(side=tk.RIGHT)
        self._frame_widgets = self.__create_frame_widgets()
        self._frame_widgets.pack()
        # -----------------------------------------------

        self._plane = self.__create_plane()
        self._plane.pack()

        # виджет отображения используемого алгоритма
        # -----------------------------------------------
        self._lbl_title_septum_alg = self.__create_label("Реализуемый алгоритм заполнения:")
        self._lbl_title_septum_alg.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_title_septum_alg.grid(row=0, column=0, columnspan=4, sticky='wens')

        self._lbl_septum_alg = self.__create_label("Алгоритм средней точки")
        self._lbl_septum_alg.grid(row=1, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты для добавления точки
        # -----------------------------------------------
        self._lbl_add_line = self.__create_label("Добавление отрезка")
        self._lbl_add_line.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_add_line.grid(row=2, column=0, columnspan=4, sticky='wens')

        self._lbl_add_x_start = self.__create_label("X_start:")
        self._lbl_add_x_start.grid(row=3, column=0, sticky='wens')

        self._entry_add_x_start = self.__create_entry()
        self._entry_add_x_start.grid(row=3, column=1, sticky='wens')

        self._lbl_add_y_start = self.__create_label("Y_start:")
        self._lbl_add_y_start.grid(row=3, column=2, sticky='wens')

        self._entry_add_y_start = self.__create_entry()
        self._entry_add_y_start.grid(row=3, column=3, sticky='wens')

        self._lbl_add_x_end = self.__create_label("X_end:")
        self._lbl_add_x_end.grid(row=4, column=0, sticky='wens')

        self._entry_add_x_end = self.__create_entry()
        self._entry_add_x_end.grid(row=4, column=1, sticky='wens')

        self._lbl_add_y_end = self.__create_label("Y_end:")
        self._lbl_add_y_end.grid(row=4, column=2, sticky='wens')

        self._entry_add_y_end = self.__create_entry()
        self._entry_add_y_end.grid(row=4, column=3, sticky='wens')

        self._btn_add_line = self.__create_button("Добавить отрезок")
        self._btn_add_line.config(command=self.__add_line)
        self._btn_add_line.grid(row=5, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты для построения отсекателя
        # -----------------------------------------------
        self._lbl_add_cutter = self.__create_label("Добавление отсекателя")
        self._lbl_add_cutter.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_add_cutter.grid(row=6, column=0, columnspan=4, sticky='wens')

        self._lbl_add_x_top_left = self.__create_label("X_лв:")
        self._lbl_add_x_top_left.grid(row=7, column=0, sticky='wens')

        self._entry_add_x_top_left = self.__create_entry()
        self._entry_add_x_top_left.grid(row=7, column=1, sticky='wens')

        self._lbl_add_y_top_left = self.__create_label("Y_лв:")
        self._lbl_add_y_top_left.grid(row=7, column=2, sticky='wens')

        self._entry_add_y_top_left = self.__create_entry()
        self._entry_add_y_top_left.grid(row=7, column=3, sticky='wens')

        self._lbl_add_x_lower_right = self.__create_label("X_пн:")
        self._lbl_add_x_lower_right.grid(row=8, column=0, sticky='wens')

        self._entry_add_x_lower_right = self.__create_entry()
        self._entry_add_x_lower_right.grid(row=8, column=1, sticky='wens')

        self._lbl_add_y_lower_right = self.__create_label("Y_пн:")
        self._lbl_add_y_lower_right.grid(row=8, column=2, sticky='wens')

        self._entry_add_y_lower_right = self.__create_entry()
        self._entry_add_y_lower_right.grid(row=8, column=3, sticky='wens')

        self._btn_add_cutter = self.__create_button("Добавить отсекатель")
        self._btn_add_cutter.config(command=self.__add_cutter)
        self._btn_add_cutter.grid(row=9, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты выбора цвета
        # -----------------------------------------------
        self._lbl_choice_color = self.__create_label("Выбор цвета")
        self._lbl_choice_color.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_choice_color.grid(row=10, column=0, columnspan=4, sticky='wens')

        # фреймы выбора цвета заполнения
        self._frame_color_fill = tk.Frame(master=self._frame_widgets)
        self._frame_color_fill.grid(row=11, column=1, columnspan=2, sticky='wens')

        # разные цвета
        self._btn_black = self.__create_choice_color_button(SteelBlue)
        self._btn_black.pack(side=tk.LEFT)
        self._btn_red = self.__create_choice_color_button(RED)
        self._btn_red.pack(side=tk.LEFT)
        self._btn_orange = self.__create_choice_color_button(ORANGE)
        self._btn_orange.pack(side=tk.LEFT)
        self._btn_yellow = self.__create_choice_color_button(DARKCYAN)
        self._btn_yellow.pack(side=tk.LEFT)
        self._btn_green = self.__create_choice_color_button(GREEN)
        self._btn_green.pack(side=tk.LEFT)
        self._btn_blue = self.__create_choice_color_button(BLUE)
        self._btn_blue.pack(side=tk.LEFT)
        self._btn_violet = self.__create_choice_color_button(VIOLET)
        self._btn_violet.pack(side=tk.LEFT)

        self._values = "Текущий цвет отрезка", "Текущий цвет отсекателя", "Текущий цвет результата"
        self._rbt_var = tk.StringVar(value=self._values[0])

        self._rbt_line = self.__create_radiobutton(self._values[0])
        self._rbt_line.grid(row=12, column=0, columnspan=3, sticky='wens')

        self._curr_color_line = self.__create_label("")
        self._curr_color_line.config(bg=SteelBlue, relief=tk.SUNKEN)
        self._curr_color_line.grid(row=12, column=3, sticky='wens')

        self._rbt_cutter = self.__create_radiobutton(self._values[1])
        self._rbt_cutter.grid(row=13, column=0, columnspan=3, sticky='wens')

        self._curr_color_cutter = self.__create_label("")
        self._curr_color_cutter.config(bg=RED, relief=tk.SUNKEN)
        self._curr_color_cutter.grid(row=13, column=3, sticky='wens')

        self._rbt_result = self.__create_radiobutton(self._values[2])
        self._rbt_result.grid(row=14, column=0, columnspan=3, sticky='wens')

        self._curr_color_result = self.__create_label("")
        self._curr_color_result.config(bg=ORANGE, relief=tk.SUNKEN)
        self._curr_color_result.grid(row=14, column=3, sticky='wens')

        self._btn_cut_off = self.__create_button("Отсечь")
        self._btn_cut_off.config(command=self.__cut)
        self._btn_cut_off.grid(row=15, column=0, columnspan=4, sticky='wens')

        # виджеты справки
        # -----------------------------------------------
        self._btn_clean_plane = self.__create_button("Очистить экран")
        self._btn_clean_plane.config(command=self.__clean_plane)
        self._btn_clean_plane.grid(row=24, column=0, columnspan=4, sticky='wens')

        self._btn_info = self.__create_button("Справка")
        self._btn_info.config(command=self.__print_info)
        self._btn_info.grid(row=25, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

    def __create_frame_plane(self) -> tk.Frame:
        """
        Метод создает фрейм для плоскости (plane)
        :return: фрейм для плоскости
        """
        frame_plane_width = self.winfo_screenwidth() - 400
        frame_plane_height = self.winfo_screenheight() - 70

        frame_plane = tk.Frame(
            self,
            width=frame_plane_width,
            height=frame_plane_height
        )

        return frame_plane

    def __create_frame_widgets(self) -> tk.Frame:
        """
        Метод создает фрейм для виджетов
        :return: фрейм для виджетов
        """
        frame_widgets_width = 400

        frame_widgets = tk.Frame(
            self,
            width=frame_widgets_width,
        )

        for i in range(4):
            frame_widgets.columnconfigure(index=i, weight=1, minsize=99)

        return frame_widgets

    def __create_plane(self) -> PlaneCanvas:
        """
        Метод размещает холст (canvas) для плоскости (plane) на главном окне
        :return: холст
        """
        plane_width = self._frame_plane.winfo_screenwidth() - 400
        plane_height = self._frame_plane.winfo_screenheight() - 70

        plane = PlaneCanvas(
            color_line=SteelBlue,
            color_cutter=RED,
            color_result=ORANGE,
            master=self._frame_plane,
            width=plane_width,
            height=plane_height,
            bg=WHITE
        )

        return plane

    def __create_label(self, text: str) -> tk.Label:
        """
        Метод создает виджет текста (label)
        :param text: строка текста
        :return: виджет текста
        """
        label = tk.Label(
            self._frame_widgets,
            text=text,
            font=(FONT, 14, 'bold'),
        )

        return label

    def __create_entry(self) -> tk.Entry:
        """
        Метод создает виджет однострочного поля ввода (entry)
        :return: виджет однострочного поля ввода
        """
        entry = tk.Entry(
            self._frame_widgets,
            width=15,
            relief=tk.SUNKEN,
            borderwidth=5,
            justify=tk.CENTER,
            font=(FONT, 14)
        )

        return entry

    def __create_button(self, text: str) -> tk.Button:
        """
        Метод создает виджет кнопки (button)
        :param text:  текст
        :return: виджет кнопки
        """
        button = tk.Button(
            self._frame_widgets,
            text=text,
            font=(FONT, 12),
            relief=tk.RAISED
        )

        button.config(bg="#FFFFFF")

        return button

    def __create_radiobutton(self, text: str) -> tk.Radiobutton:
        """
        Метод создает переключатель 2-х множеств треугольника для ввода
        :param text: значение переключателя
        :return: переключатель 2-х множеств треугольника для ввода
        """
        rbt = tk.Radiobutton(
            self._frame_widgets,
            text=text,
            value=text,
            variable=self._rbt_var,
            font=(FONT, 14, 'bold', 'italic'),
            anchor=tk.W
        )

        return rbt

    def __create_choice_color_button(self, color: str) -> tk.Button:
        """
        Метод создает кнопку выбора цвета
        """
        btn = tk.Button(self._frame_color_fill, bg=color, activebackground=color)
        btn.config(command=lambda: self.__set_color(color))

        return btn

    @staticmethod
    def get_data(entry1: tk.Entry, entry2: tk.Entry) -> (str, str):
        """
        Метод получает данные с 2-х однострочных полей ввода координат
        :param entry1: поле ввода абсциссы
        :param entry2: поле вода ординаты
        :return: кортеж с данными
        """

        return entry1.get(), entry2.get()

    def __get_point(self, entry_x: tk.Entry, entry_y: tk.Entry) -> (int | float, int | float):
        """
        Метод получает точку с однострочных полей ввода координат
        :param entry_x: поле ввода абсциссы
        :param entry_y: поле вода ординаты
        :return:
        """
        x, y = self.get_data(entry_x, entry_y)

        x = int(x) if self.is_int(x) else float(x) if self.is_float(x) else x
        y = int(y) if self.is_int(y) else float(y) if self.is_float(y) else y

        return x, y

    @staticmethod
    def __check_input_point(x: int | float, y: int | float) -> bool:
        """
        Метод проверяет введенную точку на корректность
        :param x: абсцисса точки
        :param y: ордината точки
        :return: True, если точка валидная, False иначе
        """
        if isinstance(x, str) or isinstance(y, str):
            text = "Некорректные данные для точки! Попробуйте снова."
            messagebox.showwarning("", text)

            return False

        return True

    @staticmethod
    def is_int(x: str) -> bool:
        """
        Метод проверяет, является ли строка целым числом
        :param x: строка
        :return: True, если целое число, False иначе
        """
        if check_int(x):
            return True

        return False

    @staticmethod
    def is_float(x: str) -> bool:
        """
        Метод проверяет, число ли переданный параметр.
        :param x:
        :return: True, если число, False иначе
        """
        if check_float(x):
            return True

        return False

    # методы для лабораторной

    # метод для установки цвета заполнения
    # -----------------------------------------------------------------
    def __set_color(self, color: str) -> None:
        """
        Метод для установки цвета заполнения
        """
        match self._rbt_var.get():
            case "Текущий цвет отрезка":
                self._curr_color_line.config(bg=color)
                self._plane.color_line = color
            case "Текущий цвет отсекателя":
                self._curr_color_cutter.config(bg=color)
                self._plane.color_cutter = color
            case "Текущий цвет результата":
                self._curr_color_result.config(bg=color)
                self._plane.color_result = color

    # -----------------------------------------------------------------

    def __add_line(self):
        """
        Метод позволяет добавить отрезок с поля ввода
        """
        x1, y1 = self.__get_point(self._entry_add_x_start, self._entry_add_y_start)
        x2, y2 = self.__get_point(self._entry_add_x_end, self._entry_add_y_end)

        if not self.__check_input_point(x1, y1) or not self.__check_input_point(x2, y2):
            return

        self._plane.add_line(Point(x1, y1), Point(x2, y2))

    def __add_cutter(self):
        """
        Метод позволяет добавить отсекатель
        """
        x1, y1 = self.__get_point(self._entry_add_x_top_left, self._entry_add_y_top_left)
        x2, y2 = self.__get_point(self._entry_add_x_lower_right, self._entry_add_y_lower_right)

        if not self.__check_input_point(x1, y1) or not self.__check_input_point(x2, y2):
            return

        self._plane.add_cutter(Point(x1, y1), Point(x2, y2))

    # очистка и справка
    # -----------------------------------------------------------------
    def __clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self._plane.clean_plane()

    @staticmethod
    def __print_info() -> None:
        """
        Метод выводит информацию о программе
        """
        text = 'С помощью данной программы можно выполнить отсечения произвольного ' \
               'количества отрезков регулярным прямоугольным отсекателем, ' \
               'используя алгоритм разбиения отрезка средней точкой.\n'

        messagebox.showinfo('', text)

    # -----------------------------------------------------------------

    def __cut(self):
        """
        Метод позволяет выполнить отсечение
        """
        self._plane.cut()
