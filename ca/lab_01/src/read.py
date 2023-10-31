import point as point


def read_table(filename):
    """
    Функция считывает таблицу из текстового файла
    """
    points = []

    with open(filename) as file:
        for line in file:
            data = list(map(float, line.split()))
            dot = point.Point(data[0], data[1], data[2])
            points.append(dot)

    return points


def read_degree():
    """
    Функция считывает введенную с клавиатуры степень полинома
    """
    degree = int(input("Введите степень n аппроксимирующих полиномов: "))

    return degree


def read_x():
    """
    Функция считывает значение аргумента x, для которого выполняется интерполяция
    """
    x = float(input("Введите значение аргумента x, для которого выполняется интерполяция: "))

    return x


def read_system_table(filename):
    """
    Функция считывает таблицу из текстового файла
    :param filename: путь до файла
    :return: таблицу
    """
    points = []

    with open(filename) as file:
        for line in file:
            data = list(map(float, line.split()))
            dot = point.Point(data[0], data[1], 0)
            points.append(dot)

    return points
