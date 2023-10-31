#ifndef __MEASUREMENTS_H__
#define __MEASUREMENTS_H__

#include "defines.h"
#include "matrix.h"
#include "timing.h"

void time_matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2);
void time_asm_matrix_add(const matrix_t *const matrix1, const matrix_t *const matrix2);

#endif // __MEASUREMENTS_H__