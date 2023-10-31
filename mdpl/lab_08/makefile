$(shell mkdir -p out)

CC := gcc
CC_ASM := nasm
CFLAGS := -std=c11 -Wall -pedantic -Wextra -Wfloat-equal -fverbose-asm -masm=intel -Iinc -Wvla

LINKFLAGS := -lpthread

PREF_SRC := ./src/
PREF_INC := ./inc/
PREF_OUT := ./out/

# получаем список си файлов в подпапке ./src/
SRC := $(wildcard $(PREF_SRC)*.c)

SRC_32_BIT := $(PREF_SRC)sum_mul_float_32_bit.c
SRC_64_BIT := $(PREF_SRC)sum_mul_double_64_bit.c
SRC_SIN := $(PREF_SRC)sin_pi_pi_half_2.c
SRC_TIMING := $(PREF_SRC)timing.c


OBJ_32_BIT := $(PREF_OUT)sum_mul_float_32_bit.o
OBJ_64_BIT := $(PREF_OUT)sum_mul_double_64_bit.o
OBJ_SIN := $(PREF_OUT)sin_pi_pi_half_2.o
OBJ_TIMING := $(PREF_OUT)timing.o

fpu: CFLAGS += -m80387 
fpu: 32_bit 64_bit sin

sse: CFLAGS += -mno-80387 -mno-sse
sse: 32_bit 64_bit sin

pi: sin

32_bit: $(OBJ_32_BIT) $(OBJ_TIMING)
	$(CC) $(OBJ_32_BIT) $(OBJ_TIMING) -m32 -o sum_mul_float_32_bit.exe 

64_bit: $(OBJ_64_BIT) $(OBJ_TIMING)
	$(CC) $(OBJ_64_BIT) $(OBJ_TIMING) -m32 -o sum_mul_double_64_bit.exe 

sin: $(OBJ_SIN) $(OBJ_TIMING)
	$(CC) $(OBJ_SIN) $(OBJ_TIMING) -m32 -o sin_pi_pi_half_2.exe 


$(OBJ_32_BIT): $(SRC_32_BIT)
	$(CC) $(CFLAGS) -m32   -c -MD $< -o $@

$(OBJ_64_BIT): $(SRC_64_BIT)
	$(CC) $(CFLAGS) -m32  -c -MD $< -o $@

$(OBJ_SIN): $(SRC_SIN)
	$(CC) $(CFLAGS) -m32  -c -MD $< -o $@

$(OBJ_TIMING): $(SRC_TIMING)
	$(CC) $(CFLAGS) -m32  -c -MD $< -o $@

assembly:
	gcc -S $(SRC_32_BIT) -O0 -Iinc -o $(PREF_OUT)sum_mul_float_32_bit_sse.s
	gcc -S $(SRC_32_BIT) -m80387 -O0 -Iinc -o $(PREF_OUT)sum_mul_float_32_bit_fpu.s

	gcc -S $(SRC_64_BIT) -O0 -Iinc -o $(PREF_OUT)sum_mul_double_64_bit_sse.s
	gcc -S $(SRC_64_BIT) -m80387 -O0 -Iinc -o $(PREF_OUT)sum_mul_double_64_bit_fpu.s

	g++ -S $(SRC_SIN) -masm=intel -O0 -Iinc -o $(PREF_OUT)sin_pi_pi_half_2.s

include $(wildcard $(PREF_OUT)*.d)

.PHONY: run assembly clean 

clean :
	rm -Rf $(PREF_OUT) ./*.exe