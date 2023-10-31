# from tkinter import ttk
from tkinter import messagebox

from plane import *
from checks import *
from functions import *

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
        self.title("Лабораторная №10, Лысцев Никита ИУ7-43Б")

        root_width = self.winfo_screenwidth()
        root_height = self.winfo_screenheight() - 65
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # создал фреймы для всего
        # -----------------------------------------------
        self._frame_plane = self.__create_frame_plane()
        self._frame_plane.pack(side=tk.RIGHT)
        self._frame_widgets = self.__create_frame_widgets()
        self._frame_widgets.pack()
        # -----------------------------------------------

        self._plane = self.__create_plane()
        self._plane.pack()

        # реализуемые функции
        self._tuple_funcs = ("cos(x) * sin(z)",
                             "sqrt(fabs(x * z))",
                             "exp(cos(x) * sin(z))",
                             "sin(x * z)")

        # виджеты для выбора отображаемой функции
        # -----------------------------------------------
        self._lbl_choice_func = self.__create_label("Выбор функции")
        self._lbl_choice_func.config(font=(FONT, 18, 'bold', "underline"))
        self._lbl_choice_func.grid(row=0, column=0, columnspan=4, sticky='wens')

        self._rbt_funcs = tk.StringVar(value=self._tuple_funcs[0])

        self._btn_func0 = self.__create_radiobutton(self._tuple_funcs[0])
        self._btn_func0.grid(row=1, column=1, columnspan=3, sticky='wens')

        self._btn_func1 = self.__create_radiobutton(self._tuple_funcs[1])
        self._btn_func1.grid(row=2, column=1, columnspan=3, sticky='wens')

        self._btn_func2 = self.__create_radiobutton(self._tuple_funcs[2])
        self._btn_func2.grid(row=3, column=1, columnspan=3, sticky='wens')

        self._btn_func3 = self.__create_radiobutton(self._tuple_funcs[3])
        self._btn_func3.grid(row=4, column=1, columnspan=3, sticky='wens')

        self._btn_print_graph = self.__create_button("Отобразить график")
        self._btn_print_graph.config(command=self.__create_graph, font=(FONT, 16))
        self._btn_print_graph.grid(row=5, column=0, columnspan=4, sticky='wens')

        # виджеты для выбора пределов и шага по осям Ox и Oz
        # -----------------------------------------------
        self._lbl_choice_limits = self.__create_label("Выбор пределов")
        self._lbl_choice_limits.config(font=(FONT, 18, 'bold', "underline"))
        self._lbl_choice_limits.grid(row=6, column=0, columnspan=4, sticky='wens')

        self._lbl_from = self.__create_label("От: ")
        self._lbl_from.grid(row=7, column=1, sticky='wens')

        self._lbl_to = self.__create_label("До: ")
        self._lbl_to.grid(row=7, column=2, sticky='wens')

        self._lbl_step = self.__create_label("Шаг: ")
        self._lbl_step.grid(row=7, column=3, sticky='wens')

        self._lbl_x_axis = self.__create_label("Ось X: ")
        self._lbl_x_axis.grid(row=8, column=0, sticky='wens')

        self._entry_x_from = self.__create_entry()
        self._entry_x_from.grid(row=8, column=1, sticky='wens')

        self._entry_x_to = self.__create_entry()
        self._entry_x_to.grid(row=8, column=2, sticky='wens')

        self._entry_x_step = self.__create_entry()
        self._entry_x_step.grid(row=8, column=3, sticky='wens')

        self._lbl_z_axis = self.__create_label("Ось Z: ")
        self._lbl_z_axis.grid(row=9, column=0, sticky='wens')

        self._entry_z_from = self.__create_entry()
        self._entry_z_from.grid(row=9, column=1, sticky='wens')

        self._entry_z_to = self.__create_entry()
        self._entry_z_to.grid(row=9, column=2, sticky='wens')

        self._entry_z_step = self.__create_entry()
        self._entry_z_step.grid(row=9, column=3, sticky='wens')

        # виджеты для вращения фигуры
        # -----------------------------------------------
        self._lbl_rotate = self.__create_label("Вращение поверхности")
        self._lbl_rotate.config(font=(FONT, 18, 'bold', "underline"))
        self._lbl_rotate.grid(row=10, column=0, columnspan=4, sticky='wens')

        self._lbl_x_rotate = self.__create_label("Ось X: ")
        self._lbl_x_rotate.grid(row=11, column=0, sticky='wens')

        self._entry_x_rotate = self.__create_entry()
        self._entry_x_rotate.grid(row=11, column=1, sticky='wens')

        self._btn_x_rotate = self.__create_button("Повернуть")
        self._btn_x_rotate.config(command=self.__rotate_graph_around_x, font=(FONT, 16))
        self._btn_x_rotate.grid(row=11, column=2, columnspan=2, sticky='wens')

        self._lbl_y_rotate = self.__create_label("Ось Y: ")
        self._lbl_y_rotate.grid(row=12, column=0, sticky='wens')

        self._entry_y_rotate = self.__create_entry()
        self._entry_y_rotate.grid(row=12, column=1, sticky='wens')

        self._btn_y_rotate = self.__create_button("Повернуть")
        self._btn_y_rotate.config(command=self.__rotate_graph_around_y, font=(FONT, 16))
        self._btn_y_rotate.grid(row=12, column=2, columnspan=2, sticky='wens')

        self._lbl_z_rotate = self.__create_label("Ось Z: ")
        self._lbl_z_rotate.grid(row=13, column=0, sticky='wens')

        self._entry_z_rotate = self.__create_entry()
        self._entry_z_rotate.grid(row=13, column=1, sticky='wens')

        self._btn_z_rotate = self.__create_button("Повернуть")
        self._btn_z_rotate.config(command=self.__rotate_graph_around_z, font=(FONT, 16))
        self._btn_z_rotate.grid(row=13, column=2, columnspan=2, sticky='wens')

        # виджеты справки
        # -----------------------------------------------
        self._btn_clean_plane = self.__create_button("Очистить экран")
        self._btn_clean_plane.config(command=self.__clean_plane, font=(FONT, 16))
        self._btn_clean_plane.grid(row=24, column=0, columnspan=4, sticky='wens')

        self._btn_info = self.__create_button("Справка")
        self._btn_info.config(command=self.__print_info, font=(FONT, 16))
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
            variable=self._rbt_funcs,
            font=(FONT, 16, 'bold'),
            anchor=tk.W
        )

        return rbt

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

    def __draw_func(self, func: Callable[[int | float, int | float], int | float]):
        """
        Метод позволяет отобразить поверхность для переданной функции
        """
        x_from = float(self._entry_x_from.get())
        x_to = float(self._entry_x_to.get())

        z_from = float(self._entry_z_from.get())
        z_to = float(self._entry_z_to.get())

        x_step = float(self._entry_x_step.get())
        z_step = float(self._entry_x_step.get())

        # углы все изначально по нулям
        self._plane.draw_func([x_from, x_to], [z_from, z_to], x_step, z_step, func)

    def __create_graph(self):
        """
        Метод, позволяющий отобразить поверхность
        """
        match self._rbt_funcs.get():
            case "cos(x) * sin(z)":
                self.__draw_func(func=f0)
            case "sqrt(fabs(x * z))":
                self.__draw_func(func=f1)
            case "exp(cos(x) * sin(z))":
                self.__draw_func(func=f2)
            case "sin(x * z)":
                self.__draw_func(func=f3)
            case _:
                print("Не то")

    def __rotate_func_around_x(self, func: Callable[[int | float, int | float], int | float]):
        """
        Метод позволяет отобразить поверхность для переданной функции
        """
        x_from = float(self._entry_x_from.get())
        x_to = float(self._entry_x_to.get())

        z_from = float(self._entry_z_from.get())
        z_to = float(self._entry_z_to.get())

        x_step = float(self._entry_x_step.get())
        z_step = float(self._entry_x_step.get())

        angle_x = float(self._entry_x_rotate.get())

        self._plane.rotate_around_x([x_from, x_to], [z_from, z_to], x_step, z_step, func, angle_x)

    def __rotate_graph_around_x(self):
        """
        Метод, позволяющий отобразить поверхность
        """
        match self._rbt_funcs.get():
            case "cos(x) * sin(z)":
                self.__rotate_func_around_x(func=f0)
            case "sqrt(fabs(x * z))":
                self.__rotate_func_around_x(func=f1)
            case "exp(cos(x) * sin(z))":
                self.__rotate_func_around_x(func=f2)
            case "sin(x * z)":
                self.__rotate_func_around_x(func=f3)
            case _:
                print("Не то")

    def __rotate_func_around_y(self, func: Callable[[int | float, int | float], int | float]):
        """
        Метод позволяет отобразить поверхность для переданной функции
        """
        x_from = float(self._entry_x_from.get())
        x_to = float(self._entry_x_to.get())

        z_from = float(self._entry_z_from.get())
        z_to = float(self._entry_z_to.get())

        x_step = float(self._entry_x_step.get())
        z_step = float(self._entry_x_step.get())

        angle_y = float(self._entry_x_rotate.get())

        self._plane.rotate_around_y([x_from, x_to], [z_from, z_to], x_step, z_step, func, angle_y)

    def __rotate_graph_around_y(self):
        """
        Метод, позволяющий отобразить поверхность
        """
        match self._rbt_funcs.get():
            case "cos(x) * sin(z)":
                self.__rotate_func_around_y(func=f0)
            case "sqrt(fabs(x * z))":
                self.__rotate_func_around_y(func=f1)
            case "exp(cos(x) * sin(z))":
                self.__rotate_func_around_y(func=f2)
            case "sin(x * z)":
                self.__rotate_func_around_y(func=f3)
            case _:
                print("Не то")

    def __rotate_func_around_z(self, func: Callable[[int | float, int | float], int | float]):
        """
        Метод позволяет отобразить поверхность для переданной функции
        """
        x_from = float(self._entry_x_from.get())
        x_to = float(self._entry_x_to.get())

        z_from = float(self._entry_z_from.get())
        z_to = float(self._entry_z_to.get())

        x_step = float(self._entry_x_step.get())
        z_step = float(self._entry_x_step.get())

        angle_z = float(self._entry_x_rotate.get())

        self._plane.rotate_around_z([x_from, x_to], [z_from, z_to], x_step, z_step, func, angle_z)

    def __rotate_graph_around_z(self):
        """
        Метод, позволяющий отобразить поверхность
        """
        match self._rbt_funcs.get():
            case "cos(x) * sin(z)":
                self.__rotate_func_around_z(func=f0)
            case "sqrt(fabs(x * z))":
                self.__rotate_func_around_z(func=f1)
            case "exp(cos(x) * sin(z))":
                self.__rotate_func_around_z(func=f2)
            case "sin(x * z)":
                self.__rotate_func_around_z(func=f3)
            case _:
                print("Не то")

    # -----------------------------------------------------------------

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
        text = 'С помощью данной программы можно выполнить построение заранее выбранной поверхности ' \
               'используя алгоритм плавающего горизонта.\n'

        messagebox.showinfo('', text)
