#include "defines.h"

double asm_sin_pi(void)                             
{
    double res;

    __asm__(
        "fldpi\n\t"                     
        "fsin\n\t"                      
        "fstp %0\n\t"                   
        : "=m" (res)                 
    );

    return res;
}

double asm_sin_half_pi(void)                
{
    double res;
    const int divider = 2;
    
    __asm__(
        "fldpi\n\t"                  
        "fild %1\n\t"           
        "fdivp\n\t"                     
        "fsin\n\t"                      
        "fstp %0\n\t"                   
        : "=m" (res)                    
        : "m" (divider)                
    );

    return res;
}

int main(void)
{
    printf("\nTest PI: \n");
    
    printf("LIB sin(3.14) =      %.20f\n", sin(3.14));
    printf("LIB sin(3.141596) =  %.20f\n", sin(3.1415926));
    printf("FPU sin(PI) =        %.20f\n", asm_sin_pi());
    
    printf("\nTest PI / 2: \n");

    printf("LIB sin(3.14 / 2) =     %.20f\n", sin(3.14 / 2));
    printf("LIB sin(3.141596 / 2) = %.20f\n", sin(3.1415926 / 2));
    printf("FPU sin(PI / 2) =       %.20f\n", asm_sin_half_pi());
    
    return 0;
}
