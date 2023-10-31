#include <stdio.h>
#include "timing.h"
// // Получение времени в микросекундах
// long double microseconds_now(void)
// {
//     struct timeval val;

//     if (gettimeofday(&val, NULL))
//         return (unsigned long long) -1;

//     return val.tv_sec * 1000000ULL + val.tv_usec;
// }

void print_sum_mul_32_bit(void)
{
    float a = -1.23, b = 1023.1;

    long double sum_time = 0;

    for (int i = 0; i < N_REPS; i++)
    {
        long double beg = microseconds_now();
        float res = a + b;
        long double end = microseconds_now() - beg;

        sum_time += end;
    }

    printf("sum_time float 32 bit = %Lf\n", sum_time / N_REPS);

    long double mul_time = 0;

    for (int i = 0; i < N_REPS; i++)
    {
        long double beg = microseconds_now();
        float res = a * b;
        long double end = microseconds_now() - beg;

        sum_time += end;
    }

    printf("mul_time float 32 bit = %Lf\n", mul_time / N_REPS);
}

void print_asm_sum_mul_32_bit(void)
{
    float a = -1.23, b = 1023.1;

    long double sum_time = 0;

    for (int i = 0; i < N_REPS; i++)
    {
        float res;
        long double beg = microseconds_now();
        __asm__ (
        "fld %1 \n\t"
        "fld %2 \n\t"
        "faddp \n\t"
        "fstp %0 \n\t"
        : "=m"(res)
        : "m"(a), "m"(b)
        );
        long double end = microseconds_now() - beg;

        sum_time += end;
    }

    printf("sum_time asm float 32 bit = %Lf\n", sum_time / N_REPS);

    long double mul_time = 0;

    for (int i = 0; i < N_REPS; i++)
    {
        float res;
        long double beg = microseconds_now();
        __asm__ (
        "fld %1 \n\t"
        "fld %2 \n\t"
        "fmulp \n\t"
        "fstp %0 \n\t"
        : "=m"(res)
        : "m"(a), "m"(b)
        );
        long double end = microseconds_now() - beg;

        sum_time += end;
    }

    printf("mul_time asm float 32 bit = %Lf\n", mul_time / N_REPS);
}

int main(void)
{
    print_sum_mul_32_bit();
    
    print_asm_sum_mul_32_bit();

    return 0;
}
