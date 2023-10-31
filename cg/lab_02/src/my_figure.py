import math as m
import numpy as np
import copy as cp


class Point:
    """
    Точка
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        Инициализация атрибутов класса
        """
        self.x = x
        self.y = y


class MyFigure:
    """
    Фигура по заданию
    """

    def __init__(self, a=1.26, b=0.63, center_ellipse=(2.52, 0), x_line_inters=0):  # значения по умолчанию
        """
        Инициализация атрибутов класса
        """
        self.a = a
        self.b = b
        self.center_ellipse = Point(*center_ellipse)
        self.flash_point = Point(x_line_inters, center_ellipse[1])
        self.point1 = Point(center_ellipse[0], center_ellipse[1] + self.a)
        self.point2 = Point(center_ellipse[0], center_ellipse[1] - self.a)
        self.angle = m.radians(0)  # в радианах
        self.center_figure = self.get_center_figure()

    def update_param_figure(self, x_inters: float):
        """
        Метод изменяет не вводимые параметры фигуры
        """
        self.flash_point = Point(x_inters, self.center_ellipse.y)
        self.point1 = Point(self.center_ellipse.x, self.center_ellipse.y + self.a)
        self.point2 = Point(self.center_ellipse.x, self.center_ellipse.y - self.a)
        self.angle = m.radians(0)  # в радианах
        self.center_figure = self.get_center_figure()

    def get_center_figure(self):
        """
        Метод определяет центральную точку фигуры
        """
        x_c = (self.flash_point.x + self.center_ellipse.x + self.b * m.cos(self.angle)) / 2
        y_c = (self.flash_point.y + self.center_ellipse.y + self.b * m.sin(self.angle)) / 2

        return Point(x=x_c, y=y_c)

    @staticmethod
    def apply_transform(point: Point, matrix) -> Point:
        """
        Метод применяет операцию к точке
        """
        # преобразуем точку в однородные координаты
        point = np.array([point.x, point.y, 1])
        transformed_point = np.matmul(matrix, point)  # умножаем точку на матрицу
        # преобразуем точку из однородных координат в декартовы координаты
        transformed_point = transformed_point[:2] / transformed_point[2]

        return Point(transformed_point[0], transformed_point[1])

    def rotate_figure(self, center_rotate: Point, angle: float):
        """
        Метод поворачивает фигуру
        x' = dx * cos(theta) - dy * sin(theta)
        y' = dx * sin(theta) + dy * cos(theta),
        где dx = x - xc, dy = y - yc
                        ( cos(angle) -sin(angle)  0 )
        rotate_matrix = ( sin(angle)  cos(angle)  0 )
                        (     0           0       1 )
        Используем афинные преобразования:
        Сначала перенос центра поворота в начало координат,
        потом поворот,
        потом возвращение центра поворота обратно
        Этот метод позволяет сохранить пропорции объекта при повороте для любого центра поворота
        """
        # определяем координаты центра поворота
        xc, yc = center_rotate.x, center_rotate.y

        # ввиду непонятных для меня обстоятельств нужно менять знаки у центров
        xc, yc = -xc, -yc

        # переводим угол в радианы
        radians_angle = m.radians(angle)

        # записываем последовательно матрицы в порядке их применимости
        transfer_matrix = np.array([[1, 0, -xc], [0, 1, -yc], [0, 0, 1]])
        rotate_matrix = np.array([[m.cos(radians_angle), -m.sin(radians_angle), 0],
                                  [m.sin(radians_angle), m.cos(radians_angle), 0],
                                  [0, 0, 1]])
        reverse_transfer_matrix = np.array([[1, 0, xc], [0, 1, yc], [0, 0, 1]])

        # получаем результирующую матрицу операции
        result_matrix = np.matmul(transfer_matrix, rotate_matrix)
        result_matrix = np.matmul(result_matrix, reverse_transfer_matrix)

        # применяем марицу операции к точкам
        self.flash_point = MyFigure.apply_transform(self.flash_point, result_matrix)
        self.point1 = MyFigure.apply_transform(self.point1, result_matrix)
        self.point2 = MyFigure.apply_transform(self.point2, result_matrix)

        self.center_ellipse = MyFigure.apply_transform(self.center_ellipse, result_matrix)
        self.angle += radians_angle

        self.center_figure = self.get_center_figure()

    def transfer_figure(self, dx: float, dy: float):
        """
        Метод переносит фигуру
        """
        # составляет матрицу переноса
        transfer_matrix = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

        # применяем матрицу переноса ко всем точкам фигуры
        self.flash_point = MyFigure.apply_transform(self.flash_point, transfer_matrix)
        self.point1 = MyFigure.apply_transform(self.point1, transfer_matrix)
        self.point2 = MyFigure.apply_transform(self.point2, transfer_matrix)
        self.center_ellipse = MyFigure.apply_transform(self.center_ellipse, transfer_matrix)

        self.center_figure = self.get_center_figure()

    def scaling_figure(self, kx, ky, xc, yc):
        """
        Метод масштабирует фигуру
        """
        # составляем матрицу масштабирования,
        # которая масштабирует относительно начала координат,
        # поэтому необходимо для каждой вычисляемой точки добавлять слагаемое
        scaling_matrix = np.array([[kx, 0, 0], [0, ky, 0], [0, 0, 1]])
        # то самое слагаемое
        x_term, y_term = (1 - kx) * xc, (1 - ky) * yc

        # применяем матрицу масштабирования ко всем вычисляемым точкам
        # и прибавляем то самое слагаемое, учитывающее произвольный центр масштабирования
        self.flash_point = MyFigure.apply_transform(self.flash_point, scaling_matrix)
        self.flash_point.x += x_term
        self.flash_point.y += y_term

        self.point1 = MyFigure.apply_transform(self.point1, scaling_matrix)
        self.point1.x += x_term
        self.point1.y += y_term

        self.point2 = MyFigure.apply_transform(self.point2, scaling_matrix)
        self.point2.x += x_term
        self.point2.y += y_term

        self.center_ellipse = MyFigure.apply_transform(self.center_ellipse, scaling_matrix)
        self.center_ellipse.x += x_term
        self.center_ellipse.y += y_term

        # также масштабируем значения полуосей
        self.a *= ky
        self.b *= kx

        self.center_figure = self.get_center_figure()


class StateHistory:
    """
    История состояний фигуры
    """

    def __init__(self):
        self.state_history = []

    def add_state(self, figure: MyFigure) -> None:
        """
        Метод добавляет состояние в историю состояний
        """
        copy_figure = cp.deepcopy(figure)
        self.state_history.append(copy_figure)
