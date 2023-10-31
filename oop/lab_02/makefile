$(shell mkdir -p out)

CC := g++

CFLAGS := -std=c++20 -Wall -Werror -pedantic -Wextra -Iinc -Wvla


PREF_SRC := ./src/
PREF_INC := ./inc/
PREF_OUT := ./out/

# получаем список сpp файлов в подпапке ./src/
SRC := $(wildcard $(PREF_SRC)*.cpp)

# получаем заменой список объектных файлов для файлов из подпапки ./src/
SRC_OBJ := $(patsubst $(PREF_SRC)%.cpp, $(PREF_OUT)%.o, $(SRC))

.PHONY: debug release clean run

run : app.exe
	./app.exe

app.exe : $(SRC_OBJ)
	$(CC) $(SRC_OBJ) -o app.exe

# получаем объектные файлы с помощью си файлов из подпапки ./src/
$(PREF_OUT)%.o : $(PREF_SRC)%.cpp
	$(CC) $(CFLAGS) -c -MD $< -o $@

include $(wildcard $(PREF_OUT)*.d)

debug : CFLAGS += -g3
debug : app.exe

release : CFLAGS += -DNDEBUG -g0
release : app.exe

clean :
	rm -Rf $(PREF_OUT) ./*.exe
