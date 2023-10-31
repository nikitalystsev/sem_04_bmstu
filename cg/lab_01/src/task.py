import math as m

EPS = 1e-9


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

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y


class Task:
    """
    Параметры задачи
    """

    def __init__(self):
        self.set1 = []
        self.set2 = []
        self.inters_h = []
        self.save_tri1 = []
        self.save_tri2 = []
        self.save_min_ang = float("inf")
        self.save_ph1 = None
        self.save_ph2 = None
        self.save_count = 0

    def default_save_param(self) -> None:
        """
        Метод приводит значения параметров задачи к начальным
        :return: None
        """
        self.save_tri1 = []
        self.save_tri2 = []
        self.save_min_ang = float("inf")
        self.save_ph1 = None
        self.save_ph2 = None
        self.save_count = 0

    @staticmethod
    def generate_triangles(points: list[Point]):
        triangles = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                for k in range(j + 1, len(points)):
                    x1, y1 = points[i].x, points[i].y
                    x2, y2 = points[j].x, points[j].y
                    x3, y3 = points[k].x, points[k].y
                    # если точки не лежат на одной прямой (соотношение 3)
                    if (x2 - x1) * (y3 - y1) != (x3 - x1) * (y2 - y1):
                        triangles.append((points[i], points[j], points[k]))
        return triangles

    # уравнение прямой, проходящей через 2 точки (соотношение 7):
    # A*X+B*Y+C=0, где A=Y1-Y2, B=X2-X1, C=(X1-X2)*Y1+(Y2-Y1)*X1

    # Уравнение прямой, перпендикулярной рассматриваемому отрезку и проходящей
    # через точку (Xc,Yc), имеет вид -B*X+A*Y+D=0,
    # где D=B*Xc-A*Yc (соотношение 8)

    # система уравнений для нахождения точки пересечения 2-х прямых:
    # A1*X+B1*Y+C1=0 - уравнение первой прямой
    # A2*X+B2*Y+C2=0 - уравнение второй прямой
    # A1,A2,B1,B2,C1,C2 - известные коэффициенты
    # уравнений соответствующих прямых

    # Пусть заданы две прямые общими уравнениями:
    # A1*X+B1*Y+C1=0 - уравнение первой прямой
    # A2*X+B2*Y+C2=0 - уравнение второй прямой
    # Угол между прямыми определяется след. образом:
    # tg(w)=(A1*B2-A2*B1)/(A1*A2+B1*B2)

    @staticmethod
    def get_coef_side(point1: Point, point2: Point) -> (float, float, float):
        """
        Метод позволяет определить коэффициенты уравнения стороны треугольника,
        к которой перпендикулярна высота используя соотношение 7
        :param point1: первая точка
        :param point2: вторая точка
        :return: Коэффициенты
        """
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y

        a = y1 - y2
        b = x2 - x1
        c = (x1 - x2) * y1 + (y2 - y1) * x1

        return a, b, c

    @staticmethod
    def get_coef_h(coef_side_tri, point: Point) -> (float, float, float):
        """
        Метод позволяет определить коэффициенты уравнения высоты по известным
        коэффициентам уравнения стороны треугольника и известным координатам
        вершины треугольника используя соотношение 8
        :param coef_side_tri: коэф-ты ур-я стороны треугольника
        :param point: вершина треугольника
        :return: коэффициенты
        """
        a_side, b_side, c_side = coef_side_tri
        x_c, y_c = point.x, point.y

        b = -b_side
        a = a_side
        d = b_side * x_c - a_side * y_c

        return b, a, d

    @staticmethod
    def find_point_inters(line1, line2) -> (float, float):
        """
        Метод находит точку пересечения 2-х прямых
        :param line1: коэф-ты первой прямой
        :param line2: коэф-ты второй прямой
        :return: точка пересечения
        """
        a1, b1, c1 = line1
        a2, b2, c2 = line2

        x_p = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1)
        y_p = (c1 * a2 - c2 * a1) / (a1 * b2 - a2 * b1)

        return x_p, y_p

    @staticmethod
    def find_inters_heights(tri) -> Point:
        """
        Метод обрабатывает треугольник
        :param tri: треугольник
        :return:
        """
        # находим коэф-ты уравнения стороны, к которой проведем высоту
        a_side1, b_side1, c_side1 = Task.get_coef_side(tri[0], tri[1])
        # находим коэф-ты уравнения высоты по известным коэф-там стороны,
        # и вершины
        a_h1, b_h1, c_h1 = Task.get_coef_h((a_side1, b_side1, c_side1), tri[2])

        a_side2, b_side2, c_side2 = Task.get_coef_side(tri[1], tri[2])
        a_h2, b_h2, c_h2 = Task.get_coef_h((a_side2, b_side2, c_side2), tri[0])

        # находим точку пересечения высот треугольника
        x_ph, y_ph = Task.find_point_inters((a_h1, b_h1, c_h1), (a_h2, b_h2, c_h2))

        return Point(x_ph, y_ph)

    @staticmethod
    def find_angle(line1, line2):
        """
        Метод находит угол между двумя прямыми
        :param line1: первая прямая
        :param line2: вторая прямая
        :return: угол в градусах
        """
        a1, b1, c1 = line1
        a2, b2, c2 = line2

        if m.fabs(a1 * a2 - b1 * b2) < EPS:
            return 90

        tg_w = (a1 * b2 - a2 * b1) / (a1 * a2 - b1 * b2)

        angle = m.atan(tg_w)
        angle_degrees = m.degrees(angle)

        if angle_degrees < 0:
            angle_degrees += 180
        elif m.fabs(angle_degrees) < EPS:
            angle_degrees = 0

        return angle_degrees
