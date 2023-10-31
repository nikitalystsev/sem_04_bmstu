#include "measurements.h"

void time_matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2)
{
    matrix_t matrix_res;

    long double beg = microseconds_now();

    for (size_t i = 0; i < N_REPS; ++i)
    {
        matrix_res = matrix_add(matrix1, matrix2);

        matrix_free(matrix_res.matrix, matrix_res.rows);
    }

    long double end = microseconds_now() - beg;

    printf("time_matrix_add: %.20Lf мкс\n", end / N_REPS);
}

void time_asm_matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2)
{
    matrix_t matrix_res;

    long double beg = microseconds_now();

    for (size_t i = 0; i < N_REPS; ++i)
    {
        matrix_res = asm_matrix_add(matrix1, matrix2);

        matrix_free(matrix_res.matrix, matrix_res.rows);
    }

    long double end = microseconds_now() - beg;

    printf("time_asm_matrix_add: %.20Lf мкс\n", end / N_REPS);
}
