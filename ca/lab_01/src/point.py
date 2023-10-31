class Point(object):
    """
    Точка
    """
    def __init__(self, x=0, y=0, derivative=0):
        """
        Инициализация атрибутов
        :param x: абсцисса точки
        :param y: ордината точки
        :param derivative: значение производной в точке
        """
        self.x = x
        self.y = y
        self.derivative = derivative

