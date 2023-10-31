from plane import *
from checks import *
from tkinter import messagebox
from PIL import Image, ImageTk


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """
    
    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()
        self.title("Лабораторная №2, 20-й вариант, Лысцев Никита ИУ7-43Б")

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

        # виджеты для переноса изображения
        # -----------------------------------------------
        self.lbl_image_transfer = self.draw_label("Перенос изображения")
        self.lbl_image_transfer.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_image_transfer.grid(row=0, column=0, columnspan=3, sticky='wens')

        self.info_transfer = self.draw_button("i")
        self.info_transfer.config(command=lambda: self.about_transfer())
        self.info_transfer.grid(row=0, column=3, sticky='wens')

        self.lbl_get_dx = self.draw_label("dx:")
        self.lbl_get_dx.grid(row=1, column=0, sticky='wens')

        self.entry_get_dx = self.draw_entry()
        self.entry_get_dx.grid(row=1, column=1, sticky='wens')

        self.lbl_get_dy = self.draw_label("dy:")
        self.lbl_get_dy.grid(row=1, column=2, sticky='wens')

        self.entry_get_dy = self.draw_entry()
        self.entry_get_dy.grid(row=1, column=3, sticky='wens')

        self.btn_image_transfer = self.draw_button("Переместить изображение")
        self.btn_image_transfer.config(command=lambda: self.transfer_figure())
        self.btn_image_transfer.grid(row=2, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджет масштабирования
        # -----------------------------------------------
        self.lbl_scaling = self.draw_label("Масштабирование")
        self.lbl_scaling.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_scaling.grid(row=3, column=0, columnspan=3, sticky='wens')

        self.info_scaling = self.draw_button("i")
        self.info_scaling.config(command=lambda: self.about_scaling())
        self.info_scaling.grid(row=3, column=3, sticky='wens')

        self.lbl_get_kx = self.draw_label("kx:")
        self.lbl_get_kx.grid(row=4, column=0, sticky='wens')

        self.entry_get_kx = self.draw_entry()
        self.entry_get_kx.grid(row=4, column=1, sticky='wens')

        self.lbl_get_ky = self.draw_label("ky:")
        self.lbl_get_ky.grid(row=4, column=2, sticky='wens')

        self.entry_get_ky = self.draw_entry()
        self.entry_get_ky.grid(row=4, column=3, sticky='wens')

        self.lbl_get_scal_xc = self.draw_label("x_c:")
        self.lbl_get_scal_xc.grid(row=5, column=0, sticky='wens')

        self.entry_get_scal_xc = self.draw_entry()
        self.entry_get_scal_xc.grid(row=5, column=1, sticky='wens')

        self.lbl_get_scal_yc = self.draw_label("y_c:")
        self.lbl_get_scal_yc.grid(row=5, column=2, sticky='wens')

        self.entry_get_scal_yc = self.draw_entry()
        self.entry_get_scal_yc.grid(row=5, column=3, sticky='wens')

        self.btn_scaling = self.draw_button("Масштабировать")
        self.btn_scaling.config(command=lambda: self.scaling_figure())
        self.btn_scaling.grid(row=6, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты поворота изображения
        # -----------------------------------------------
        self.lbl_image_rotate = self.draw_label("Поворот изображения")
        self.lbl_image_rotate.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_image_rotate.grid(row=7, column=0, columnspan=3, sticky='wens')

        self.info_rotate = self.draw_button("i")
        self.info_rotate.config(command=lambda: self.about_rotate())
        self.info_rotate.grid(row=7, column=3, sticky='wens')

        self.lbl_get_rot_xc = self.draw_label("x_c:")
        self.lbl_get_rot_xc.grid(row=8, column=0, sticky='wens')

        self.entry_get_rot_xc = self.draw_entry()
        self.entry_get_rot_xc.grid(row=8, column=1, sticky='wens')

        self.lbl_get_rot_yc = self.draw_label("y_c:")
        self.lbl_get_rot_yc.grid(row=8, column=2, sticky='wens')

        self.entry_get_rot_yc = self.draw_entry()
        self.entry_get_rot_yc.grid(row=8, column=3, sticky='wens')

        self.lbl_get_angle = self.draw_label(" Angle:")
        self.lbl_get_angle.grid(row=9, column=0, sticky='wens', columnspan=2)

        self.entry_get_angle = self.draw_entry()
        self.entry_get_angle.grid(row=9, column=2, sticky='wens', columnspan=2)

        self.btn_image_rotate = self.draw_button("Повернуть изображение")
        self.btn_image_rotate.config(command=lambda: self.rotate_figure())
        self.btn_image_rotate.grid(row=10, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты сохранения состояний
        # -----------------------------------------------
        self.lbl_state_figure = self.draw_label("Состояния")
        self.lbl_state_figure.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_state_figure.grid(row=11, column=0, columnspan=3, sticky='wens')

        self.info_state = self.draw_button("i")
        self.info_state.config(command=lambda: self.about_state())
        self.info_state.grid(row=11, column=3, sticky='wens')

        self.btn_step_back = self.draw_button("Шаг назад")
        self.btn_step_back.config(command=lambda: self.step_back())
        self.btn_step_back.grid(row=12, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты изменения параметров фигуры
        # -----------------------------------------------
        self.lbl_param_figure = self.draw_label("Параметры фигуры")
        self.lbl_param_figure.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_param_figure.grid(row=13, column=0, columnspan=3, sticky='wens')

        self.info_param_figure = self.draw_button("i")
        self.info_param_figure.config(command=lambda: self.about_param_figure())
        self.info_param_figure.grid(row=13, column=3, sticky='wens')

        self.lbl_get_a = self.draw_label("a:")
        self.lbl_get_a.grid(row=14, column=0, sticky='wens')

        self.entry_get_a = self.draw_entry()
        self.entry_get_a.grid(row=14, column=1, sticky='wens')

        self.lbl_get_b = self.draw_label("b:")
        self.lbl_get_b.grid(row=14, column=2, sticky='wens')

        self.entry_get_b = self.draw_entry()
        self.entry_get_b.grid(row=14, column=3, sticky='wens')

        self.lbl_get_xc_ellipse = self.draw_label("xc_ellipse:")
        self.lbl_get_xc_ellipse.config(font=("Courier New", 10, 'bold'))
        self.lbl_get_xc_ellipse.grid(row=15, column=0, sticky='wens')

        self.entry_get_xc_ellipse = self.draw_entry()
        self.entry_get_xc_ellipse.grid(row=15, column=1, sticky='wens')

        self.lbl_get_yc_ellipse = self.draw_label("yc_ellipse:")
        self.lbl_get_yc_ellipse.config(font=("Courier New", 10, 'bold'))
        self.lbl_get_yc_ellipse.grid(row=15, column=2, sticky='wens')

        self.entry_get_yc_ellipse = self.draw_entry()
        self.entry_get_yc_ellipse.grid(row=15, column=3, sticky='wens')

        self.lbl_get_x_inters = self.draw_label("Абсцисса точки пересечения прямых:")
        self.lbl_get_x_inters.grid(row=16, column=0, sticky='wens', columnspan=4)

        self.entry_get_x_inters = self.draw_entry()
        self.entry_get_x_inters.config(justify=tk.CENTER)
        self.entry_get_x_inters.grid(row=17, column=0, sticky='wens', columnspan=4)

        self.btn_change_param_figure = self.draw_button("Применить изменения")
        self.btn_change_param_figure.config(command=lambda: self.change_param_figure())
        self.btn_change_param_figure.grid(row=18, column=0, columnspan=4, sticky='wens')
        # -----------------------------------------------

        # виджеты отображения центральной точки фигуры
        # -----------------------------------------------
        self.lbl_param_figure = self.draw_label("Центральная точка фигуры")
        self.lbl_param_figure.config(font=("Courier New", 14, 'bold', "underline"))
        self.lbl_param_figure.grid(row=19, column=0, columnspan=4, sticky='wens')

        self.text_varx, self.text_vary = tk.StringVar(), tk.StringVar()

        self.text_varx.set(f"X: {self.plane.figure.center_figure.x: .2f}")
        self.text_vary.set(f"Y: {self.plane.figure.center_figure.y: .2f}")

        self.lbl_center_x = self.draw_label("")
        self.lbl_center_x.config(textvariable=self.text_varx)
        self.lbl_center_x.grid(row=20, column=0, columnspan=2, sticky='wens')

        self.lbl_center_y = self.draw_label("")
        self.lbl_center_y.config(textvariable=self.text_vary)
        self.lbl_center_y.grid(row=20, column=2, columnspan=2, sticky='wens')
        # -----------------------------------------------

        self.btn_task = self.draw_button("Условие задачи")
        self.btn_task.config(command=lambda: self.print_task())
        self.btn_task.grid(row=21, column=0, columnspan=4, sticky='wens')

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

        frame_widgets.config(bg=LightCyan)

        return frame_widgets

    def draw_plane(self) -> PlaneCanvas:
        """
        Метод размещает холст (canvas) для плоскости (plane) на главном окне
        :return: холст
        """
        plane_width = self.frame_plane.winfo_screenwidth() - 400
        plane_height = self.frame_plane.winfo_screenheight() - 70

        plane = PlaneCanvas(
            y_min=-15,
            y_max=15,
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

    def rotate_figure(self) -> None:
        """
        Метод поворачивает фигуру
        """

        rot_xc, rot_yc = self.get_data(self.entry_get_rot_xc, self.entry_get_rot_yc)

        if not self.is_float(rot_xc) or not self.is_float(rot_yc):
            messagebox.showwarning("Некорректные данные центра поворота!\n",
                                   "Были получены некорректные данные центра поворота!\n"
                                   "Ожидался ввод действительных или целых чисел.\n"
                                   "Пожалуйста, попробуйте снова.\n")
            return

        angle = self.entry_get_angle.get()

        if not self.is_float(angle):
            messagebox.showwarning("Некорректные данные угла поворота!\n",
                                   "Были получены некорректные данные угла поворота!\n"
                                   "Ожидался ввод действительных или целых чисел.\n"
                                   "Величина вводимого угла - градусы\n"
                                   "Пожалуйста, попробуйте снова.")
            return

        rot_xc, rot_yc, angle = map(float, [rot_xc, rot_yc, angle])

        center_rotate = Point(x=rot_xc, y=rot_yc)

        self.plane.rotate_figure(center_rotate, angle)
        self.get_center_figure()

    def transfer_figure(self) -> None:
        """
        Метод переносит фигуру
        """
        dx, dy = self.get_data(self.entry_get_dx, self.entry_get_dy)

        if not self.is_float(dx) or not self.is_float(dy):
            messagebox.showwarning("Некорректные данные величин смешения для переноса!\n",
                                   "Были получены некорректные данные величин смещения для переноса фигуры!\n"
                                   "Ожидался ввод действительных или целых чисел. \n"
                                   "Пожалуйста, попробуйте снова.")
            return

        dx, dy = map(float, [dx, dy])

        self.plane.transfer_figure(dx, dy)
        self.get_center_figure()

    def scaling_figure(self) -> None:
        """
        Метод масштабирует фигуру
        """
        kx, ky = self.get_data(self.entry_get_kx, self.entry_get_ky)
        xc, yc = self.get_data(self.entry_get_scal_xc, self.entry_get_scal_yc)

        if not self.is_float(kx) or not self.is_float(ky):
            messagebox.showwarning("Некорректные данные коэффициентов масштабирования!\n",
                                   "Были получены некорректные данные коэффициентов масштабирования!\n"
                                   "Ожидался ввод действительных или целых чисел. \n"
                                   "Пожалуйста, попробуйте снова.")
            return

        if not self.is_float(xc) or not self.is_float(yc):
            messagebox.showwarning("Некорректные данные центра масштабирования!\n",
                                   "Были получены некорректные данные центра масштабирования!\n"
                                   "Ожидался ввод действительных или целых чисел. \n"
                                   "Пожалуйста, попробуйте снова.")
            return

        kx, ky, xc, yc = map(float, [kx, ky, xc, yc])

        self.plane.scaling_figure(kx, ky, xc, yc)
        self.get_center_figure()

    def step_back(self) -> None:
        """
        Метод возвращает предыдущее состояние фигуры
        """
        self.plane.step_back()
        self.get_center_figure()

    def change_param_figure(self) -> None:
        """
        Метод позволяет сменить параметры фигуры
        """
        a, b = self.get_data(self.entry_get_a, self.entry_get_b)
        xc_ellipse, yc_ellipse = self.get_data(self.entry_get_xc_ellipse, self.entry_get_yc_ellipse)
        x_inters = self.entry_get_x_inters.get()

        if not self.is_float(a) or not self.is_float(b) or \
                not self.is_float(xc_ellipse) or not self.is_float(yc_ellipse) or \
                not self.is_float(x_inters):
            messagebox.showwarning("Некорректные данные параметров фигуры!\n",
                                   "Были получены некорректные данные параметров фигуры!\n"
                                   "Ожидался ввод действительных или целых чисел. \n"
                                   "Пожалуйста, попробуйте снова.")
            return

        a, b, xc_ellipse, yc_ellipse, x_inters = map(float, [a, b, xc_ellipse, yc_ellipse, x_inters])
        self.plane.change_param_figure(a, b, xc_ellipse, yc_ellipse, x_inters)
        self.get_center_figure()

    def get_center_figure(self):
        """
        Метод получает центр фигуры для вывода
        """
        point_center = self.plane.figure.get_center_figure()
        self.text_varx.set(f"X: {point_center.x: .2f}")
        self.text_vary.set(f"y: {point_center.y: .2f}")

    @staticmethod
    def about_transfer():
        """
        Метод выводит информацию об операции переноса
        """
        text = "Для выполнения переноса фигуры необходимы:\n" \
               "dx, dy - величины смещения " \
               "по осям абсцисс и ординат соответственно."
        messagebox.showinfo("", text)

    @staticmethod
    def about_scaling():
        """
        Метод выводит информацию об операции масштабирования
        """
        text = "Для выполнения масштабирования фигуры необходимы:\n" \
               "Точка (x_c, y_c) - центр масштабирования, то есть точка, " \
               "относительно которой выполняется операция масштабирования;\n" \
               "kx, ky - коэффициенты масштабирования " \
               "по осям абсцисс и ординат соответственно."
        messagebox.showinfo("", text)

    @staticmethod
    def about_rotate():
        """
        Метод выводит информацию об операции поворота
        """
        text = "Для выполнения поворота фигуры необходимы:\n" \
               "Точка (x_c, y_c) - центр поворота, то есть точка, " \
               "относительно которой выполняется операция поворота;\n" \
               "angle - угол, на который должен быть совершен поворот в градусах."
        messagebox.showinfo("", text)

    @staticmethod
    def about_param_figure():
        """
        Метод выводит информацию о параметрах фигуры
        """
        text = "Параметрическое уравнение эллипса в декартовых координатах имеет вид:\n" \
               "x = xc_ellipse + a*cos(theta)cos(phi) - b*sin(theta)*sin(phi)\n" \
               "y = yc_ellipse + a*cos(theta)sin(phi) + b*sin(theta)*cos(phi)\n" \
               "где:\n" \
               "(xc_ellipse, yc_ellipse) - координаты центра эллипса;\n" \
               "a и b - длины большой и малой полуосей соответственно;\n" \
               "theta - угол между направлением большой полуоси эллипса и осью x, " \
               "который изменяется от -pi/2 до pi/2 (от -90 до 90 градусов);\n" \
               "phi - угол поворота эллипса вокруг его центра.\n\n" \
               "Абсцисса точки пересечения прямых - абсцисса точки, " \
               "где пересекаются прямые. Ордината точки пересечения прямых " \
               "определяется из ординаты центра эллипса"

        messagebox.showinfo("", text)

    @staticmethod
    def about_state():
        """
        Метод выводит информацию о том, что такое состояние
        """
        text = "Состояние - положение фигуры после применения одной из 3-х операций:\n" \
               "1) Перенос;\n" \
               "2) Масштабирование;\n" \
               "3) Поворот.\n" \
               "Операция возврата на один шаг назад позволяет отобразить" \
               " на плоскости фигуру после применения к ней предыдущей операции"
        messagebox.showinfo("", text)

    @staticmethod
    def print_task():
        """
        Метод выводит условие задачи
        """
        # создание дополнительного окна
        window = tk.Toplevel()
        window.grab_set()

        # создание холста на окне
        canvas = tk.Canvas(window, width=800, height=400)
        canvas.pack()

        # загрузка изображения с помощью Pillow
        pil_image = Image.open('../lab2_task.png')

        # преобразование изображения в PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)

        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

        # запуск цикла обработки событий для дополнительного окна
        window.mainloop()
