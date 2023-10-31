import math as m
import copy as cp


EPS = 1e-9


def float_equal(a, b):
    """
    Функция сравнивает числа с плавающей запятой
    """
    return m.fabs(a - b) < EPS


def get_table_value_for_x(points, x):
    """
    Функция ищет ближайшее к x табличное значение
    :param points: считанный список точек
    :param x: точка интерполирования
    :return: индекс ближайшей к x табличной точки
    """
    diff = m.fabs(x - points[0].x)

    index = 0

    for ind, val in enumerate(points):
        if m.fabs(x - val.x) < diff:
            diff = m.fabs(x - val.x)
            index = ind

    return index


def collect_config(points, x, n):
    """
    Функция собирает конфигурацию
    :param points: считанный список точек
    :param x: точка интерполирования
    :param n: степень полинома
    :return: список точек конфигурации
    """
    index = get_table_value_for_x(points, x)

    left = right = index

    for i in range(n):
        if i % 2 == 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(points) - 1:
                left -= 1
            else:
                right += 1

    return points[left:right + 1]


def get_points_for_hermite(config_points):
    """
    Функция получает таблицу точек для полинома Эрмита
    :param config_points: список точек конфигурации
    :return: список точек конфигурации для полинома Эрмита
    """
    new_table = []

    for point in config_points:
        multiplicity = 2  # кратность узла
        for i in range(multiplicity):
            tmp_point = cp.deepcopy(point)
            new_table.append(tmp_point)

    return new_table


def get_diff_table(config_points):
    """
    Функция получает таблицу разделенных разностей
    для полиномов Ньютона или Эрмита
    :param config_points: список точек конфигурации
    :return: матрица - таблица разделенных разностей
    """
    count_points = len(config_points)

    diff_table = [[0] * count_points for _ in range(count_points)]

    for i in range(count_points):
        diff_table[i][0] = config_points[i].y

    for i in range(1, count_points):
        for j in range(i, count_points):
            if not float_equal(config_points[j].x, config_points[j - i].x):
                diff_table[j][i] = \
                    (diff_table[j][i - 1] - diff_table[j - 1][i - 1]) / \
                    (config_points[j].x - config_points[j - i].x)
            else:
                diff_table[j][i] = config_points[j].derivative

    return diff_table


def get_diagonal(diff_table):
    """
    Функция получает нужные разделенные разности
    (находятся на главной диагонали)
    :param diff_table: матрица разделенных разностей
    :return: список нужных разностей
    """
    diagonal = []

    for i in range(len(diff_table)):
        diagonal.append(diff_table[i][i])

    return diagonal


def polynom(config_points, x, n):
    """
    Функция строит полином Ньютона или Эрмита 
    и вычисляет значение при фиксированном x
    :param config_points: список точек конфигурации
    :param x: точка интерполирования
    :param n: степень полинома
    :return: значение функции при x
    """
    diff_table = get_diff_table(config_points)

    diff = get_diagonal(diff_table)

    result = diff[0]

    for i in range(1, len(diff)):
        p = diff[i]
        for j in range(i):
            p *= (x - config_points[j].x)
        result += p

    return result
