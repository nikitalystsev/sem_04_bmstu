from tkinter import messagebox

from plane import *
from checks import *
from canonical_equ import CanonicalCircle, CanonicalEllipse
from parametric_equ import ParametricCircle, ParametricEllipse
from bresenham import BresenhamCircle, BresenhamEllipse
from mid_point import MidPointAlgCircle, MidPointAlgEllipse
from PointClass import Point
from measurements import CompareTimeCircle, CompareTimeEllipse

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
        self._dict_algs = {"cane": "Каноническое уравнение",
                           "pare": "Параметрическое уравнение",
                           "bres": "Алгоритм Брезенхема",
                           "midp": "Алгоритм средней точки",
                           "lib": "Библиотечный алгоритм"}
        # -----------------------------------------------

        # создал фреймы для всего
        # -----------------------------------------------
        self._frame_plane = self.__create_frame_plane()
        self._frame_plane.pack(side=tk.RIGHT)
        self._frame_widgets = self.__create_frame_widgets()
        self._frame_widgets.pack()
        # -----------------------------------------------

        self._plane = self.__create_plane()
        self._plane.pack()

        # виджеты для выбора алгоритма построения отрезка
        # -----------------------------------------------
        self._lbl_draw_line_algs = self.__create_label("Алгоритмы построения")
        self._lbl_draw_line_algs.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_draw_line_algs.grid(row=0, column=0, columnspan=4, sticky='wens')

        self._rbt_algs = tk.StringVar(value=self._dict_algs["cane"])

        self._btn_cane_alg = self.__create_radiobutton(self._dict_algs["cane"])
        self._btn_cane_alg.grid(row=1, column=0, columnspan=4, sticky='wens')

        self._btn_pare_alg = self.__create_radiobutton(self._dict_algs["pare"])
        self._btn_pare_alg.grid(row=2, column=0, columnspan=4, sticky='wens')

        self._btn_bres_alg = self.__create_radiobutton(self._dict_algs["bres"])
        self._btn_bres_alg.grid(row=3, column=0, columnspan=4, sticky='wens')

        self._btn_midp_alg = self.__create_radiobutton(self._dict_algs["midp"])
        self._btn_midp_alg.grid(row=4, column=0, columnspan=4, sticky='wens')

        self._btn_lib_alg = self.__create_radiobutton(self._dict_algs["lib"])
        self._btn_lib_alg.grid(row=5, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты выбора цвета фона и линии
        # -----------------------------------------------
        self._lbl_choice_color = self.__create_label("Выбор цвета")
        self._lbl_choice_color.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_choice_color.grid(row=7, column=0, columnspan=4, sticky='wens')

        self._lbl_choice_color_bg = self.__create_label("Цвет фона: ")
        self._lbl_choice_color_bg.config(font=(FONT, 14, 'bold'))
        self._lbl_choice_color_bg.grid(row=8, column=0, columnspan=2, sticky='wens')

        self._lbl_choice_color_line = self.__create_label("Цвет линии: ")
        self._lbl_choice_color_line.config(font=(FONT, 14, 'bold'))
        self._lbl_choice_color_line.grid(row=9, column=0, columnspan=2, sticky='wens')

        # фреймы выбора цвета
        self._frame_color_bg = tk.Frame(master=self._frame_widgets)
        self._frame_color_bg.grid(row=8, column=2, columnspan=2, sticky='wens')

        self._frame_color_line = tk.Frame(master=self._frame_widgets)
        self._frame_color_line.grid(row=9, column=2, columnspan=2, sticky='wens')
        # -----

        # разные цвета
        self._btn_white_bg = self.__create_choice_color_bg_button("white")
        self._btn_white_bg.pack(side=tk.LEFT)
        self._btn_red_bg = self.__create_choice_color_bg_button("red")
        self._btn_red_bg.pack(side=tk.LEFT)
        self._btn_orange_bg = self.__create_choice_color_bg_button("orange")
        self._btn_orange_bg.pack(side=tk.LEFT)
        self._btn_yellow_bg = self.__create_choice_color_bg_button("yellow")
        self._btn_yellow_bg.pack(side=tk.LEFT)
        self._btn_green_bg = self.__create_choice_color_bg_button("green")
        self._btn_green_bg.pack(side=tk.LEFT)
        self._btn_blue_bg = self.__create_choice_color_bg_button("blue")
        self._btn_blue_bg.pack(side=tk.LEFT)
        self._btn_violet_bg = self.__create_choice_color_bg_button("violet")
        self._btn_violet_bg.pack(side=tk.LEFT)

        self._btn_white_line = self.__create_choice_color_figure_button("white")
        self._btn_white_line.pack(side=tk.LEFT)
        self._btn_red_line = self.__create_choice_color_figure_button("red")
        self._btn_red_line.pack(side=tk.LEFT)
        self._btn_orange_line = self.__create_choice_color_figure_button("orange")
        self._btn_orange_line.pack(side=tk.LEFT)
        self._btn_yellow_line = self.__create_choice_color_figure_button("yellow")
        self._btn_yellow_line.pack(side=tk.LEFT)
        self._btn_green_line = self.__create_choice_color_figure_button("green")
        self._btn_green_line.pack(side=tk.LEFT)
        self._btn_blue_line = self.__create_choice_color_figure_button("blue")
        self._btn_blue_line.pack(side=tk.LEFT)
        self._btn_violet_line = self.__create_choice_color_figure_button("violet")
        self._btn_violet_line.pack(side=tk.LEFT)

        self._lbl_curr_color_bg = self.__create_label("Текущий цвет фона: ")
        self._lbl_curr_color_bg.grid(row=10, column=0, columnspan=2, sticky='wens')

        self._curr_color_bg = self.__create_label("")
        self._curr_color_bg.config(bg=self._plane.color_bg, relief=tk.SUNKEN)
        self._curr_color_bg.grid(row=10, column=2, columnspan=2, sticky='wens')

        self._lbl_curr_color_line = self.__create_label("Текущий цвет линии: ")
        self._lbl_curr_color_line.grid(row=11, column=0, columnspan=2, sticky='wens')

        self._curr_color_line = self.__create_label("")
        self._curr_color_line.config(bg=self._plane.color_figure, relief=tk.SUNKEN)
        self._curr_color_line.grid(row=11, column=2, columnspan=2, sticky='wens')
        # -----------------------------------------------

        # виджеты построения окружности
        # -----------------------------------------------
        self._lbl_param_circle = self.__create_label("Параметры окружности")
        self._lbl_param_circle.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_param_circle.grid(row=12, column=0, columnspan=4, sticky='wens')

        self._lbl_get_xc = self.__create_label("x_c: ")
        self._lbl_get_xc.grid(row=13, column=0, sticky='wens')

        self._entry_get_xc = self.__create_entry()
        self._entry_get_xc.grid(row=13, column=1, sticky='wens')

        self._lbl_get_yc = self.__create_label("y_c: ")
        self._lbl_get_yc.grid(row=13, column=2, sticky='wens')

        self._entry_get_yc = self.__create_entry()
        self._entry_get_yc.grid(row=13, column=3, sticky='wens')

        self._lbl_get_r = self.__create_label("R: ")
        self._lbl_get_r.grid(row=14, column=0, columnspan=2, sticky='wens')

        self._entry_get_r = self.__create_entry()
        self._entry_get_r.grid(row=14, column=2, columnspan=2, sticky='wens')

        self._btn_draw_circle = self.__create_button("Построить окружность")
        self._btn_draw_circle.config(command=self.__draw_circle)
        self._btn_draw_circle.grid(row=15, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты построения эллипса
        # -----------------------------------------------
        self._lbl_param_ellipse = self.__create_label("Параметры эллипса")
        self._lbl_param_ellipse.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_param_ellipse.grid(row=16, column=0, columnspan=4, sticky='wens')

        self._lbl_get_xc_el = self.__create_label("x_c: ")
        self._lbl_get_xc_el.grid(row=17, column=0, sticky='wens')

        self._entry_get_xc_el = self.__create_entry()
        self._entry_get_xc_el.grid(row=17, column=1, sticky='wens')

        self._lbl_get_yc_el = self.__create_label("y_c: ")
        self._lbl_get_yc_el.grid(row=17, column=2, sticky='wens')

        self._entry_get_yc_el = self.__create_entry()
        self._entry_get_yc_el.grid(row=17, column=3, sticky='wens')

        self._lbl_get_a = self.__create_label("a: ")
        self._lbl_get_a.grid(row=18, column=0, sticky='wens')

        self._entry_get_a = self.__create_entry()
        self._entry_get_a.grid(row=18, column=1, sticky='wens')

        self._lbl_get_b = self.__create_label("b: ")
        self._lbl_get_b.grid(row=18, column=2, sticky='wens')

        self._entry_get_b = self.__create_entry()
        self._entry_get_b.grid(row=18, column=3, sticky='wens')

        self._btn_draw_ellipse = self.__create_button("Построить эллипс")
        self._btn_draw_ellipse.config(command=self.__draw_ellipse)
        self._btn_draw_ellipse.grid(row=19, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты построения спектра окружностей
        # -----------------------------------------------
        self._lbl_param_spect_circle = self.__create_label("Параметры спектра окружностей")
        self._lbl_param_spect_circle.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_param_spect_circle.grid(row=20, column=0, columnspan=4, sticky='wens')

        self._lbl_get_rbeg = self.__create_label("Rн: ")
        self._lbl_get_rbeg.grid(row=21, column=0, sticky='wens')

        self._entry_get_rbeg = self.__create_entry()
        self._entry_get_rbeg.grid(row=21, column=1, sticky='wens')

        # self._lbl_get_re = self.__create_label("Rк: ")
        # self._lbl_get_re.grid(row=21, column=2, sticky='wens')
        #
        # self._entry_get_re = self.__create_entry()
        # self._entry_get_re.grid(row=21, column=3, sticky='wens')

        self._lbl_get_step = self.__create_label("Шаг: ")
        self._lbl_get_step.grid(row=22, column=0, sticky='wens')

        self._entry_get_step = self.__create_entry()
        self._entry_get_step.grid(row=22, column=1, sticky='wens')

        self._lbl_get_N = self.__create_label("N: ")
        self._lbl_get_N.grid(row=22, column=2, sticky='wens')

        self._entry_get_N = self.__create_entry()
        self._entry_get_N.grid(row=22, column=3, sticky='wens')

        self._btn_draw_spect_circle = self.__create_button("Построить спектр окружностей")
        self._btn_draw_spect_circle.config(command=self.__draw_spectrum_circle)
        self._btn_draw_spect_circle.grid(row=23, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты построения спектра эллипсов
        # -----------------------------------------------
        self._lbl_param_spect_ellipse = self.__create_label("Параметры спектра эллипсов")
        self._lbl_param_spect_ellipse.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_param_spect_ellipse.grid(row=24, column=0, columnspan=4, sticky='wens')

        self._lbl_get_spect_a = self.__create_label("a: ")
        self._lbl_get_spect_a.grid(row=25, column=0, sticky='wens')

        self._entry_get_spect_a = self.__create_entry()
        self._entry_get_spect_a.grid(row=25, column=1, sticky='wens')

        self._lbl_get_spect_b = self.__create_label("b: ")
        self._lbl_get_spect_b.grid(row=25, column=2, sticky='wens')

        self._entry_get_spect_b = self.__create_entry()
        self._entry_get_spect_b.grid(row=25, column=3, sticky='wens')

        self._lbl_get_step_el = self.__create_label("Шаг: ")
        self._lbl_get_step_el.grid(row=26, column=0, sticky='wens')

        self._entry_get_step_el = self.__create_entry()
        self._entry_get_step_el.grid(row=26, column=1, sticky='wens')

        self._lbl_get_N_el = self.__create_label("N: ")
        self._lbl_get_N_el.grid(row=26, column=2, sticky='wens')

        self._entry_get_N_el = self.__create_entry()
        self._entry_get_N_el.grid(row=26, column=3, sticky='wens')

        self._btn_draw_spect_ellipse = self.__create_button("Построить спектр эллипсов")
        self._btn_draw_spect_ellipse.config(command=self.__draw_spectrum_ellipse)
        self._btn_draw_spect_ellipse.grid(row=27, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        self._lbl_cmp_algs = self.__create_label("Сравнение алгоритмов построения")
        self._lbl_cmp_algs.config(font=(FONT, 16, 'bold', "underline"))
        self._lbl_cmp_algs.grid(row=28, column=0, columnspan=4, sticky='wens')

        self._btn_cmp_time_circle = self.__create_button("Сравнить алгоритмы построения окружности")
        self._btn_cmp_time_circle.config(command=self.__cmp_time_circle)
        self._btn_cmp_time_circle.grid(row=29, column=0, columnspan=4, sticky='wens')
        self.cmp_time_circle = CompareTimeCircle()

        self._btn_cmp_time_ellipse = self.__create_button("Сравнить алгоритмы построения эллипса")
        self._btn_cmp_time_ellipse.config(command=self.__cmp_time_ellipse)
        self._btn_cmp_time_ellipse.grid(row=30, column=0, columnspan=4, sticky='wens')
        self.__cmp_time_ellipse = CompareTimeEllipse()

        self._btn_clean_plane = self.__create_button("Очистить экран")
        self._btn_clean_plane.config(command=self.clean_plane)
        self._btn_clean_plane.grid(row=31, column=0, columnspan=4, sticky='wens')

        self._btn_info = self.__create_button("Справка")
        self._btn_info.config(command=self.print_info)
        self._btn_info.grid(row=32, column=0, columnspan=4, sticky='wens')

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
            color_figure="red",
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

        button.config(bg=WHITE)

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
            variable=self._rbt_algs,
            font=(FONT, 14, 'bold', 'italic'),
            anchor=tk.W
        )

        return rbt

    def __create_choice_color_bg_button(self, color: str) -> tk.Button:
        """
        Метод создает кнопку выбора цвета
        """
        btn = tk.Button(self._frame_color_bg, bg=color, activebackground=color)
        btn.config(command=lambda: self.set_color_bg(color))

        return btn

    def __create_choice_color_figure_button(self, color: str) -> tk.Button:
        """
        Метод создает кнопку выбора цвета
        """
        btn = tk.Button(self._frame_color_line, bg=color, activebackground=color)
        btn.config(command=lambda: self.set_color_figure(color))

        return btn

    def set_color_bg(self, color: str):
        """
        Метод позволяет изменить текущий цвет фона холста
        """
        self._plane.color_bg = color
        self._curr_color_bg.config(bg=self._plane.color_bg)

    def set_color_figure(self, color: str):
        """
        Метод позволяет изменить текущий цвет фона холста
        """
        self._plane.color_figure = color
        self._curr_color_line.config(bg=self._plane.color_figure)

    def clean_plane(self) -> None:
        """
        Метод позволяет очистить содержимое плоскости
        """
        self._plane.clean_plane()

    def __get_point_center(self, entry_x: tk.Entry, entry_y: tk.Entry) -> Point:
        """
        Метод позволяет получить центр окружности или эллипса
        """
        x_c, y_c = self.get_data(entry_x, entry_y)

        x_c = int(x_c) if self.is_int(x_c) else float(x_c) if self.is_float(x_c) else x_c
        y_c = int(y_c) if self.is_int(y_c) else float(y_c) if self.is_float(y_c) else y_c

        # потоп проверки точек накинуть еще
        return Point(x=x_c, y=y_c, color=self._plane.color_bg)

    @staticmethod
    def __check_points_center(point_center: Point) -> bool:
        """
        Метод проверяет точки после возможных
        приведений их к числовому значению
        """
        if isinstance(point_center.x, str) or isinstance(point_center.y, str):
            text = "Получены некорректные данные для центра фигуры!\n" \
                   "Попробуйте снова!"
            messagebox.showwarning("", text)
            return False

        return True

    def __get_radius(self, entry_r: tk.Entry) -> int | float:
        """
        Метод получения радиуса окружности
        """
        r = entry_r.get()

        r = int(r) if self.is_int(r) else float(r) if self.is_float(r) else r

        return r

    @staticmethod
    def __check_radius(r: int | float) -> bool:
        """
        Метод проверяет точки после возможных
        приведений их к числовому значению
        """
        if isinstance(r, str):
            text = "Получены некорректные данные для радиуса!\n" \
                   "Попробуйте снова!"
            messagebox.showwarning("", text)
            return False

        return True

    def __draw_circle_by_alg(self, point_center: Point, r: int | float,
                             alg: type[
                                 Union[CanonicalCircle, ParametricCircle, BresenhamCircle, MidPointAlgCircle]]) -> None:
        """
        Метод строит окружность по алгоритму
        """
        build_alg = alg(point_center, r)

        self._plane.draw_circle(build_alg)

    def __draw_circle(self):
        """
        Метод позволяет отобразить окружность в зависимости от алгоритма
        """

        point_center = self.__get_point_center(self._entry_get_xc, self._entry_get_yc)
        r = self.__get_radius(self._entry_get_r)

        if not self.__check_points_center(point_center) or not self.__check_radius(r):
            return

        match self._rbt_algs.get():
            case "Каноническое уравнение":
                self.__draw_circle_by_alg(point_center, r, CanonicalCircle)
            case "Параметрическое уравнение":
                self.__draw_circle_by_alg(point_center, r, ParametricCircle)
            case "Алгоритм Брезенхема":
                self.__draw_circle_by_alg(point_center, r, BresenhamCircle)
            case "Алгоритм средней точки":
                self.__draw_circle_by_alg(point_center, r, MidPointAlgCircle)
            case "Библиотечный алгоритм":
                self._plane.create_oval(point_center.x - r, point_center.y - r,
                                        point_center.x + r, point_center.y + r,
                                        outline=self._plane.color_figure)

    def __get_h(self, entry_h: tk.Entry) -> int | float:
        """
        Метод позволяет получить шаг, с которым будет отображаться спектр окружностей
        """
        h = entry_h.get()

        h = int(h) if self.is_int(h) else float(h) if self.is_float(h) else h

        return h

    def __get_n(self, entry_n: tk.Entry) -> int | float:
        """
        Метод позволяет получить шаг, с которым будет отображаться спектр окружностей
        """
        n = entry_n.get()

        n = int(n) if self.is_int(n) else float(n) if self.is_float(n) else n

        return n

    def __draw_spectrum_circle_by_lib(
            self,
            point_center: Point,
            r: int | float,
            h: int,
            n: int,
    ) -> list[tuple[int | float, int | float]]:
        """
        Метод строит спектр по алгоритму
        """
        list_time = list()

        for _ in range(n):
            # строим линию
            beg = CompareTimeCircle.time_now()
            self._plane.create_oval(point_center.x - r, point_center.y - r,
                                    point_center.x + r, point_center.y + r,
                                    outline=self._plane.color_figure)
            end = CompareTimeCircle.time_now() - beg
            list_time.append((end, r))

            r += h

        return list_time

    def __draw_spectrum_circle_by_alg(
            self,
            point_center: Point,
            r: int | float,
            h: int,
            n: int,
            alg: type[
                CanonicalCircle |
                ParametricCircle |
                BresenhamCircle |
                MidPointAlgCircle
                ]
    ) -> list[tuple[int | float, int | float]]:
        """
        Метод строит спектр по алгоритму
        """
        list_time = list()

        for _ in range(n):
            # строим линию
            build_alg = alg(point_center, r)
            build_time = self._plane.draw_circle(build_alg)

            list_time.append((build_time, r))

            r += h

        return list_time

    def __draw_spectrum_circle(self):
        """
        Метод позволяет отобразить спектр окружностей
        """
        point_center = self.__get_point_center(self._entry_get_xc, self._entry_get_yc)
        r_begin = self.__get_radius(self._entry_get_rbeg)
        h = self.__get_h(self._entry_get_step)
        n = self.__get_n(self._entry_get_N)

        if isinstance(r_begin, str) or isinstance(h, str) or isinstance(n, str) \
                or not self.__check_points_center(point_center):
            return

        match self._rbt_algs.get():
            case "Каноническое уравнение":
                self.__draw_spectrum_circle_by_alg(point_center, r_begin, h, n, CanonicalCircle)
            case "Параметрическое уравнение":
                self.__draw_spectrum_circle_by_alg(point_center, r_begin, h, n, ParametricCircle)
            case "Алгоритм Брезенхема":
                self.__draw_spectrum_circle_by_alg(point_center, r_begin, h, n, BresenhamCircle)
            case "Алгоритм средней точки":
                self.__draw_spectrum_circle_by_alg(point_center, r_begin, h, n, MidPointAlgCircle)
            case "Библиотечный алгоритм":
                self.__draw_spectrum_circle_by_lib(point_center, r_begin, h, n)

    def __get_a_b(self, entry_a: tk.Entry, entry_b: tk.Entry) -> (int | float, int | float):
        """
        Метод позволяет получить значения полуосей эллипса
        """
        a, b = self.get_data(entry_a, entry_b)

        a = int(a) if self.is_int(a) else float(a) if self.is_float(a) else a
        b = int(b) if self.is_int(b) else float(b) if self.is_float(b) else b

        return a, b

    @staticmethod
    def __check_a_b(a: int | float, b: int | float) -> bool:
        """
        Метод проверяет полуоси после возможных
        приведений их к числовому значению
        """
        if isinstance(a, str) or isinstance(b, str):
            text = "Получены некорректные данные для центра окружности!\n" \
                   "Попробуйте снова!"
            messagebox.showwarning("", text)
            return False

        return True

    def __draw_ellipse_by_alg(self, point_center: Point, a: int | float, b: int | float,
                              alg: type[Union[
                                  CanonicalEllipse, ParametricEllipse, BresenhamEllipse, MidPointAlgEllipse]]) -> None:
        """
        Метод строит окружность по алгоритму
        """
        build_alg = alg(point_center, a, b)

        self._plane.draw_ellipse(build_alg)

    def __draw_ellipse(self):
        """
        Метод позволяет отобразить эллипс в зависимости от алгоритма
        """

        point_center = self.__get_point_center(self._entry_get_xc_el, self._entry_get_yc_el)
        a, b = self.__get_a_b(self._entry_get_a, self._entry_get_b)

        if not self.__check_points_center(point_center) or not self.__check_a_b(a, b):
            return

        match self._rbt_algs.get():
            case "Каноническое уравнение":
                self.__draw_ellipse_by_alg(point_center, a, b, CanonicalEllipse)
            case "Параметрическое уравнение":
                self.__draw_ellipse_by_alg(point_center, a, b, ParametricEllipse)
            case "Алгоритм Брезенхема":
                self.__draw_ellipse_by_alg(point_center, a, b, BresenhamEllipse)
            case "Алгоритм средней точки":
                self.__draw_ellipse_by_alg(point_center, a, b, MidPointAlgEllipse)
            case "Библиотечный алгоритм":
                self._plane.create_oval(point_center.x - a, point_center.y - b,
                                        point_center.x + a, point_center.y + b,
                                        outline=self._plane.color_figure)

    def __draw_spectrum_ellipse_by_lib(
            self,
            point_center: Point,
            a: int | float,
            b: int | float,
            h: int,
            n: int
    ):
        """
        Метод строит спектр по алгоритму
        """
        list_times = list()

        c = a / b
        for _ in range(n):
            # строим эллипс
            beg = CompareTimeCircle.time_now()
            self._plane.create_oval(point_center.x - a, point_center.y - b,
                                    point_center.x + a, point_center.y + b,
                                    outline=self._plane.color_figure)
            end = CompareTimeCircle.time_now() - beg

            list_times.append((end, a))

            a += h
            b = a / c

        return list_times

    def __draw_spectrum_ellipse_by_alg(
            self,
            point_center: Point,
            a: int | float,
            b: int | float,
            h: int,
            n: int,
            alg: type[
                CanonicalEllipse |
                ParametricEllipse |
                BresenhamEllipse |
                MidPointAlgEllipse
                ]
    ):
        """
        Метод строит спектр по алгоритму
        """
        list_times = list()

        c = a / b
        for _ in range(n):
            # строим эллипс
            build_alg = alg(point_center, a, b)
            build_time = self._plane.draw_ellipse(build_alg)

            list_times.append((build_time, a))

            a += h
            b = a / c

        return list_times

    def __draw_spectrum_ellipse(self):
        """
        Метод позволяет отобразить спектр эллипсов
        """
        point_center = self.__get_point_center(self._entry_get_xc_el, self._entry_get_yc_el)
        a, b = self.__get_a_b(self._entry_get_spect_a, self._entry_get_spect_b)
        h = self.__get_h(self._entry_get_step_el)
        n = self.__get_n(self._entry_get_N_el)

        if not self.__check_a_b(a, b) or isinstance(h, str) or isinstance(n, str) \
                or not self.__check_points_center(point_center):
            return

        match self._rbt_algs.get():
            case "Каноническое уравнение":
                self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, CanonicalEllipse)
            case "Параметрическое уравнение":
                self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, ParametricEllipse)
            case "Алгоритм Брезенхема":
                self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, BresenhamEllipse)
            case "Алгоритм средней точки":
                self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, MidPointAlgEllipse)
            case "Библиотечный алгоритм":
                self.__draw_spectrum_ellipse_by_lib(point_center, a, b, h, n)

    @staticmethod
    def __convert_to_r_list_time_list(list_times: list[tuple[int | float, int | float]]):
        """
        Метод конвертирует список со временем и радиусом в два списка
        """
        times = list()
        radius = list()

        for time, r in list_times:
            print(f"time = {time}, r = {r}")
            times.append(time)
            radius.append(r)

        return times, radius

    def __cmp_time_circle(self):
        """
        Метод позволяет получить зависимость времени работы алгоритма от радиуса
        """

        # очищаем если уже получали
        self.cmp_time_circle.times.clear()
        self.cmp_time_circle.radius_list.clear()

        point_center = Point(x=750, y=750)
        r = 100
        h = 10
        n = 10

        list_times = self.__draw_spectrum_circle_by_alg(point_center, r, h, n, CanonicalCircle)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.cmp_time_circle.times.append(times)
        self.cmp_time_circle.radius_list.append(radius)

        list_times = self.__draw_spectrum_circle_by_alg(point_center, r, h, n, ParametricCircle)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.cmp_time_circle.times.append(times)
        self.cmp_time_circle.radius_list.append(radius)

        list_times = self.__draw_spectrum_circle_by_alg(point_center, r, h, n, BresenhamCircle)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.cmp_time_circle.times.append(times)
        self.cmp_time_circle.radius_list.append(radius)

        list_times = self.__draw_spectrum_circle_by_alg(point_center, r, h, n, MidPointAlgCircle)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.cmp_time_circle.times.append(times)
        self.cmp_time_circle.radius_list.append(radius)

        list_times = self.__draw_spectrum_circle_by_lib(point_center, r, h, n)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.cmp_time_circle.times.append(times)
        self.cmp_time_circle.radius_list.append(radius)

        self._plane.clean_plane()
        self.cmp_time_circle.print_compare()

    def __cmp_time_ellipse(self):
        """
        Метод позволяет получить зависимость времени работы алгоритма от радиуса
        """

        # очищаем если уже получали
        self.__cmp_time_ellipse.times.clear()
        self.__cmp_time_ellipse.radius_list.clear()

        point_center = Point(x=750, y=750)
        a, b = 100, 50
        h = 100
        n = 10

        list_times = self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, CanonicalEllipse)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.__cmp_time_ellipse.times.append(times)
        self.__cmp_time_ellipse.radius_list.append(radius)

        list_times = self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, ParametricEllipse)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.__cmp_time_ellipse.times.append(times)
        self.__cmp_time_ellipse.radius_list.append(radius)

        list_times = self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, BresenhamEllipse)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.__cmp_time_ellipse.times.append(times)
        self.__cmp_time_ellipse.radius_list.append(radius)

        list_times = self.__draw_spectrum_ellipse_by_alg(point_center, a, b, h, n, MidPointAlgEllipse)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.__cmp_time_ellipse.times.append(times)
        self.__cmp_time_ellipse.radius_list.append(radius)

        list_times = self.__draw_spectrum_ellipse_by_lib(point_center, a, b, h, n)
        times, radius = self.__convert_to_r_list_time_list(list_times)
        self.__cmp_time_ellipse.times.append(times)
        self.__cmp_time_ellipse.radius_list.append(radius)

        self._plane.clean_plane()
        self.__cmp_time_ellipse.print_compare()

    @staticmethod
    def print_info() -> None:
        """
        Метод выводит информацию о программе
        """
        text = 'С помощью данной программы можно построить окружность или эллипс 5-ми способами:\n' \
               '1) используя Каноническое уравнение;\n' \
               '2) используя Параметрическое уравнение;\n' \
               '3) алгоритм Брезенхема;\n' \
               '4) алгоритм средней точки;\n' \
               '5) библиотечной функцией.\n' \
               '\nДля построения окружности необходимо задать центр (Xc, Yc)\n' \
               'и радиус R и выбрать метод построения из списка предложенных.\n' \
               '\nДля построения эллипса необходимо задать центр (Xc, Yc)\n' \
               'и величины полуосей а и b; выбрать метод построения из списка предложенных.\n' \
               '\nДля построения спектра фигур\n' \
               'необходимо задать центр фигуры, радиусы (полуоси)\n' \
               'выбрать метод для построения,\n' \
               'а также шаг изменения и количество фигур.\n' \
               '\nДля анализа времени работы построения окружности нужно нажать на кнопку ' \
               'Сравнить алгоритмы построения окружности".\n' \
               '\nДля анализа времени работы построения эллипса нужно нажать на кнопку ' \
               '"Сравнение алгоритмы построения эллипса".\n'

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
