from plane import *
from listpoints import *
from checks import *


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()
        self.title("Лабораторная №1, 20-й вариант, Лысцев Никита ИУ7-43Б")
        root_width = self.winfo_screenwidth()
        root_height = self.winfo_screenheight() - 65
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # создал фреймы для всего
        # -----------------------------------------------
        self.frame_plane = self.create_frame_plane()
        self.frame_plane.pack(side=tk.RIGHT)
        self.frame_widgets = self.create_frame_widgets()
        self.frame_widgets.pack()
        # -----------------------------------------------
        self.plane = self.draw_plane()
        self.plane.pack()

        # виджеты для добавления точки
        # -----------------------------------------------
        self.lbl_add_point = self.draw_label("Добавить точку")
        self.lbl_add_point.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_add_point.grid(row=0, column=0, columnspan=4, sticky='wens')

        self.lbl_add_x = self.draw_label("X:")
        self.lbl_add_x.grid(row=1, column=0, sticky='wens')

        self.entry_add_x = self.draw_entry()
        self.entry_add_x.grid(row=1, column=1, sticky='wens')

        self.lbl_add_y = self.draw_label("Y:")
        self.lbl_add_y.grid(row=1, column=2, sticky='wens')

        self.entry_add_y = self.draw_entry()
        self.entry_add_y.grid(row=1, column=3, sticky='wens')

        self.btn_add_point = self.draw_button("Добавить точку")
        self.btn_add_point.config(command=lambda: self.add_point())
        self.btn_add_point.grid(row=2, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджет переключения множеств
        # -----------------------------------------------
        values = "Первое множество", "Второе множество"
        self.rbt_var = tk.StringVar(value=values[0])

        self.rbt_set1 = self.draw_radiobutton(values[0])
        self.rbt_set1.grid(row=3, column=0, columnspan=2, sticky='wens')

        self.rbt_set2 = self.draw_radiobutton(values[1])
        self.rbt_set2.grid(row=3, column=2, columnspan=2, sticky='wens')
        # -----------------------------------------------

        # виджет удаления точки по номеру
        # -----------------------------------------------
        self.lbl_del_point = self.draw_label("Удалить точку")
        self.lbl_del_point.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_del_point.grid(row=4, column=0, columnspan=4, sticky='wens')

        self.lbl_n_del = self.draw_label("Номер точки:")
        self.lbl_n_del.grid(row=5, column=0, sticky='wens', columnspan=2)

        self.entry_n_del = self.draw_entry()
        self.entry_n_del.grid(row=5, column=2, sticky='wens', columnspan=2)

        self.btn_del_point = self.draw_button("Удалить точку")
        self.btn_del_point.config(command=lambda: self.del_point_by_number())
        self.btn_del_point.grid(row=6, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты изменения точки
        # -----------------------------------------------
        self.lbl_change_point = self.draw_label("Изменить точку")
        self.lbl_change_point.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_change_point.grid(row=7, column=0, columnspan=4, sticky='wens')

        self.lbl_n_change = self.draw_label("Номер точки:")
        self.lbl_n_change.grid(row=8, column=0, sticky='wens', columnspan=2)

        self.entry_n_change = self.draw_entry()
        self.entry_n_change.grid(row=8, column=2, sticky='wens', columnspan=2)

        self.lbl_new_x = self.draw_label(" New X:")
        self.lbl_new_x.grid(row=9, column=0, sticky='wens')

        self.entry_new_x = self.draw_entry()
        self.entry_new_x.grid(row=9, column=1, sticky='wens')

        self.lbl_new_y = self.draw_label("New Y:")
        self.lbl_new_y.grid(row=9, column=2, sticky='wens')

        self.entry_new_y = self.draw_entry()
        self.entry_new_y.grid(row=9, column=3, sticky='wens')

        self.btn_change_point = self.draw_button("Изменить точку")
        self.btn_change_point.config(command=lambda: self.change_point_by_number())
        self.btn_change_point.grid(row=10, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты отображения точек
        # -----------------------------------------------
        self.lbl_set1 = self.draw_label("Первое множество")
        self.lbl_set1.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_set1.grid(row=11, column=0, sticky='wens', columnspan=2)

        self.lbl_set2 = self.draw_label("Второе множество")
        self.lbl_set2.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_set2.grid(row=11, column=2, sticky='wens', columnspan=2)

        self.columns = "number", "point"

        # Создал фреймы для таблицы с точками обоих множеств
        # -----------------------------------------------
        frame_sets = tk.Frame(self)
        frame_sets.pack()
        self.frame_set1 = tk.Frame(frame_sets)
        self.frame_set1.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_set2 = tk.Frame(frame_sets)
        self.frame_set2.pack(side=tk.RIGHT)
        # -----------------------------------------------

        self.listpoints_set1 = self.draw_listpoints(self.frame_set1)
        self.listpoints_set1.pack(side=tk.LEFT, fill=tk.Y)

        self.listpoints_set2 = self.draw_listpoints(self.frame_set2)
        self.listpoints_set2.pack(side=tk.LEFT)

        scroll_set1, scroll_set2 = self.draw_set_scrollbars()
        scroll_set1.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_set2.pack(side=tk.RIGHT, fill=tk.Y)
        # -----------------------------------------------

        # виджеты доп. кнопок
        # -----------------------------------------------

        # Создал фрейм для доп. кнопок
        # -----------------------------------------------
        frame_tasks = self.create_frame_widgets()
        frame_tasks.pack()
        # -----------------------------------------------

        self.btn_task = tk.Button(frame_tasks, text="Условие задачи", font=("Courier New", 12),
                                  relief=tk.RAISED, bg=WHITE)
        self.btn_task.config(command=lambda: MyWindow.print_task())
        self.btn_task.grid(row=0, column=0, columnspan=4, sticky='wens')

        self.btn_print_res = tk.Button(frame_tasks, text="Вывести результаты", font=("Courier New", 12),
                                       relief=tk.RAISED, bg=WHITE, command=lambda: self.plane.draw_solve())
        self.btn_print_res.grid(row=1, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

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
        Метод создает фрейм для виджетов (plane)
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
            y_min=-10,
            y_max=10,
            master=self.frame_plane,
            width=plane_width,
            height=plane_height,
            bg="#FFFFFF"
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
            font=("Courier New", 14, 'bold'),
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
            justify=tk.RIGHT,
            font=("Courier New", 14)
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
            font=("Courier New", 12),
            relief=tk.RAISED
        )

        button.config(bg=WHITE)

        return button

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
            variable=self.rbt_var,
            font=("Courier New", 12, 'bold')
        )

        return rbt

    def draw_listpoints(self, frame: tk.Frame) -> ListPoints:
        """
        Метод создает таблицу для отображения точек
        :param frame: окно
        :return: фрейм
        """
        listpoints = ListPoints(
            frame,
            columns=self.columns,
            show="headings",
            height=14
        )

        return listpoints

    def draw_set_scrollbars(self) -> (ttk.Scrollbar, ttk.Scrollbar):
        """
        Метод создает полосу прокрутки для отображенных точек
        :return: полосу прокрутки
        """
        set1_scrollbar = ttk.Scrollbar(self.frame_set1, command=self.listpoints_set1.yview)
        self.listpoints_set1.config(yscrollcommand=set1_scrollbar.set)

        set2_scrollbar = ttk.Scrollbar(self.frame_set2, command=self.listpoints_set2.yview)
        self.listpoints_set2.config(yscrollcommand=set2_scrollbar.set)

        return set1_scrollbar, set2_scrollbar

    @staticmethod
    def get_point(entry_x: tk.Entry, entry_y: tk.Entry) -> (str, str):
        """
        Метод получает точку с однострочных полей ввода координат
        :param entry_x: поле ввода абсциссы
        :param entry_y: поле вода ординаты
        :return:
        """
        x = entry_x.get()
        y = entry_y.get()

        return x, y

    @staticmethod
    def is_int(x: str) -> bool:
        """
        Метод проверяет, является ли строка целым числом
        :param x: строка
        :return: True, если целое число, False иначе
        """
        if check_int(x):
            return True

        messagebox.showwarning(
            "Некорректный ввод!",
            "Введены некорректные данные для номера точки!"
        )

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

        messagebox.showwarning(
            "Некорректный ввод!",
            "Введены недопустимые символы!"
        )

        return False

    def check_input_point(self, x: str, y: str) -> bool:
        """
        Метод проверяет введенную точку на корректность
        :param x: абсцисса точки
        :param y: ордината точки
        :return: True, если точка валидная, False иначе
        """
        if not self.is_float(x) or not self.is_float(y):
            return False

        return True

    def add_point(self) -> None:
        """
        Метод вставляет в поле в зависимости от выбора множества
        :return: None
        """
        x, y = self.get_point(self.entry_add_x, self.entry_add_y)

        if self.check_input_point(x, y):
            x, y = float(x), float(y)
            if self.rbt_var.get() == "Первое множество":
                self.listpoints_set1.add_point((x, y))
                self.plane.draw_point(x, y, color=BLUE)
            else:
                self.listpoints_set2.add_point((x, y))
                self.plane.draw_point(x, y, color=RED)

    def del_if_valid_num(self, table: ListPoints, n: int, color: str) -> None:
        """
        Метод удаляет точку по валидному номеру
        :param table: таблица точек
        :param n: номер точки
        :param color: цвет точки
        :return: None
        """
        if table.is_valid_number(n):
            table.del_point(n)
            self.plane.del_point(n, color=color)
            return

        messagebox.showwarning("Неверный номер точки!",
                               "Точки с введенным номером не существует!")

    def del_point_by_number(self) -> None:
        """
        Метод удаляет из поля точку в зависимости от выбора множества
        :return: None
        """
        n = self.entry_n_del.get()

        if self.is_int(n):
            n = int(n)
            if self.rbt_var.get() == "Первое множество":
                self.del_if_valid_num(self.listpoints_set1, n, color=BLUE)
            else:
                self.del_if_valid_num(self.listpoints_set2, n, color=RED)

    def change_if_valid_num(self, table: ListPoints,
                            num: int,
                            new_x: float,
                            new_y: float,
                            color: str) -> None:
        """
        Метод изменяет точку по валидному номеру
        :param table: окно
        :param num: номер точки
        :param new_x: новая абсцисса точки
        :param new_y: новая ордината точки
        :param color: цвет точки
        :return: None
        """
        if table.is_valid_number(num):
            table.change_point(num, new_x, new_y)
            self.plane.change_point(num, new_x, new_y, color=color)
            return

        messagebox.showwarning("Неверный номер точки!",
                               "Точки с введенным номером не существует!")

    def change_point_by_number(self) -> None:
        """
        Метод изменяет точку в одном из множеств
        :return: None
        """
        n = self.entry_n_change.get()
        x, y = self.get_point(self.entry_new_x, self.entry_new_y)

        if self.is_int(n) and self.check_input_point(x, y):
            n, x, y = int(n), float(x), float(y)
            if self.rbt_var.get() == "Первое множество":
                self.change_if_valid_num(self.listpoints_set1, n, x, y, color=BLUE)
            else:
                self.change_if_valid_num(self.listpoints_set2, n, x, y, color=RED)

    @staticmethod
    def print_task():
        """
        Метод выводи условие задачи
        """
        text = "На плоскости даны два множества точек. " \
               "Найти пару треугольников (каждый треугольник в качестве вершин имеет три " \
               "различные точки одного и того же множества; " \
               "треугольники строятся на точках различных множеств) таких, что прямая, " \
               "соединяющая точки пересечения высот, образует минимальный угол с осью абсцисс"
        messagebox.showinfo("task", text)
