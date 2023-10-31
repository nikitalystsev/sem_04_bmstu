#include <stdio.h>

int my_strlen(const char *const str)
{
    int length;

    __asm__(
        "mov x0, %1 \n"
        "ldr x3, =0 \n"
        "ldr x4, =0 \n"
        "loop: \n"
        "ldrb w4, [x0], #1 \n"
        "cmp x4, #0 \n"
        "beq end \n"
        "add x3, x3, #1 \n"
        "b loop \n"
        "end: \n"
        "mov %0, x3 \n"
        : "=r"(length)
        : "r"(str)
        : "r0", "r3", "r4");

    return length;
}

int main()
{
    const char *str = "Hello, World!";

    int len = my_strlen(str);

    printf("Length: %d\n", len);

    return 0;
}
