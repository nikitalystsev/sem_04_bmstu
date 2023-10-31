#include "defines.h"
#include "matrix.h"
#include "measurements.h"

// void add_elements(void)
// {
//     float arr1[5] = {1, 2, 3, 4, 5};
//     float arr2[5] = {1, 2, 3, 4, 5};
//     float arr3[5] = {0};

//     for (size_t i = 0; i < 5; i += 4)
//     {
//         float *p = &arr3[i];
        
//         __asm__ ("mov eax, %1\n\t"
//                 "movups xmm0, [eax]\n\t"
//                 "mov ebx, %2\n\t"
//                 "movups xmm1, [ebx]\n\t"
//                 "addps xmm0, xmm1\n\t"
//                 "movups %0, xmm0\n\t"
//                 : "=r"(p)
//                 : "r"(&arr1[i]), "r"(&arr2[i])
//         );
//     }

//     for (size_t i = 0; i < 4; i++)
//         printf("arr3[%lu] = %f\n", i, arr3[i]);

//     return;
// }

int main(void)
{
    int rc = 0;
    
    printf("Hello, world!\n");

    matrix_t matrix1, matrix2;

    printf("sizeof(float) = %lu байтов\n", sizeof(float));
    printf("sizeof(double) = %lu байтов\n", sizeof(double));
    printf("sizeof(long double) = %lu байтов\n", sizeof(long double));

    // add_elements();

    INIT_MATRIX(matrix1);
    INIT_MATRIX(matrix2);

    rc = get_matrix_size(&matrix1.rows, &matrix1.cols);
    rc += get_matrix_size(&matrix2.rows, &matrix2.cols);

    matrix_alloc(&matrix1);
    matrix_alloc(&matrix2);

    srand(time(NULL));
    fill_matrix_by_random(&matrix1);
    fill_matrix_by_random(&matrix2);

    print_matrix(&matrix1);
    print_matrix(&matrix2);

    matrix_t matrix_res = asm_matrix_add(&matrix1, &matrix2);
    print_matrix(&matrix_res);

    time_matrix_add(&matrix1, &matrix2);
    time_asm_matrix_add(&matrix1, &matrix2);

    matrix_free(matrix1.matrix, matrix1.rows);
    matrix_free(matrix2.matrix, matrix2.rows);

    return rc;
}
