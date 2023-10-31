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
