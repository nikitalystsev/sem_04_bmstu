//
// Created by nikita on 17.04.23.
//
#include <stdio.h>
#include <string.h>

#include "my_strlen.h"

extern  char *my_strncpy(char *dst, const char *src, size_t n);

int main(void) {

    char buff[15] = "Hello, world!";
    char buff_3[15] = "\0";

    size_t len_buff = my_strlen(buff);

    printf("len_buff = %u\n", len_buff);

    my_strncpy(buff_3, buff, len_buff);

    printf("buff_3 = (%s)\n", buff_3);

    return 0;
}