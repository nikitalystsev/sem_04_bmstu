import interpolation as interpolation
import print_data as print_data
import read as read
import copy as cp
import point as point

SIZE_TABLE = 53


def get_table_value(x, points):
    """
    Функция получает таблицу значений при разных степенях полиномов
    и при фиксированном x
    :param x: точка интерполирования
    :param points: считанный список точек
    :return: таблица значений
    """
    table_value = []

    for i in range(1, 6):
        config_points = interpolation.collect_config(points, x, i)
        result_newton = interpolation.polynom(config_points, x, i)
        config_points = interpolation.get_points_for_hermite(config_points)
        result_hermit = interpolation.polynom(config_points, x, i)

        table_value.append([i, result_newton, result_hermit])

    return table_value


#####################################################################################################

def is_change_sign(points) -> bool:
    """
    Факт наличия корня у функции устанавливается по наличию 
    смены знака у функции при продвижении по строкам таблицы
    :param points: считанный список точек
    :return: True - знак меняется, False в противном случае
    """
    prev = points[0].y

    for dot in points:
        cur = dot.y
        if prev * cur < 0:
            return True
        prev = cur

    return False


def swap_abscissa_ordinate(points):
    """
    Функция меняет местами столбцы с аргументом функции и ее значением
    :param points: считанный список точек
    :return: преобразованный список точек
    """
    tmp_points = cp.deepcopy(points)

    for i in range(len(tmp_points)):
        tmp_points[i].x, tmp_points[i].y = tmp_points[i].y, tmp_points[i].x

    return tmp_points


def get_newton_root(points, n):
    """
    Функция вычисляет корень табличной функции с
    помощью обратной интерполяции полинома Ньютона
    :param points: считанный список точек
    :param n: степень полинома
    :return: корень функции
    """
    tmp_points = cp.deepcopy(points)

    tmp_points = swap_abscissa_ordinate(tmp_points)

    tmp_points.sort(key=lambda dot: dot.y)

    tmp_points = interpolation.collect_config(tmp_points, 0, n)

    root = interpolation.polynom(tmp_points, 0, n)

    return root


def get_hermit_root(points, n):
    """
    Функция вычисляет корень табличной функции с
    помощью обратной интерполяции полинома Эрмита
    :param points: считанный список точек
    :param n: степень полинома
    :return: корень функции
    """
    tmp_points = cp.deepcopy(points)

    tmp_points = interpolation.collect_config(tmp_points, 0, n)
    tmp_points = interpolation.get_points_for_hermite(tmp_points)
    print_data.print_table(tmp_points)
    tmp_points = swap_abscissa_ordinate(tmp_points)

    for dot in tmp_points:
        if not interpolation.float_equal(dot.derivative, 0):
            dot.derivative = 1 / dot.derivative
        else:
            dot.derivative = 0

    tmp_points.sort(key=lambda t: t.y)

    root = interpolation.polynom(tmp_points, 0, n)

    return root


def get_root(points, n):
    """
    Функция вычисляет корень таблично заданной функции
    :param points: считанный список точек
    :param n: степень полинома
    :return: корень
    """
    newton_points = cp.deepcopy(points)
    hermit_points = cp.deepcopy(points)

    root_newton = get_newton_root(newton_points, n)
    root_hermit = get_hermit_root(hermit_points, n)

    return root_newton, root_hermit

#####################################################################################################


# С помощью интерполяции перестроить приведенные табличные представления
# функций к новой таблице, в которой содержится зависимость разности функций y(x) из
# (1) и (2) от фиксированного набора значений аргумента x, например, такого, как во второй
# таблице, или любого другого из рассматриваемого интервала. Затем применить процедуру
# обратной интерполяции.

# выбираем множество Х для двух функций (удобно взять Х-сы их 2-й таблицы, поскольку Y для них известны)
# Чтобы найти разность Y тебе нужно из значений Y второй таблицы
# вычесть значения Y из первой таблицы, но с помощью интерполяции в тех же x

def change_table(points1, points2, n):
    """
    Функция в первой таблице изменяет с помощью интерполяции
    ординаты в соответствии с абсциссами второй таблицы
    :param points1: первая таблица точек
    :param points2: вторая таблица точек
    :param n: степень полинома
    :return: новую первую таблицу
    """
    new_points1 = []

    for i in range(len(points2)):
        tmp_points = cp.deepcopy(points1)

        tmp_points = interpolation.collect_config(tmp_points, points2[i].x, n)
        result_newton = interpolation.polynom(tmp_points, points2[i].x, n)

        new_points1.append(point.Point(points1[i].x, result_newton, 0))

    return new_points1


def get_subtract_table(points1, points2):
    """
    Функция получает новую таблицу, в которой содержится зависимость разности функций y(x) из
    (1) и (2) от фиксированного набора значений аргумента из второй таблицы
    :param points1: первая уже измененная ранее таблица точек
    :param points2: вторая таблицы точек
    :return: таблица разностей функций y(x)
    """
    subtract_table = []

    for i in range(len(points2)):
        subtract_table.append(point.Point(points2[i].x, - points2[i].y + points1[i].y, 0))

    return subtract_table


def get_system_root(n):
    """
    Функция находит корень системы
    :param n: степень полинома Ньютона
    :return: корень
    """

    points1 = read.read_system_table("../data/system1.txt")

    # print("Первая считанная таблица X(Y):")
    # print_data.print_table(points1)

    points2 = read.read_system_table("../data/system2.txt")

    # смена столбцов
    points1 = swap_abscissa_ordinate(points1)

    print("Первая считанная таблица Y(X):")
    print_data.print_table(points1)

    print("Вторая считанная таблица Y(X):")
    print_data.print_table(points2)

    # степень полинома len(points1) - 1, поскольку нужно, чтобы все точки участвовали в интерполяции
    points1 = change_table(points1, points2, len(points1) - 1)

    print("Интерполированная первая таблица (Ординаты интерполированы для абсцисс второй таблицы):")
    print_data.print_table(points1)

    table = get_subtract_table(points1, points2)

    print("Таблица с разностями абсцисс двух таблиц и ординат второй таблицы")
    print_data.print_table(table)

    root_x = get_newton_root(table, n)

    tmp_points2 = cp.deepcopy(points2)

    config_points2 = interpolation.collect_config(tmp_points2, root_x, n)

    root_y = interpolation.polynom(config_points2, root_x, n)

    return root_x, root_y
