import read as read
import print_data as print_data
import tasks as tasks

SIZE = 75


def main():
    """
    Главная функция
    :return:
    """

    filename = "../data/data2.txt"

    print("\n" + SIZE * "-")

    points = read.read_table(filename)

    print("Считанная таблица:")
    print_data.print_table(points)
    n = read.read_degree()
    x = read.read_x()

    table_value = tasks.get_table_value(x, points)
    print_data.print_table_value(table_value, x)

    if tasks.is_change_sign(points):
        root_newton, root_hermit = tasks.get_root(points, n)
        print_data.print_root(points, root_newton, root_hermit, n)
    else:
        print("Функция не имеет корней!")

    root_system_x, root_system_y = tasks.get_system_root(n)
    print_data.print_system_root(root_system_x, root_system_y, n)

    print("\n" + SIZE * "-")


if __name__ == "__main__":
    main()
