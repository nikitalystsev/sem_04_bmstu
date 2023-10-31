from plane import *
from checks import *
import tkinter as tk
from tkinter import messagebox
from typing import Union
import copy as cp

from PointClass import *
from dda import Dda
from bresenham import BresenhamInt, BresenhamFloat, BresenhamElimAlias
from vu import Vu
from measurements import CompareTime, CompareStepping

FONT = "Times New Roman"


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()
        self.title("Лабораторная №3, Лысцев Никита ИУ7-43Б")

        root_width = self.winfo_screenwidth()
        root_height = self.winfo_screenheight() - 65
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # определяю используемые алгоритмы построения
        # -----------------------------------------------
        self.dict_algs = {"dda": "Цифровой дифференциальный анализатор",
                          "bi": "Брезенхем с целыми числами",
                          "bf": "Брезенхем с действительными числами",
                          "bea": "Брезенхем с устранением ступенчатости",
                          "vu": "Алгоритм Ву",
                          "lib": "Библиотечный алгоритм"}
        # -----------------------------------------------

        # создал фреймы для всего
        # -----------------------------------------------
        self.frame_plane = self.create_frame_plane()
        self.frame_plane.pack(side=tk.RIGHT)
        self.frame_widgets = self.create_frame_widgets()
        self.frame_widgets.pack()
        # -----------------------------------------------

        self.plane = self.draw_plane()
        self.plane.pack()

        # виджеты для выбора алгоритма построения отрезка
        # -----------------------------------------------
        self.lbl_draw_line_algs = self.draw_label("Алгоритмы построения")
        self.lbl_draw_line_algs.config(font=(FONT, 16, 'bold', "underline"))
        self.lbl_draw_line_algs.grid(row=0, column=0, columnspan=4, sticky='wens')

        self.rbt_algs = tk.StringVar(value=self.dict_algs["dda"])

        self.btn_dda_alg = self.draw_radiobutton(self.dict_algs["dda"])
        self.btn_dda_alg.grid(row=1, column=0, columnspan=4, sticky='wens')

        self.btn_bi_alg = self.draw_radiobutton(self.dict_algs["bi"])
        self.btn_bi_alg.grid(row=2, column=0, columnspan=4, sticky='wens')

        self.btn_bf_alg = self.draw_radiobutton(self.dict_algs["bf"])
        self.btn_bf_alg.grid(row=3, column=0, columnspan=4, sticky='wens')

        self.btn_bea_alg = self.draw_radiobutton(self.dict_algs["bea"])
        self.btn_bea_alg.grid(row=4, column=0, columnspan=4, sticky='wens')

        self.btn_vu_alg = self.draw_radiobutton(self.dict_algs["vu"])
        self.btn_vu_alg.grid(row=5, column=0, columnspan=4, sticky='wens')

        self.btn_lib_alg = self.draw_radiobutton(self.dict_algs["lib"])
        self.btn_lib_alg.grid(row=6, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты выбора цвета фона и линии
        # -----------------------------------------------
        self.lbl_choice_color = self.draw_label("Выбор цвета")
        self.lbl_choice_color.config(font=(FONT, 16, 'bold', "underline"))
        self.lbl_choice_color.grid(row=7, column=0, columnspan=4, sticky='wens')

        self.lbl_choice_color_bg = self.draw_label("Цвет фона: ")
        self.lbl_choice_color_bg.config(font=(FONT, 14, 'bold'))
        self.lbl_choice_color_bg.grid(row=8, column=0, columnspan=2, sticky='wens')

        self.lbl_choice_color_line = self.draw_label("Цвет линии: ")
        self.lbl_choice_color_line.config(font=(FONT, 14, 'bold'))
        self.lbl_choice_color_line.grid(row=9, column=0, columnspan=2, sticky='wens')

        # фреймы выбора цвета
        self.frame_color_bg = tk.Frame(master=self.frame_widgets)
        self.frame_color_bg.grid(row=8, column=2, columnspan=2, sticky='wens')

        self.frame_color_line = tk.Frame(master=self.frame_widgets)
        self.frame_color_line.grid(row=9, column=2, columnspan=2, sticky='wens')
        # -----

        # разные цвета
        self.btn_white_bg = self.draw_choice_color_bg_button("white")
        self.btn_white_bg.pack(side=tk.LEFT)
        self.btn_red_bg = self.draw_choice_color_bg_button("red")
        self.btn_red_bg.pack(side=tk.LEFT)
        self.btn_orange_bg = self.draw_choice_color_bg_button("orange")
        self.btn_orange_bg.pack(side=tk.LEFT)
        self.btn_yellow_bg = self.draw_choice_color_bg_button("yellow")
        self.btn_yellow_bg.pack(side=tk.LEFT)
        self.btn_green_bg = self.draw_choice_color_bg_button("green")
        self.btn_green_bg.pack(side=tk.LEFT)
        self.btn_blue_bg = self.draw_choice_color_bg_button("blue")
        self.btn_blue_bg.pack(side=tk.LEFT)
        self.btn_violet_bg = self.draw_choice_color_bg_button("violet")
        self.btn_violet_bg.pack(side=tk.LEFT)

        self.btn_white_line = self.draw_choice_color_line_button("white")
        self.btn_white_line.pack(side=tk.LEFT)
        self.btn_red_line = self.draw_choice_color_line_button("red")
        self.btn_red_line.pack(side=tk.LEFT)
        self.btn_orange_line = self.draw_choice_color_line_button("orange")
        self.btn_orange_line.pack(side=tk.LEFT)
        self.btn_yellow_line = self.draw_choice_color_line_button("yellow")
        self.btn_yellow_line.pack(side=tk.LEFT)
        self.btn_green_line = self.draw_choice_color_line_button("green")
        self.btn_green_line.pack(side=tk.LEFT)
        self.btn_blue_line = self.draw_choice_color_line_button("blue")
        self.btn_blue_line.pack(side=tk.LEFT)
        self.btn_violet_line = self.draw_choice_color_line_button("violet")
        self.btn_violet_line.pack(side=tk.LEFT)

        self.lbl_curr_color_bg = self.draw_label("Текущий цвет фона: ")
        self.lbl_curr_color_bg.grid(row=10, column=0, columnspan=2, sticky='wens')

        self.curr_color_bg = self.draw_label("")
        self.curr_color_bg.config(bg=self.plane.get_bg_color(), relief=tk.SUNKEN)
        self.curr_color_bg.grid(row=10, column=2, columnspan=2, sticky='wens')

        self.lbl_curr_color_line = self.draw_label("Текущий цвет линии: ")
        self.lbl_curr_color_line.grid(row=11, column=0, columnspan=2, sticky='wens')

        self.curr_color_line = self.draw_label("")
        self.curr_color_line.config(bg=self.plane.get_line_color(), relief=tk.SUNKEN)
        self.curr_color_line.grid(row=11, column=2, columnspan=2, sticky='wens')
        # -----------------------------------------------

        # виджеты построения отрезка
        # -----------------------------------------------
        self.lbl_create_line = self.draw_label("Построение линии")
        self.lbl_create_line.config(font=(FONT, 16, 'bold', "underline"))
        self.lbl_create_line.grid(row=12, column=0, columnspan=4, sticky='wens')

        self.lbl_get_xn = self.draw_label("Xн:")
        self.lbl_get_xn.grid(row=13, column=0, sticky='wens')

        self.entry_get_xn = self.draw_entry()
        self.entry_get_xn.grid(row=13, column=1, sticky='wens')

        self.lbl_get_yn = self.draw_label("Yн:")
        self.lbl_get_yn.grid(row=13, column=2, sticky='wens')

        self.entry_get_yn = self.draw_entry()
        self.entry_get_yn.grid(row=13, column=3, sticky='wens')

        self.lbl_get_xk = self.draw_label("Xк:")
        self.lbl_get_xk.grid(row=14, column=0, sticky='wens')

        self.entry_get_xk = self.draw_entry()
        self.entry_get_xk.grid(row=14, column=1, sticky='wens')

        self.lbl_get_yk = self.draw_label("Yк:")
        self.lbl_get_yk.grid(row=14, column=2, sticky='wens')

        self.entry_get_yk = self.draw_entry()
        self.entry_get_yk.grid(row=14, column=3, sticky='wens')

        self.btn_create_line = self.draw_button("Построить линию")
        self.btn_create_line.config(command=self.draw_line)
        self.btn_create_line.grid(row=15, column=0, columnspan=4, sticky='wens')

        self.lbl_get_angle = self.draw_label("Угол поворота:")
        self.lbl_get_angle.grid(row=16, column=0, columnspan=2, sticky='wens')

        self.entry_get_angle = self.draw_entry()
        self.entry_get_angle.grid(row=16, column=2, columnspan=2, sticky='wens')

        self.btn_create_range_line = self.draw_button("Построить спектр линий")
        self.btn_create_range_line.config(command=self.draw_spectrum)
        self.btn_create_range_line.grid(row=17, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты проведения измерений
        # -----------------------------------------------
        self.lbl_cmp_algs = self.draw_label("Сравнение алгоритмов построения")
        self.lbl_cmp_algs.config(font=(FONT, 16, 'bold', "underline"))
        self.lbl_cmp_algs.grid(row=18, column=0, columnspan=4, sticky='wens')

        self.lbl_get_len_line = self.draw_label("Длина линии: ")
        self.lbl_get_len_line.grid(row=19, column=0, columnspan=2, sticky='wens')

        self.entry_get_len_line = self.draw_entry()
        self.entry_get_len_line.grid(row=19, column=2, columnspan=2, sticky='wens')

        self.btn_cmp_time = self.draw_button("Сравнить время")
        self.btn_cmp_time.config(command=self.cmp_time_draw_spectrum)
        self.btn_cmp_time.grid(row=20, column=0, columnspan=4, sticky='wens')
        self.compare_time = CompareTime()

        self.btn_cmp_stepping = self.draw_button("Сравнить ступенчатость")
        self.btn_cmp_stepping.config(command=self.cmp_stepping)
        self.btn_cmp_stepping.grid(row=21, column=0, columnspan=4, sticky='wens')
        self.compare_stepping = CompareStepping()

        self.btn_clean_plane = self.draw_button("Очистить экран")
        self.btn_clean_plane.config(command=self.clean_plane)
        self.btn_clean_plane.grid(row=22, column=0, columnspan=4, sticky='wens')

        self.btn_info = self.draw_button("Справка")
        self.btn_info.config(command=self.print_info)
        self.btn_info.grid(row=23, column=0, columnspan=4, sticky='wens')

    def create_frame_plane(self) -> tk.Frame:
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

    def create_frame_widgets(self) -> tk.Frame:
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

    def draw_plane(self) -> PlaneCanvas:
        """
        Метод размещает холст (canvas) для плоскости (plane) на главном окне
        :return: холст
        """
        plane_width = self.frame_plane.winfo_screenwidth() - 400
        plane_height = self.frame_plane.winfo_screenheight() - 70

        plane = PlaneCanvas(
            color_line="red",
            master=self.frame_plane,
            width=plane_width,
            height=plane_height,
            bg=WHITE
        )

        return plane

    def draw_label(self, text: str) -> tk.Label:
        """
        Метод создает виджет текста (label)
        :param text: строка текста
        :return: виджет текста
        """
        label = tk.Label(
            self.frame_widgets,
            text=text,
            font=(FONT, 14, 'bold'),
        )

        return label

    def draw_entry(self) -> tk.Entry:
        """
        Метод создает виджет однострочного поля ввода (entry)
        :return: виджет однострочного поля ввода
        """
        entry = tk.Entry(
            self.frame_widgets,
            width=15,
            relief=tk.SUNKEN,
            borderwidth=5,
            justify=tk.CENTER,
            font=(FONT, 14)
        )

        return entry

    def draw_button(self, text: str) -> tk.Button:
        """
        Метод создает виджет кнопки (button)
        :param text:  текст
        :return: виджет кнопки
        """
        button = tk.Button(
            self.frame_widgets,
            text=text,
            font=(FONT, 12),
            relief=tk.RAISED
        )

        button.config(bg=WHITE)

        return button

    def draw_choice_color_bg_button(self, color: str) -> tk.Button:
        """
        Метод создает кнопку выбора цвета
        """
        btn = tk.Button(self.frame_color_bg, bg=color, activebackground=color)
        btn.config(command=lambda: self.set_bg_color(color))

        return btn

    def draw_choice_color_line_button(self, color: str) -> tk.Button:
        """
        Метод создает кнопку выбора цвета
        """
        btn = tk.Button(self.frame_color_line, bg=color, activebackground=color)
        btn.config(command=lambda: self.set_line_color(color))

        return btn

    def set_bg_color(self, color: str):
        """
        Метод позволяет изменить текущий цвет фона холста
        """
        self.plane.set_bg_color(color)
        self.curr_color_bg.config(bg=self.plane.get_bg_color())

    def set_line_color(self, color: str):
        """
        Метод позволяет изменить текущий цвет фона холста
        """
        self.plane.set_line_color(color)
        self.curr_color_line.config(bg=self.plane.get_line_color())

    def draw_radiobutton(self, text: str) -> tk.Radiobutton:
        """
        Метод создает переключатель 2-х множеств треугольника для ввода
        :param text: значение переключателя
        :return: переключатель 2-х множеств треугольника для ввода
        """
        rbt = tk.Radiobutton(
            self.frame_widgets,
            text=text,
            value=text,
            variable=self.rbt_algs,
            font=(FONT, 14, 'bold', 'italic'),
            anchor=tk.W
        )

        return rbt

    def draw_line(self):
        """
        Метод позволяет отобразить линию в зависимости от алгоритма
        """
        point1, point2 = self.get_points()

        if not self.check_points_line(point1, point2):
            return

        match self.rbt_algs.get():
            case "Цифровой дифференциальный анализатор":
                self.draw_line_by_alg(point1, point2, Dda)
            case "Брезенхем с целыми числами":
                self.draw_line_by_alg(point1, point2, BresenhamInt)
            case "Брезенхем с действительными числами":
                self.draw_line_by_alg(point1, point2, BresenhamFloat)
            case "Брезенхем с устранением ступенчатости":
                self.draw_line_by_alg(point1, point2, BresenhamElimAlias)
            case "Алгоритм Ву":
                self.draw_line_by_alg(point1, point2, Vu)
            case "Библиотечный алгоритм":
                self.plane.create_line(point1.x, point1.y, point2.x, point2.y, fill=self.plane.color_line)

    def draw_line_by_alg(self, point1: Point, point2: Point,
                         alg: type[Union[Dda, BresenhamInt, BresenhamFloat, BresenhamElimAlias, Vu]]) -> None:
        """
        Метод строит линию по алгоритму
        """
        build_alg = alg(point1, point2)

        self.plane.draw_line(build_alg)

    def draw_spectrum(self) -> None:
        """
        Метод позволяет построить спектр линий определенным алгоритмом
        """
        point1, point2 = self.get_points()

        if not self.check_points_line(point1, point2):
            return

        angle = self.get_angle()

        if not self.check_angle(angle):
            return

        match self.rbt_algs.get():
            case "Цифровой дифференциальный анализатор":
                self.draw_spectrum_by_alg(point1, point2, angle, Dda)
            case "Брезенхем с целыми числами":
                self.draw_spectrum_by_alg(point1, point2, angle, BresenhamInt)
            case "Брезенхем с действительными числами":
                self.draw_spectrum_by_alg(point1, point2, angle, BresenhamFloat)
            case "Брезенхем с устранением ступенчатости":
                self.draw_spectrum_by_alg(point1, point2, angle, BresenhamElimAlias)
            case "Алгоритм Ву":
                self.draw_spectrum_by_alg(point1, point2, angle, Vu)
            case "Библиотечный алгоритм":
                self.draw_spectrum_by_lib_func(point1, point2, angle)

    def draw_spectrum_by_alg(self, point1: Point, point2: Point, angle,
                             alg: type[Union[Dda, BresenhamInt, BresenhamFloat, BresenhamElimAlias, Vu]]) -> float:
        """
        Метод строит спектр по алгоритму
        """
        steps = int(360 / angle)
        # время построения изначально 0
        build_time = 0

        for _ in range(steps):
            copy_point1 = cp.deepcopy(point1)
            copy_point2 = cp.deepcopy(point2)

            # строим линию
            build_alg = alg(copy_point1, copy_point2)
            build_time += self.plane.draw_line(build_alg)

            # поворачиваем
            point1, point2 = self.plane.rotate_line(point1, point2, angle)

        return build_time / steps

    def draw_spectrum_by_lib_func(self, point1: Point, point2: Point, angle):
        """
        Метод позволяет построить спектр библиотечной функцией
        """
        steps = int(360 / angle)

        build_time = 0

        for _ in range(steps):
            # строим линию
            beg = CompareTime.time_now()
            self.plane.create_line(point1.x, point1.y, point2.x, point2.y, fill=self.plane.color_line)
            end = CompareTime.time_now()

            build_time += end - beg

            # поворачиваем
            point1, point2 = self.plane.rotate_line(point1, point2, angle)

        return build_time / steps

    def cmp_time_draw_spectrum(self):
        """
        Метод позволяет получить время построения линии каждым алгоритмом
        """
        # очищаем если уже получали время
        self.compare_time.clean_times()

        len_line = self.get_len_line()

        if not self.check_len_line(len_line):
            return

        self.compare_time.len_line = len_line

        point1 = Point(750, 500, self.plane.get_line_color())
        point2 = Point(750 + len_line, 500, self.plane.get_line_color())

        angle = 5

        self.compare_time.times.append(self.draw_spectrum_by_alg(point1, point2, angle, Dda))
        self.compare_time.times.append(self.draw_spectrum_by_alg(point1, point2, angle, BresenhamInt))
        self.compare_time.times.append(self.draw_spectrum_by_alg(point1, point2, angle, BresenhamFloat))
        self.compare_time.times.append(self.draw_spectrum_by_alg(point1, point2, angle, BresenhamElimAlias))
        self.compare_time.times.append(self.draw_spectrum_by_alg(point1, point2, angle, Vu))
        self.compare_time.times.append(self.draw_spectrum_by_lib_func(point1, point2, angle))

        self.plane.clean_plane()

        self.compare_time.print_compare()

    def cmp_stepping(self):
        """
        Метод собирает данные для количества сравнения количества ступенек
        """
        # очищаем если уже сравнивали ступенчатость
        self.compare_stepping.clean_steps()

        len_line = self.get_len_line()

        if not self.check_len_line(len_line):
            return

        self.compare_stepping.len_line = len_line

        angle = 0
        step = 2

        point1 = Point(0, 0, self.plane.color_line)
        point2 = Point(0, 0 + len_line, self.plane.color_line)

        for _ in range(90 // step):
            # делаем копии (Ву меняет конкретно и портит все)
            copy_point1 = cp.deepcopy(point1)
            copy_point2 = cp.deepcopy(point2)

            self.compare_stepping.dda_steps.append(self.get_steps_by_alg(point1, point2, Dda))
            self.compare_stepping.bres_int_steps.append(self.get_steps_by_alg(point1, point2, BresenhamInt))
            self.compare_stepping.bres_float_steps.append(self.get_steps_by_alg(point1, point2, BresenhamFloat))
            self.compare_stepping.bres_elim_alias.append(self.get_steps_by_alg(point1, point2, BresenhamElimAlias))
            self.compare_stepping.vu_steps.append(self.get_steps_by_alg(copy_point1, copy_point2, Vu))

            point1, point2 = self.plane.rotate_line(point1, point2, step)
            self.compare_stepping.angles.append(angle)

            angle += step

        self.compare_stepping.print_compare()

    def get_steps_by_alg(self, point1: Point, point2: Point,
                         alg: type[Union[Dda, BresenhamInt, BresenhamFloat, BresenhamElimAlias, Vu]]):
        """
        Метод позволяет получить колиество ступенек для построения
        линии заданной длины заданным алгоритмом
        """
        ex_alg = alg(point1, point2, stepmode=True)

        count_steps = ex_alg.get_points_for_line(self.plane.get_line_color(), self.plane.get_bg_color())

        return count_steps

    def get_points(self) -> (Point, Point):
        """
        Метод позволяет получить начальную и конечную точку линии
        """
        x1, y1 = self.get_data(self.entry_get_xn, self.entry_get_yn)
        x2, y2 = self.get_data(self.entry_get_xk, self.entry_get_yk)

        x1 = int(x1) if self.is_int(x1) else float(x1) if self.is_float(x1) else x1
        y1 = int(y1) if self.is_int(y1) else float(y1) if self.is_float(y1) else y1
        x2 = int(x2) if self.is_int(x2) else float(x2) if self.is_float(x2) else x2
        y2 = int(y2) if self.is_int(y2) else float(y2) if self.is_float(y2) else y2

        # потоп проверки точек накинуть еще
        return Point(x1, y1, self.plane.get_line_color()), Point(x2, y2, self.plane.get_line_color())

    def get_angle(self):
        """
        Метод позволяет получить угол с поля ввода
        """
        angle = self.entry_get_angle.get()

        angle = int(angle) if self.is_int(angle) else float(angle) if self.is_float(angle) else angle

        return angle

    def get_len_line(self):
        """
        Метод позволяет получить угол с поля ввода
        """
        len_line = self.entry_get_len_line.get()

        len_line = int(len_line) if self.is_int(len_line) else float(len_line) if self.is_float(len_line) else len_line

        return len_line

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self.plane.clean_plane()

    @staticmethod
    def check_points_line(point1: Point, point2: Point) -> bool:
        """
        Метод проверяет точки после возможных
        приведений их к числовому значению
        """
        if isinstance(point1.x, str) or isinstance(point1.y, str) or \
                isinstance(point2.x, str) or isinstance(point2.y, str):
            text = "Получены некорректные данные для точек отрезка!\n" \
                   "Попробуйте снова!"
            messagebox.showwarning("", text)
            return False

        return True

    @staticmethod
    def check_angle(angle) -> bool:
        """
        Метод проверяет точки после возможных
        приведений их к числовому значению
        """
        if isinstance(angle, str):
            text = "Получены некорректные данные для угла поворота!\n" \
                   "Попробуйте снова!"
            messagebox.showwarning("", text)
            return False

        return True

    @staticmethod
    def check_len_line(len_line) -> bool:
        """
        Метод проверяет точки после возможных
        приведений их к числовому значению
        """
        if isinstance(len_line, str):
            text = "Получены некорректные данные для длины линии!\n" \
                   "Попробуйте снова!"
            messagebox.showwarning("", text)
            return False

        return True

    @staticmethod
    def print_info() -> None:
        """
        Метод выводит информацию о программе
        """
        text = 'С помощью данной программы можно построить отрезки 6 способами:\n' \
               '1) методом цифрового дифференциального анализатора;\n' \
               '2) методом Брезенхема с целыми коэффициентами;\n' \
               '3) методом Брезенхема с действительными коэффициентами;\n' \
               '4) методом Брезенхема с устранением ступенчатости;\n' \
               '5) методом Ву;\n' \
               '6) библиотечной функцией.\n' \
               '\nДля построения отрезка необходимо задать его начало\n' \
               'и конец и выбрать метод построения из списка предложенных.\n' \
               '\nДля построения спектра (пучка отрезков)\n' \
               'необходимо задать начало и конец,\n' \
               'выбрать метод для построения,\n' \
               'а также угол поворота отрезка.\n' \
               '\nДля анализа ступенчатости достаточно нажать на кнопку "Сравнение ступенчатости".\n' \
               'Анализ ступенчатости и времени исполнения приводится\n' \
               'в виде графиков pyplot.\n' \
               'Введите длину отрезка, если хотите сделать анализ программы\n' \
               'при построении отрезков определенной длины.'

        messagebox.showinfo('', text)

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
