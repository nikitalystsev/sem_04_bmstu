from task import *
import tkinter as tk
from tkinter import messagebox

CONST_SCALE = 5

ORANGE = "#FFA500"
RED = "#FF0000"
DARKCYAN = "DarkCyan"
GREEN = "#008000"
BLUE = "#0000FF"
YELLOW = "#FFFF00"
WHITE = "#FFFFFF"
BLACK = "#000000"
Aquamarine = "#7FFFD4"
LightCyan = "#E0FFFF"
SILVER = "#C0C0C0"

EPS = 1e-9


def float_equal(a, b):
    """
    Функция сравнивает вещественные числа
    """
    return abs(a - b) < EPS


class PlaneCanvas(tk.Canvas):
    """
    Плоскость
    """

    def __init__(self, y_min, y_max, grid_step=50, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        :param y_min: желаемая минимальная ордината
        :param y_max: желаемая максимальная ордината
        :param x_min: желаемая минимальная абсцисса
        :param master: окно, на котором размещается виджет
        :param kwargs: прочие родительские аргументы
        """
        super().__init__(master, **kwargs)
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.y_min = y_min
        self.y_max = y_max
        self.x_max, self.x_min = self.get_x_coord(self.y_max)
        self.grid_step = grid_step
        self.km = self.get_default_km()
        self.task = Task()
        self.draw_grid()

    def get_x_coord(self, y_max: float):
        """
        Метод вычисляет максимальную и минимальную абсциссы
        при заданных размерах холста
        """
        axis_coef = self.width / self.height
        x_max = y_max * axis_coef

        return x_max, -x_max

    def get_default_km(self):
        """
        Метод вычисляет коэф-т масштабирования по умолчанию
        """
        y_max, y_min = 10, -10
        x_max, x_min = self.get_x_coord(y_max)

        kx = (self.width - 0) / (x_max - x_min)
        ky = (self.height - 0) / (y_max - y_min)

        return min(kx, ky)

    def plane_default(self):
        """
        Метод возвращает параметры масштаба по умолчанию
        """
        self.y_max, self.y_min = 10, -10
        self.x_max, self.x_min = self.get_x_coord(self.y_max)
        self.km = self.get_default_km()

    def get_scal_coord(self, max_coord: float, is_x: bool):
        """
        Метод вычисляет масштабируемые координаты
        """
        if is_x:
            axis_coef = self.height / self.width
            y_max = (max_coord + CONST_SCALE) * axis_coef
            self.x_max = max_coord + CONST_SCALE
            self.y_max = y_max
            self.x_min = -max_coord - CONST_SCALE
            self.y_min = -y_max
            return

        axis_coef = self.width / self.height
        x_max = (max_coord + CONST_SCALE) * axis_coef
        self.x_max = x_max
        self.y_max = max_coord + CONST_SCALE
        self.x_min = -x_max
        self.y_min = -max_coord - CONST_SCALE

    def get_km(self) -> float:
        """
        Функция вычисляет коэффициент масштабирования
        :return: None
        """
        # вычисляем разности максимальных и минимальных значений
        diff_x, diff_y = self.x_max - self.x_min, self.y_max - self.y_min
        # определяем начальные значения коэффициентов масштабирования по осям
        kx = ky = self.get_default_km()

        # вычисляем коэффициенты масштабирования по осям
        if not float_equal(diff_x, 0) and not float_equal(diff_y, 0):
            kx = (self.width - 0) / diff_x
            ky = (self.height - 0) / diff_y

        return min(kx, ky)

    def scaling(self) -> None:
        """
        Метод масштабирует плоскость
        :return: None
        """
        list_points = self.task.set1 + self.task.set2 + self.task.inters_h

        x_s = [point.x for point in list_points]
        y_s = [point.y for point in list_points]

        if len(x_s) == 0 or len(y_s) == 0:
            self.plane_default()
            return

        x_max, y_max = max(map(abs, x_s)), max(map(abs, y_s))

        if x_max > y_max:
            self.get_scal_coord(max_coord=x_max, is_x=True)
        else:
            self.get_scal_coord(max_coord=y_max, is_x=False)

        self.km = self.get_km()

    def draw_grid(self) -> None:
        """
        Метод отображает сетку на плоскости и координатные оси
        """

        # Рисуем вертикальные линии с шагом grid_step
        for x in range(self.width // 2, self.width, self.grid_step):
            self.create_line(x, 0, x, self.height, fill=SILVER)  # вправо
            self.create_line(self.width - x, 0, self.width - x, self.height, fill=SILVER)  # влево
            origin_x_left, origin_x_right = self.to_origin_x(self.width - x), self.to_origin_x(x)
            text_left, text_right = f"{round(origin_x_left, 2)}", f"{round(origin_x_right, 2)}"
            self.create_text(x, self.height // 2 - 10, text=text_right)
            self.create_text(self.width - x, self.height // 2 - 10, text=text_left)

        # Рисуем горизонтальные линии с шагом grid_step
        for y in range(self.height // 2, self.height, self.grid_step):
            self.create_line(0, y, self.width, y, fill=SILVER)
            self.create_line(0, self.height - y, self.width, self.height - y, fill=SILVER)
            origin_y_up, origin_y_down = self.to_origin_y(self.height - y), self.to_origin_y(y)
            text_up, text_dowm = f"{round(origin_y_up, 2)}", f"{round(origin_y_down, 2)}"
            if not float_equal(origin_y_up, 0) and not float_equal(origin_y_down, 0):
                self.create_text(self.width // 2 + 14, y, text=text_dowm)
                self.create_text(self.width // 2 + 14, self.height - y, text=text_up)
        # Рисуем оси координат
        # ось ординат
        self.create_line(self.width / 2, self.height, self.width / 2, 0, width=2, arrow="last", fill=BLACK)
        # ось абсцисс
        self.create_line(0, self.height / 2, self.width, self.height / 2, width=2, arrow="last", fill=BLACK)

    def to_origin_x(self, canvas_x: float) -> float:
        """
        Метод преобразует абсциссу точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_x: абсцисса холста
        :return: оригинальная абсцисса
        """
        origin_x = (canvas_x - 0) / self.km + self.x_min

        return origin_x

    def to_origin_y(self, canvas_y: float) -> float:
        """
        Метод преобразует ординату точки, ранее преобразованную
        для отображения на холсте, в оригинальное значение
        :param canvas_y:  ордината холста
        :return: оригинальная ордината
        """
        origin_y = self.y_max - (canvas_y - 0) / self.km

        return origin_y

    def to_origin_coords(self, canvas_x: float, canvas_y: float) \
            -> (float, float):
        """
        Метод преобразует координаты точки, ранее преобразованные
        для отображения на холсте, в оригинальные значения
        :param canvas_x: абсцисса холста
        :param canvas_y: ордината холста
        :return: оригинальные координаты
        """

        return self.to_origin_x(canvas_x), self.to_origin_y(canvas_y)

    def to_canvas_x(self, origin_x: float) -> float:
        """
        Метод преобразует полученную с поля ввода абсциссу
        для отображения на холсте
        :param origin_x: оригинальная абсцисса
        :return: абсцисса холста.
        """
        canvas_x = int(0 + (origin_x - self.x_min) * self.km)

        return canvas_x

    def to_canvas_y(self, origin_y: float) -> float:
        """
        Метод преобразует полученную с поля ввода ординату
        для отображения на холсте
        :param origin_y: оригинальная ордината
        :return: ордината холста
        """
        canvas_y = int(0 + (self.y_max - origin_y) * self.km)

        return canvas_y

    def to_canvas_coords(self, x: float, y: float) -> (float, float):
        """
        Метод преобразует полученные с поля ввода координаты
        для отображения на холсте
        :param x: оригинальная абсцисса
        :param y: оригинальная ордината
        :return: координаты точки для холста
        """

        return self.to_canvas_x(x), self.to_canvas_y(y)

    def create_point(self, x0: float, y0: float, color: str = 'red') -> None:
        """
        Метод отображает точку на плоскости
        """
        self.create_oval(x0 - 3, y0 - 3, x0 + 3, y0 + 3,
                         fill=color, outline=color)

    def draw_list_points(self, list_points: list[Point], color) -> None:
        """
        Метод отображает список точек на холсте
        :param list_points: список точек
        :param color: цвет точек
        :return: None
        """
        for i, point in enumerate(list_points):
            canvas_x, canvas_y = self.to_canvas_coords(point.x, point.y)
            text = f"{i + 1}.({round(point.x, 2)};{round(point.y, 2)})"
            self.create_point(canvas_x, canvas_y, color=color)
            self.create_text(canvas_x + 5, canvas_y - 10, text=text,
                             fill=color, font=("Courier New", 8))

    def draw_set_points(self) -> None:
        """
        Метод отображает введенные точки на плоскости
        :return: None
        """
        # отображение первого множества точек
        self.draw_list_points(self.task.set1, BLUE)
        # отображение второго множества точек
        self.draw_list_points(self.task.set2, RED)
        # отображение прочих точек
        self.draw_list_points(self.task.inters_h, DARKCYAN)

    def draw_point(self, origin_x: float, origin_y: float, color: str) -> None:
        """
        Метод отображает точку на плоскости
        :param origin_x: оригинальная абсцисса
        :param origin_y: оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        self.delete(tk.ALL)  # очищаю весь холст

        # добавляю точку ко множеству точек (первому или второму)
        if color == BLUE:  # первое множество точек
            self.task.set1.append(Point(origin_x, origin_y))
        elif color == RED:  # второе множество точек
            self.task.set2.append(Point(origin_x, origin_y))
        else:  # прочие точки
            if len(self.task.inters_h) == 2:
                # чтобы при каждом новом отображении решения задачи
                # старые точки пересечения высот не отображались
                self.task.inters_h = []
            self.task.inters_h.append(Point(origin_x, origin_y))

        self.scaling()  # выполняется масштабирование
        # рисуются координатные оси, с промежуточными значениями,
        # соответствующими масштабу
        self.draw_grid()
        self.draw_set_points()  # отображаю имеющиеся точки

    def change_point(self, n: int, new_origin_x: float,
                     new_origin_y: float, color: str) -> None:
        """
        Метод изменяет точку
        :param n: номер точки
        :param new_origin_x: новая оригинальная абсцисса
        :param new_origin_y: новая оригинальная ордината
        :param color: цвет точки
        :return: None
        """
        # удаляю старую точку
        self.del_point(n, color)

        # Изменяю данные точки (первого или второго множества)
        if color == BLUE:
            self.task.set1.insert(n - 1, Point(new_origin_x, new_origin_y))
        else:
            self.task.set2.insert(n - 1, Point(new_origin_x, new_origin_y))

        self.task.inters_h = []

        self.task.default_save_param()

        self.delete(tk.ALL)  # очищаю холст
        self.scaling()  # выполняется масштабирование
        # рисуются координатные оси, с промежуточными значениями,
        # соответствующими масштабу
        self.draw_grid()
        self.draw_set_points()  # отображаю имеющиеся точки

    def del_point(self, n: int, color: str) -> None:
        """
        Метод удаляет точку
        :param n: номер точки
        :param color: цвет точки
        :return: None
        """
        # удаляю точку со списка с координатами
        self.task.set1.pop(n - 1) if color == BLUE else self.task.set2.pop(n - 1)

        self.task.inters_h = []

        self.task.default_save_param()

        self.delete(tk.ALL)  # очищаю холст
        self.scaling()  # выполняется масштабирование
        # рисуются координатные оси, с промежуточными значениями,
        # соответствующими масштабу
        self.draw_grid()
        self.draw_set_points()  # отображаем неудаленные точки

    def draw_triangle(self, point1: Point, point2: Point,
                      point3: Point, color: str) -> None:
        """
        Метод строит треугольник по трем точкам
        :param point1: первая точка
        :param point2: вторая точка
        :param point3: третья точка
        :param color: цвет треугольника
        :return: None
        """
        x1, y1 = self.to_canvas_coords(point1.x, point1.y)
        x2, y2 = self.to_canvas_coords(point2.x, point2.y)
        x3, y3 = self.to_canvas_coords(point3.x, point3.y)

        self.create_line(x1, y1, x2, y2, width=2, fill=color)
        self.create_line(x2, y2, x3, y3, width=2, fill=color)
        self.create_line(x3, y3, x1, y1, width=2, fill=color)

    @staticmethod
    def get_nums_vertex(num_vertex: int):
        """
        Метод определит вершины для стороны, к которой будет проведена высота
        :param num_vertex: номер вершины, из которой будет проведена высота
        :return: три номера вершины по порядку
        """
        num_vertex -= 1  # для индексов

        if num_vertex == 0:
            return 0, 1, 2
        if num_vertex == 1:
            return 1, 0, 2
        if num_vertex == 2:
            return 2, 0, 1

    def draw_height(self, tri, num_vertex, canvas_ph: Point, color) -> None:
        """
        Метод отображает высоту треугольника,
        проведенную из вершины с номером num_vertex
        :param color: цвет высоты
        :param canvas_ph: точка пересечения высот треугольника
        :param tri: треугольник
        :param num_vertex: номер вершины
        :return: None
        """
        n, m, k = self.get_nums_vertex(num_vertex)
        # находим коэф-ты уравнения стороны, к которой проведем высоту
        a_side, b_side, c_side = Task.get_coef_side(tri[m], tri[k])
        # находим коэф-ты уравнения высоты по известным коэф-там стороны,
        # и вершины
        a_h, b_h, c_h = Task.get_coef_h((a_side, b_side, c_side), tri[n])
        # находим точку пересечения стороны и высоты
        x_p, y_p = Task.find_point_inters((a_side, b_side, c_side), (a_h, b_h, c_h))
        # переводим координаты в координаты холста
        canvas_x_p, canvas_y_p = self.to_canvas_coords(x_p, y_p)
        # строим высоту от точки пересечения высоты со стороной
        # до точки пересечения высот
        self.create_line(canvas_x_p, canvas_y_p, canvas_ph.x, canvas_ph.y,
                         width=2, fill=color)

    def draw_heights(self, tri, canvas_ph: Point, color) -> None:
        """
        Метод рисует все высоты треугольника
        :param color:
        :param tri: треугольник
        :param canvas_ph: точка пересечения высот треугольника
        :return: None
        """
        self.draw_height(tri, 1, canvas_ph, color)
        self.draw_height(tri, 2, canvas_ph, color)
        self.draw_height(tri, 3, canvas_ph, color)

    def get_solve(self) -> None:
        """
        Метод находит решение задачи
        :return: количество рассмотренных вариантов
        """

        # генерируются всевозможные валидные треугольники
        tri_s1 = Task.generate_triangles(self.task.set1)
        tri_s2 = Task.generate_triangles(self.task.set2)

        # найдем коэфф-ты для уравнения оси абсцисс (y = 0, A=C=0, By=0 => y=0)
        a_x, b_x, c_x = Task.get_coef_side(Point(0, 0), Point(1, 0))  # точки оси абсцисс

        for tri1 in tri_s1:
            for tri2 in tri_s2:
                self.task.save_count += 1
                # находит точки пересечения высот обоих треугольников
                ph1 = self.task.find_inters_heights(tri1)
                ph2 = self.task.find_inters_heights(tri2)

                # найдем коэффициенты прямой,
                # проходящей через точки пересечения высот двух треугольников
                a, b, c = Task.get_coef_side(ph1, ph2)

                # находим угол между прямыми
                angle = Task.find_angle((a, b, c), (a_x, b_x, c_x))

                # определяем минимальный угол
                if angle < self.task.save_min_ang:
                    self.task.save_min_ang = angle
                    self.task.save_tri1, self.task.save_tri2 = tri1, tri2
                    self.task.save_ph1, self.task.save_ph2 = ph1, ph2

    def error_processing(self) -> bool:
        """
        Метод обрабатывает возможные ошибки при получении решения задачи
        :return: True, если ошибок нет, False - иначе
        """

        if len(self.task.set1) == 0 and len(self.task.set2) == 0:
            text = "Плоскость пустая!\n" \
                   "Добавьте точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False
        elif len(self.task.set1) == 0:
            text = "На плоскости отсутствуют точки первого множества!\n" \
                   "Добавьте их, чтобы решить задачу!"
            messagebox.showwarning("", text)
            return False
        elif len(self.task.set2) == 0:
            text = "На плоскости отсутствуют точки второго множества!\n" \
                   "Добавьте их, чтобы решить задачу!"
            messagebox.showwarning("", text)
            return False
        elif 0 < len(self.task.set1) < 3 and 0 < len(self.task.set2) < 3:
            text = "Точек обеих множеств недостаточно для построения треугольников!\n" \
                   "Для построения треугольника нужно не менее 3-х точек каждого множества!\n" \
                   "Добавьте точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False
        elif len(self.task.set1) < 3:
            text = "Точек первого множества недостаточно для построения треугольника!\n" \
                   "Для построения треугольника нужно не менее 3-х точек!\n" \
                   "Добавьте точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False
        elif len(self.task.set2) < 3:
            text = "Точек второго множества недостаточно для построения треугольника!\n" \
                   "Для построения треугольника нужно не менее 3-х точек!\n" \
                   "Добавьте точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False

        tri_s1 = Task.generate_triangles(self.task.set1)
        tri_s2 = Task.generate_triangles(self.task.set2)

        if len(tri_s1) == 0 and len(tri_s2) == 0:
            text = "Точки каждого множества лежат на одной прямой!\n" \
                   "Добавьте других точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False
        elif len(tri_s1) == 0:
            text = "Точки первого множества лежат на одной прямой!\n" \
                   "Добавьте других точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False
        elif len(tri_s2) == 0:
            text = "Точки второго множества лежат на одной прямой!\n" \
                   "Добавьте других точек, чтобы получить решение задачи!"
            messagebox.showwarning("", text)
            return False

        return True

    def draw_solve(self) -> None:
        """
        Функция отображает найденное перебором решение
        :return:
        """
        if not self.error_processing():
            return

        self.get_solve()

        # # отображаю точки пересечения высот
        self.draw_point(self.task.save_ph1.x, self.task.save_ph1.y, DARKCYAN)
        self.draw_point(self.task.save_ph2.x, self.task.save_ph2.y, DARKCYAN)

        # получаю координаты холста
        # для точек пересечения высот найденных треугольников
        canvas_x_ph1, canvas_y_ph1 = self.to_canvas_coords(self.task.save_ph1.x, self.task.save_ph1.y)
        canvas_x_ph2, canvas_y_ph2 = self.to_canvas_coords(self.task.save_ph2.x, self.task.save_ph2.y)

        # отображаю найденные треугольники
        self.draw_triangle(self.task.save_tri1[0], self.task.save_tri1[1], self.task.save_tri1[2], BLUE)
        self.draw_triangle(self.task.save_tri2[0], self.task.save_tri2[1], self.task.save_tri2[2], RED)

        # отображаю прямую,
        # соединяющую точку пересечения высот 2-х треугольников
        self.create_line(canvas_x_ph1, canvas_y_ph1, canvas_x_ph2, canvas_y_ph2, width=2, fill=DARKCYAN)

        # первый треугольник
        # ---------------------------------------------------------------------
        self.draw_heights(self.task.save_tri1, Point(canvas_x_ph1, canvas_y_ph1), GREEN)

        # второй треугольник
        # ---------------------------------------------------------------------
        self.draw_heights(self.task.save_tri2, Point(canvas_x_ph2, canvas_y_ph2), GREEN)

        self.text_solve()

    def text_solve(self) -> None:
        """
        Метод отображает результаты в текстовом формате
        :return: None
        """

        win = tk.Toplevel()
        win.grab_set()
        win.geometry("800x300")
        textbox = tk.Text(win, width=60, height=11, state=tk.DISABLED, borderwidth=5,
                          wrap="word", font=("Courier New", 14), fg=BLACK, bg=Aquamarine)
        textbox.pack()

        text = f"Всего было рассмотрено {self.task.save_count} вариантов\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("1.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Треугольник первого множества был построен на след. точках:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("2.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"1.({round(self.task.save_tri1[0].x, 2)};{round(self.task.save_tri1[0].y, 2)}), " \
               f"2.({round(self.task.save_tri1[1].x, 2)};{round(self.task.save_tri1[1].y, 2)})," \
               f"3.({round(self.task.save_tri1[2].x, 2)};{round(self.task.save_tri1[2].y, 2)})\n"

        textbox.config(state=tk.NORMAL)
        textbox.insert("3.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Треугольник второго множества был построен на след. точках:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("4.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"1.({round(self.task.save_tri2[0].x, 2)};{round(self.task.save_tri2[0].x, 2)}), " \
               f"2.({round(self.task.save_tri2[1].x, 2)};{round(self.task.save_tri2[1].x, 2)})," \
               f"3.({round(self.task.save_tri2[2].x, 2)};{round(self.task.save_tri2[2].x, 2)})\n"

        textbox.config(state=tk.NORMAL)
        textbox.insert("5.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Точки пересечения высот имеют след. координаты:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("6.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"1.({round(self.task.save_ph1.x, 2)};{round(self.task.save_ph1.y, 2)}), " \
               f"2.({round(self.task.save_ph2.x, 2)};{round(self.task.save_ph2.y, 2)})\n"

        textbox.config(state=tk.NORMAL)
        textbox.insert("7.0", text)
        textbox.config(state=tk.DISABLED)

        text = "Искомое минимальное значение угла между прямой,\n" \
               "соединяющей точки пересечения высот 2-х треугольников, и осью абсцисс:\n"
        textbox.config(state=tk.NORMAL)
        textbox.insert("8.0", text)
        textbox.config(state=tk.DISABLED)

        text = f"angle = {round(self.task.save_min_ang, 3)} градуса"
        textbox.config(state=tk.NORMAL)
        textbox.insert("11.0", text)
        textbox.config(state=tk.DISABLED)
