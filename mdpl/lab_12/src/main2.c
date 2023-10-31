#include <stdio.h>

void asm_sum_array(float *vector1, float *vector2, float *res, int lenght)
{
    float *p_vector1 = vector1;
    float *p_vector2 = vector2;
    float *p_res = res;

    for (int i = 0; i < lenght / 4; i++, p_vector1 += 4, p_vector2 += 4, p_res += 4)
    {
        float result = 0;

        __asm__(
            "ld1 {v0.4s}, [%1]\n"
            "ld1 {v1.4s}, [%2]\n"
            "fadd v2.4s, v0.4s, v1.4s\n"
            "st1 {v2.4s}, [%3]\n"
            : "=r"(result)
            : "r"(p_vector1), "r"(p_vector2), "r"(p_res)
            : "v0", "v1", "v2");
    }
}

int main(void)
{
    float vector1[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    float vector2[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    int length = 8;

    printf("sizeof(float) = %lu\n", sizeof(float));

    float vector3[8];

    asm_sum_array(vector1, vector2, vector3, length);

    for (int i = 0; i < length; i++)
        printf("elem = %f\n", vector3[i]);

    return 0;
}
