#ifndef __MATRIX_H__
#define __MATRIX_H__

#include "defines.h"

typedef struct matrix_t matrix_t;

struct matrix_t
{
    float **matrix;
    size_t rows;
    size_t cols;
};

#define INIT_MATRIX(matrix_1)   \
    do                          \
    {                           \
        matrix_1.matrix = NULL; \
        matrix_1.rows = 0;      \
    } while (0);

int get_matrix_size(size_t *const n, size_t *const m);

int matrix_alloc(matrix_t *const matrix);
void matrix_free(float **matrix, const size_t n);

void fill_matrix_by_random(matrix_t *const matrix);

matrix_t matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2);

matrix_t asm_matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2);

void print_matrix(const matrix_t *const matrix);

#endif // __MATRIX_H__