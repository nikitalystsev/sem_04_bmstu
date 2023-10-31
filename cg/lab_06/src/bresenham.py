from PointClass import Point


def sign(arg):
    """
    Функция определяет знак переданного числа
    """

    return 1 if arg > 0 else -1 if arg < 0 else 0


class BresenhamFloat:
    """
    Класс алгоритма Брезенхема с действительными значениями
    """

    def __init__(self, point1: Point, point2: Point, stepmode: bool = False):
        """
        Инициализация атрибутов класса
        """
        self.point1: Point = point1
        self.point2: Point = point2
        self.stepmode = stepmode
        self.steps = 0
        self.points: list[Point] = list()

    def get_points_for_line(self, color_line):
        """
        Метод получает массив точек для отрисовки линии
        """
        # флаг обмена приращений (пока не меняли)
        exchange = False

        # очищаем список, если уже строили
        self.points.clear()

        # определили длины линии по осям координат
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y

        # определили знак приращений по осям
        sx, sy = sign(dx), sign(dy)

        dx, dy = abs(dx), abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            exchange = True

        # понятие ошибки
        m = dy / dx  # тангенс угла наклона отрезка
        # удобнее анализировать знак ошибки, так истинное значение ошибки смещается на -0,5
        e = m - 0.5

        # начальные значения
        x = self.point1.x
        y = self.point1.y

        # для подсчета количества ступенек
        xb = x
        yb = y

        for _ in range(round(dx) + 1):  # правильный диапазон
            # print(f"Bres_float: x = {x}, y = {y}")
            if not self.stepmode:
                self.points.append(Point(x, y, color_line))

            if e >= 0:
                if not exchange:
                    y += sy
                else:
                    x += sx

                e -= 1  # отличие

            if not exchange:
                x += sx
            else:
                y += sy

            e += m  # отличие

            if self.stepmode:
                if xb != x and yb != y:
                    self.steps += 1
                xb = x
                yb = y

        if self.stepmode:
            return self.steps

        return self.points


class BresenhamEllipse:
    """
    Класс алгоритма Брезенхема для построения эллипса
    1/4 части
    """

    def __init__(
            self,
            point_center: Point,  # центр эллипса
            a: int | float,  # большая полуось
            b: int | float,  # малая полуось
    ):
        """
        Инициализация атрибутов класса
        """
        self._point_center: Point = point_center
        self._a: int | float = a
        self._b: int | float = b

    def __get_symmetrical_points(self, point: Point, color: str) -> list[Point]:
        """
        Метод позволяет получить симметричные данной точке точки
        """
        x_c, y_c = self._point_center.x, self._point_center.y
        x, y = point.x, point.y

        list_point = list()

        list_point.append(Point(x=x, y=y, color=color))
        list_point.append(Point(x=(-x + 2 * x_c), y=y, color=color))
        list_point.append(Point(x=x, y=(-y + 2 * y_c), color=color))
        list_point.append(Point(x=(-x + 2 * x_c), y=(-y + 2 * y_c), color=color))

        return list_point

    def create_ellipse(self, color: str) -> list[Point]:
        """
        Метод для отображения эллипса
        """
        x_c, y_c = self._point_center.x, self._point_center.y

        x, y = 0, self._b

        points = list()

        point = Point(x=(x_c + x), y=(y_c + y), color=color)

        list_points = self.__get_symmetrical_points(point, color)
        points.extend(list_points)

        a_squared, b_squared = self._a ** 2, self._b ** 2
        delta_i = b_squared - a_squared * (2 * self._b + 1)

        while y >= 0:
            if delta_i < 0:
                d1 = 2 * delta_i + a_squared * (2 * y + 2)
                x += 1
                if d1 < 0:
                    delta_i += b_squared * (2 * x + 1)
                else:
                    y -= 1
                    delta_i += b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)
            elif delta_i > 0:
                d2 = 2 * delta_i + b_squared * (2 - 2 * x)
                y -= 1
                if d2 > 0:
                    delta_i += a_squared * (1 - 2 * y)
                else:
                    x += 1
                    delta_i += b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)
            else:
                x += 1
                y -= 1
                delta_i += b_squared * (2 * x + 1) + a_squared * (1 - 2 * y)

            point = Point(x=(x_c + x), y=(y_c + y), color=color)

            list_points = self.__get_symmetrical_points(point, color)
            points.extend(list_points)

        return points
