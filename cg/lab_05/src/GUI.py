from tkinter import ttk

from plane import *
from checks import *
from listpoints import ListPoints
from PointClass import Point

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


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()
        self.title("Лабораторная №5, Лысцев Никита ИУ7-43Б")

        root_width = self.winfo_screenwidth()
        root_height = self.winfo_screenheight() - 65
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        self.bind("<Button-3>", self.__add_mouse_point)  # правая кнопка мыши
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

        self._lbl_septum_alg = self.__create_label("Алгоритм заполнения с перегородкой")
        self._lbl_septum_alg.grid(row=1, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты для добавления точки
        # -----------------------------------------------
        self._lbl_add_point = self.__create_label("Добавить точку")
        self._lbl_add_point.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_add_point.grid(row=2, column=0, columnspan=4, sticky='wens')

        self._lbl_add_x = self.__create_label("X:")
        self._lbl_add_x.grid(row=3, column=0, sticky='wens')

        self._entry_add_x = self.__create_entry()
        self._entry_add_x.grid(row=3, column=1, sticky='wens')

        self._lbl_add_y = self.__create_label("Y:")
        self._lbl_add_y.grid(row=3, column=2, sticky='wens')

        self._entry_add_y = self.__create_entry()
        self._entry_add_y.grid(row=3, column=3, sticky='wens')

        self._btn_add_point = self.__create_button("Добавить точку")
        self._btn_add_point.config(command=self.__add_point)
        self._btn_add_point.grid(row=4, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # # виджеты удаления точки по номеру (скорее не дам такой возможности)
        # # -----------------------------------------------
        # self._lbl_add_point = self.__create_label("Удалить точку")
        # self._lbl_add_point.config(font=(FONT, 16, 'bold', "underline"))
        # self._lbl_add_point.grid(row=5, column=0, columnspan=4, sticky='wens')
        #
        # self._lbl_n_del = self.__create_label("Номер точки:")
        # self._lbl_n_del.grid(row=6, column=0, sticky='wens', columnspan=2)
        #
        # self._entry_n_del = self.__create_entry()
        # self._entry_n_del.grid(row=6, column=2, sticky='wens', columnspan=2)
        #
        # self._btn_del_point = self.__create_button("Удалить точку")
        # self._btn_del_point.grid(row=7, column=0, columnspan=4, sticky='wens')
        # # -----------------------------------------------

        # виджеты для таблицы с точками
        # -----------------------------------------------
        self._lbl_list_points = self.__create_label("Добавленные точки:")
        self._lbl_list_points.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_list_points.grid(row=7, column=0, columnspan=4, sticky='wens')

        self._columns = "number", "point_x", "point_y"

        self._list_points = self.__create_listpoints(self._frame_widgets)
        self._list_points.grid(row=8, column=0, columnspan=3, sticky='wens')

        self._scrollbar = self.__create_scrollbars()
        self._scrollbar.grid(row=8, column=3, columnspan=1, sticky='wens')

        self._close_figure = self.__create_button("Замкнуть фигуру")
        self._close_figure.config(command=self.__close)
        self._close_figure.grid(row=9, column=0, columnspan=4, sticky='wens')

        self._close_figure = self.__create_button("Выполнить закраску")
        self._close_figure.config(command=self.__fill)
        self._close_figure.grid(row=10, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджет выбора задержки
        # -----------------------------------------------
        self._lbl_choice_delay = self.__create_label("Выбор типа закраски:")
        self._lbl_choice_delay.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_choice_delay.grid(row=11, column=0, columnspan=4, sticky='wens')

        self._values = "Без задержки", "С задержкой"
        self._rbt_var = tk.StringVar(value=self._values[0])

        self._rbt_delay = self.__create_radiobutton(self._values[0])
        self._rbt_delay.grid(row=12, column=0, columnspan=2, sticky='wens')

        self._rbt_no_delay = self.__create_radiobutton(self._values[1])
        self._rbt_no_delay.grid(row=12, column=2, columnspan=2, sticky='wens')
        # -----------------------------------------------

        # виджеты для выбора цвета заполнения
        # -----------------------------------------------
        self._lbl_choice_color_fill = self.__create_label("Выбор цвета заполнения:")
        self._lbl_choice_color_fill.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_choice_color_fill.grid(row=13, column=0, columnspan=4, sticky='wens')

        # фреймы выбора цвета заполнения
        self._frame_color_fill = tk.Frame(master=self._frame_widgets)
        self._frame_color_fill.grid(row=14, column=1, columnspan=2, sticky='wens')

        # разные цвета
        self._btn_black = self.__create_choice_color_button(DARKCYAN)
        self._btn_black.pack(side=tk.LEFT)
        self._btn_red = self.__create_choice_color_button(RED)
        self._btn_red.pack(side=tk.LEFT)
        self._btn_orange = self.__create_choice_color_button(ORANGE)
        self._btn_orange.pack(side=tk.LEFT)
        self._btn_yellow = self.__create_choice_color_button(YELLOW)
        self._btn_yellow.pack(side=tk.LEFT)
        self._btn_green = self.__create_choice_color_button(GREEN)
        self._btn_green.pack(side=tk.LEFT)
        self._btn_blue = self.__create_choice_color_button(BLUE)
        self._btn_blue.pack(side=tk.LEFT)
        self._btn_violet = self.__create_choice_color_button(VIOLET)
        self._btn_violet.pack(side=tk.LEFT)

        self._lbl_curr_color_fill = self.__create_label("Текущий цвет заполнения: ")
        self._lbl_curr_color_fill.grid(row=15, column=0, columnspan=4, sticky='wens')

        self._curr_color_fill = self.__create_label("")
        self._curr_color_fill.config(bg=self._plane.color_fill, relief=tk.SUNKEN)
        self._curr_color_fill.grid(row=16, column=1, columnspan=2, sticky='wens')
        # -----------------------------------------------

        # виджеты вывода времени работы алгоритма
        # -----------------------------------------------
        self._lbl_time_work = self.__create_label("Время работы алгоритма:")
        self._lbl_time_work.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_time_work.grid(row=17, column=0, columnspan=4, sticky='wens')

        self.text_var_time = tk.StringVar()
        self.text_var_time.set(f"{0: .2f} секунд")

        self._time_work = self.__create_label("")
        self._time_work.config(textvariable=self.text_var_time)
        self._time_work.grid(row=18, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------
        # виджеты справки
        # -----------------------------------------------
        self._btn_clean_plane = self.__create_button("Очистить экран")
        self._btn_clean_plane.config(command=self.__clean_plane)
        self._btn_clean_plane.grid(row=19, column=0, columnspan=4, sticky='wens')

        self._btn_info = self.__create_button("Справка")
        self._btn_info.config(command=self.__print_info)
        self._btn_info.grid(row=120, column=0, columnspan=4, sticky='wens')
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
            color_fill=DARKCYAN,
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

    def __create_listpoints(self, frame: tk.Frame) -> ListPoints:
        """
        Метод создает таблицу для отображения точек
        :param frame: окно
        :return: фрейм
        """
        listpoints = ListPoints(
            frame,
            columns=self._columns,
            show="headings",
            height=14
        )

        return listpoints

    def __create_scrollbars(self) -> ttk.Scrollbar:
        """
        Метод создает полосу прокрутки для отображенных точек
        :return: полосу прокрутки
        """
        scrollbar = ttk.Scrollbar(self._frame_widgets, command=self._list_points.yview)
        self._list_points.config(yscrollcommand=scrollbar.set)

        return scrollbar

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
        btn.config(command=lambda: self.__set_color_fill(color))

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

    def __set_color_fill(self, color: str) -> None:
        """
        Метод для установки цвета заполнения
        """
        self._plane.color_fill = color
        self._curr_color_fill.config(bg=self._plane.color_fill)

    def __get_point(self, entry_x: tk.Entry, entry_y: tk.Entry) -> (int | float, int | float):
        """
        Метод получает точку с однострочных полей ввода координат
        :param entry_x: поле ввода абсциссы
        :param entry_y: поле вода ординаты
        :return:
        """
        x, y = entry_x.get(), entry_y.get()

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

    def __add_point(self) -> None:
        """
        Метод добавляет точку в таблицу
        """
        x, y = self.__get_point(self._entry_add_x, self._entry_add_y)

        if not self.__check_input_point(x, y):
            return

        point = Point(x=x, y=y)

        self._list_points.add_point(point)
        self._plane.add_point(point)
        self._plane.create_point(x, y, color=self._plane.color_fill)

        self._plane.draw_edge()

    @staticmethod
    def __print_info() -> None:
        """
        Метод выводит информацию о программе
        """
        text = 'С помощью данной программы можно выполнить заполнение произвольной многоугольной области,\n' \
               '\nИспользуя алгоритм заполнения с перегородкой.\n'

        messagebox.showinfo('', text)

    def __clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self._plane.clean_plane()
        self.text_var_time.set(f" {0: .2f} секунд")
        self._list_points.clear_points()

    def __add_mouse_point(self, event):
        """
        Метод для получения точки с помощью мыши
        """
        x, y = self._plane.get_point_by_click(event)

        if not self.__check_input_point(x, y):
            return

        point = Point(x=x, y=y)

        self._list_points.add_point(point)
        self._plane.add_point(point)
        self._plane.create_point(x, y, color=self._plane.color_fill)

        self._plane.draw_edge()

    def __close(self):
        """
        Метод позволяет замкнуть фигуру
        """
        self._plane.close()

    def __fill(self):
        """
        Метод позволяет заполнить фигуру
        """
        match self._rbt_var.get():
            case "С задержкой":
                self._plane.fill(delay_mode=True)
            case "Без задержки":
                work_time = self._plane.fill()
                print(f"time = {work_time}")
                self.text_var_time.set(f"{work_time: .2f} секунд")
            case _:
                print(f"Не то")
