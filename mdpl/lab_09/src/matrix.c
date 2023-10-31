#include "matrix.h"

int get_matrix_size(size_t *const n, size_t *const m)
{
    puts("Введите количество строк и столбцов в каждой строке: ");

    if (scanf("%lu", n) != 1)
        return ERR_DIMENTION;

    if (scanf("%lu", m) != 1)
        return ERR_DIMENTION;

    if (*n <= 0 || *m <= 0)
        return ERR_DIMENTION;

    return EXIT_SUCCESS;
}

int matrix_alloc(matrix_t *const matrix)
{
    matrix->matrix = calloc(matrix->rows, sizeof(float *));

    if (!matrix->matrix)
        return ERR_ALLOC_MATRIX;

    for (size_t i = 0; i < matrix->rows; i++)
    {
        matrix->matrix[i] = calloc(matrix->cols, sizeof(float));

        if (!matrix->matrix[i])
        {
            matrix_free(matrix->matrix, matrix->rows);
            return ERR_ALLOC_MATRIX;
        }
    }

    return EXIT_SUCCESS;
}

void matrix_free(float **matrix, const size_t n)
{
    for (size_t i = 0; i < n; i++)
        free(matrix[i]);

    free(matrix);
}

void fill_matrix_by_random(matrix_t *const matrix)
{
    for (size_t i = 0; i < matrix->rows; i++)
        for (size_t j = 0; j < matrix->cols; j++)
        {
            float x = MIN_DATA + rand() % (MAX_DATA - MIN_DATA + 1);

            matrix->matrix[i][j] = x;
        }
}

matrix_t matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2)
{
    matrix_t matrix_res;
    matrix_res.rows = matrix1->rows;
    matrix_res.cols = matrix1->cols;

    matrix_alloc(&matrix_res);

    for (size_t i = 0; i < matrix1->rows; i++)
        for (size_t j = 0; j < matrix1->cols; j++)
            matrix_res.matrix[i][j] = matrix1->matrix[i][j] + matrix2->matrix[i][j];

    return matrix_res;
}

matrix_t asm_matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2)
{
    matrix_t matrix_res;
    matrix_res.rows = matrix1->rows;
    matrix_res.cols = matrix2->cols;

    matrix_alloc(&matrix_res);

    for (size_t i = 0; i < matrix1->rows; i++)
    {
        for (size_t j = 0; j < matrix1->cols; j += 4)
        {
            // float arr1[4] = {matrix1->matrix[i][j], matrix1->matrix[i][j + 1], matrix1->matrix[i][j + 2], matrix1->matrix[i][j + 3]};
            float arr2[4] = {matrix2->matrix[i][j], matrix2->matrix[i][j + 1], matrix2->matrix[i][j + 2], matrix2->matrix[i][j + 3]};
            float arr3[4];

            __asm__(
                "movaps xmm0, %1\n\t"
                "movaps xmm1, %2\n\t"
                "addps xmm0, xmm1\n\t"
                "movaps %0, xmm0\n\t"
                : "=m"(arr3)
                : "m"(matrix1->matrix[i]), "m"(arr2));

            size_t l = j;

            for (size_t k = 0; k < 4; k++)
            {
                __asm__(
                    "movss xmm0, %0\n\t"
                    "movss xmm1, %1\n\t"
                    "addps xmm0, xmm1\n\t"
                    "movss %0, xmm0\n\t"
                    : "=m"(matrix_res.matrix[i][l])
                    : "m"(arr3[k]));

                l++;
            }
        }
    }

    return matrix_res;
}

void print_matrix(const matrix_t *const matrix)
{
    printf("Матрица:\n");

    for (size_t i = 0; i < matrix->rows; ++i)
    {
        for (size_t j = 0; j < matrix->cols; ++j)
            printf("%12.3f", matrix->matrix[i][j]);

        puts("");
    }
}