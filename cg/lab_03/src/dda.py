from PointClass import *


class Dda:
    """
    Класс для построения линии алгоритмом
    цифрового дифференциального анализатора
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

    def get_points_for_line(self, color_line, color_bg):
        """
        Метод получает массив точек для отрисовки линии
        """
        # очищаем список, если уже строили
        self.points.clear()

        # определили длины линии по осям координат
        dx = abs(self.point2.x - self.point1.x)
        dy = abs(self.point2.y - self.point1.y)

        # определили наибольшее изменение по осям
        length = dx if dx > dy else dy

        # вычислили приращение для каждой координаты
        delta_x = (self.point2.x - self.point1.x) / length
        delta_y = (self.point2.y - self.point1.y) / length

        # начальные значения
        x = self.point1.x
        y = self.point1.y

        for _ in range(int(length) + 1):  # правильный диапазон
            # print(f"Dda: x = {round(x)}, y = {round(y)}")

            if not self.stepmode:
                self.points.append(Point(round(x), round(y), color_line))
            elif round(x + delta_x) != round(x) and round(y + delta_y) != round(y):
                # тип если ступенька?
                self.steps += 1
                
            x += delta_x
            y += delta_y

        if self.stepmode:
            return self.steps

        return self.points
