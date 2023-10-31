#include <iostream>
#include <string>
#include <concepts>
#include "Matrix.hpp"

using string = std::string;
using namespace std;

int main()
{
    std::cout << "Тестирование конструкторов создания матрицы:\n\n";

    // Matrix<float> matrix1; нельзя
    Matrix<int> matrix2(2, 2);
    Matrix<int> matrix3(2, 3, 5); // филлером

    int **m = new int *[2];
    for (int i = 0; i < 2; ++i)
    {
        m[i] = new int[2];
        for (int j = 0; j < 2; ++j)
            m[i][j] = i + j;
    }
    Matrix<int> matrix4{2, 2, m}; // на основе си-матрицы

    for (int i = 0; i < 2; ++i)
        delete[] m[i];
    delete[] m;

    Matrix<float> matrix5({{1, 2, 3},
                           {4, 5, 6},
                           {7, 8, 9}}); // список инициализации

    cout << "matrix3\n";
    cout << matrix3 << "\n\n";
    for (auto &x : matrix3)
        std::cout << x << ' ';

    cout << "\nmatrix5\n";
    cout << matrix5 << "\n\n";
    Matrix<float>::const_reverse_iterator rit = matrix5.rcbegin();

    // Итерация по вектору в прямом порядке
    for (; rit != matrix5.rcend(); ++rit)
        std::cout << *rit << " ";

    Matrix<string> matrix6(2, 2, "hello");
    Matrix<string> matrix7(2, 2, "bye");

    Matrix<string> matrix_new(matrix7);

    // std::cout << "\n-matrix7:\n"
    //           << -matrix7 << "\n\n";m

    std::cout << "\n-matrix5:\n"
              << -matrix5 << "\n\n";

    std::cout << "\nmatrix7:\n"
              << matrix7 << "\n\n";

    matrix7 = matrix6;

    std::cout << "matrix7:\n"
              << matrix7 << "\n\n";

    std::cout << "Проверка булевых операторов == и !=:\n";
    if (matrix4 != matrix5)
        std::cout << "матрицы не равны"
                  << "\n\n";
    else
        std::cout << "матрицы равны"
                  << "\n\n";

    matrix5 += matrix5 + 1.2;

    matrix5 -= matrix5 - 1.2;

    matrix5 -= matrix5 - 1.2;

    matrix5 *= 4 + matrix5;

    cout << matrix5.determinant() << endl;
    cout << matrix5.identity() << endl;

    // cout << matrix3.determinant() << endl;
    // cout << matrix3.identity() << endl;

    Matrix<int> matrix8{{1, 2, 6}, {3, 4, 5}};
    Matrix<float> matrix9{{1.3, 24, 6.0}, {3, 414, 5}};

    std::cout << "matrix8:\n"
              << matrix8 << "\n\n";
    std::cout << "matrix9:\n"
              << matrix9 << "\n\n";

    std::cout << "Сложение матрицы float и int:\n";
    std::cout << "sum matrix:\n"
              << matrix9 + matrix8 << "\n\n";

    Matrix<float> matrix10(matrix3);

    for (auto &x : matrix10)
        std::cout << x << ' ';

    try
    {
        std::cout << "Матрица с отрицательными количеством строк:\n";
        Matrix<int> err_m(-1, 2);
    }
    catch (MatrixExceptions &err)
    {
        std::cerr << err.what() << "\n\n";
    }

    size_t row = 2, col = 3;
    std::cout << "Конструктор с двумя числами типа size_t:\n";
    Matrix<int> my_matrix(row, col, 4);
    std::cout << my_matrix << "\n\n";

    const size_t a = 2;
    const size_t b = 2;
    // const size_t c = 3;

    std::cout << "Проверка конструктора для списка инициализации:\n";
    Matrix<int> my_matrix3(a, b);
    // std::cout << my_matrix3 << "\n\n";
    Matrix<int> my_matrix4({{1, 2, 3},
                            {4, 5, 6}});
    std::cout << "Проверка булевых операторов == и !=:\n";
    if (my_matrix4 != my_matrix3)
        std::cout << "матрицы не равны"
                  << "\n\n";
    else
        std::cout << "матрицы равны"
                  << "\n\n";

    std::cout << "Получение элемента матрицы:\n\n";
    Matrix<string> matrix11 = {{"a1", "a2", "a3"},
                               {"b1", "b2", "b3"},
                               {"c1", "c2", "c3"}};
    std::cout << "matrix11: \n"
              << matrix11 << "\n\n";

    std::cout << "matrix11[1][1] and matrix11.get_elem(1, 1)\n";
    std::cout << matrix11[1][1] << " and " << matrix11.get_elem(1, 1) << "\n\n";

    std::cout << "new_matrix[1][1] = new1 and new_matrix.get_elem(1, 2) = new2\n";
    matrix11[1][1] = "hello";
    matrix11.get_elem(1, 2) = "hello";
    std::cout << "matrix11[1][1] = " << matrix11[1][1] << ", matrix11[1][2] = " << matrix11[1][2] << "\n\n";

    std::cout << "Элементы матрицы matrix11:\n";
    for (const auto &elem : matrix11)
        std::cout << elem << ' ';
    std::cout << "\n\n";

    std::cout << "Проверка определителя матрицы:\n\n";
    Matrix<double> matrix12 = {
        {2, -1, 0}, {0, 2, -1}, {-1, -1, 1}};

    std::cout << "matrix12:\n"
              << matrix12 << "\n\n";

    std::cout << "inverse:\n"
              << matrix12.inverse() << "\n\n";

    // std::cout << "Заполнение элементов матрицы (последняя линия):\n";
    // new_matrix.fill(new_matrix.end() - static_cast<int>(new_matrix.get_cols()), new_matrix.end(), "0");
    // std::cout << new_matrix << "\n\n";

    std::cout << "Константная матрица:\n";
    const Matrix<string> matrix13 = {{"11", "12", "13"},
                                     {"21", "22", "23"}};
    std::cout << "Range-based for cycle for const matrix:\n";
    for (const auto &elem : matrix13)
        std::cout << elem << "; ";
    std::cout << "\n\n";

    std::cout << "Проверка cbegin и cend к не константному объекту (new_matrix):\n";
    for (auto it = matrix11.cbegin(); it < matrix11.cend(); it++)
        std::cout << *it << "; ";
    std::cout << "\n\n";

    std::cout << "Математические операции:\n\n";
    Matrix<double> matrix14 = {{1, 2, 3, 4},
                               {7, 9, 11, 13},
                               {4, 2, 0, -2},
                               {1, 4, 7, 10}};
    std::cout << "matrix14: \n";
    std::cout << matrix14 << "\n\n";

    std::cout << "Операция: matrix14 += 2.5;\n";
    matrix14 += 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << matrix14 << "\n\n";

    std::cout << "Операция: matrix14 -= 2.5;\n";
    matrix14 -= 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << matrix14 << "\n\n";

    std::cout << "Операция: matrix14 *= 2.5;\n";
    matrix14 *= 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << matrix14 << "\n\n";

    std::cout << "Операция: matrix14 /= 2.5;\n";
    matrix14 /= 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << matrix14 << "\n\n";

    Matrix<double> tmp;

    std::cout << "Операция: tmp = matrix14 + 2.5;\n";
    tmp = matrix14 + 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << tmp << "\n\n";

    std::cout << "Операция: tmp = matrix14 - 2.5;\n";
    tmp = matrix14 - 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << tmp << "\n\n";

    std::cout << "Операция: tmp = matrix14 * 2.5;\n";
    tmp = matrix14 * 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << tmp << "\n\n";

    std::cout << "Операция: tmp = matrix14 / 2.5;\n";
    tmp = matrix14 / 2.5;
    std::cout << "Матрица после операции:\n";
    std::cout << tmp << "\n\n";

    Matrix<double> det_matrix = {{38, 382, 21, 9},
                                 {21, 1, 9, 11},
                                 {118, 5, 85, 2},
                                 {10, 8, 22, 13}};
    std::cout << "\ndet_matrix:\n"
              << det_matrix << "\n\n";

    std::cout << "Операция: det_matrix.determinant();\n";
    std::cout << "Результат: " << det_matrix.determinant() << "\n";

    std::cout << "Операция: det_matrix.inverse();\n";
    det_matrix.inverse();
    std::cout << "Результат: \n"
              << det_matrix << "\n";

    std::cout << "Матричное умножение: \n";
    Matrix<double> res;
    Matrix<double> m1 = {{1},
                         {2},
                         {3}},
                   m2 = {{1, 2}};
    std::cout << "Операция: m1 * m2 (m1 = { { 1 }, { 2 }, { 3 } }, m2 = { { 1, 2 } })\n";
    res = m1 * m2;
    std::cout << "Результат:\n"
              << res << "\n\n";

    std::cout << "Ошибки:\n\n";
    std::cout << "Обращение к неверному индексу столбца:\n";

    try
    {
        res[0][100] = 1;
    }
    catch (MatrixExceptions &err)
    {
        std::cout << err.what() << "\n\n\n";
    }

    std::cout << "Обращение к неверному индексу строки:\n";
    try
    {
        res[100][0] = 22;
    }
    catch (MatrixExceptions &err)
    {
        std::cout << err.what() << "\n\n\n";
    }

    std::cout << "Сложение с неправильными матрицами:\n";
    try
    {
        Matrix<int> m1 = {{1, 2, 3}};
        Matrix<int> m2 = {{1, 2},
                          {3, 4}};
        std::cout << m1 + m2;
    }
    catch (MatrixExceptions &err)
    {
        std::cout << err.what() << "\n\n\n";
    }

    std::cout << "Умножение неправильных матриц:\n";
    try
    {
        Matrix<int> m1 = {{1, 2, 3}};
        Matrix<int> m2 = {{1, 2, 3}};
        std::cout << m1 * m2;
    }
    catch (MatrixExceptions &err)
    {
        std::cout << err.what() << "\n\n\n";
    }

    std::cout << "Вызов конструктора с неправильными аргументами:\n";
    try
    {
        Matrix<int> matrix_inv = {{1, 2},
                                  {3}};
    }
    catch (MatrixExceptions &err)
    {
        std::cout << err.what() << "\n\n\n";
    }

    std::cout << "Вызов конструктора с нерабочей си матрицей\n";
    try
    {
        int **ec_matrix = NULL;
        Matrix<int> matr_er{2, 2, ec_matrix};
        std::cout << matr_er << "\n\n";
    }
    catch (MatrixExceptions &err)
    {
        std::cout << err.what() << "\n\n";
    }

    return 0;
}
