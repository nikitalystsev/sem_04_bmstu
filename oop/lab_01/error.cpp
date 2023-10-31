#include "error.h"

void error_message(myerror_t &error) {
  switch (error) {
  case ERR_OPEN_FILE:
    QMessageBox::critical(NULL, "Ошибка!", "Не удалось открыть файл!");
    break;
  case ERR_READ_FILE:
    QMessageBox::critical(NULL, "Ошибка!", "Не удалось прочитать файл!");
    break;
  case ERR_MEM_ALLOC:
    QMessageBox::critical(NULL, "Ошибка!", "Не удалось выделить память!");
    break;
  case ERR_SIZE_POINTS:
    QMessageBox::critical(NULL, "Ошибка!",
                          "Кол-во точек в файле должно быть > 0!");
    break;
  case ERR_SIZE_EDGES:
    QMessageBox::critical(NULL, "Ошибка!",
                          "Кол-во ребер в файле должно быть > 0!");
    break;
  case ERR_SCENE_WRONG:
    QMessageBox::critical(NULL, "Ошибка!",
                          "При попытке нарисовать, фигуру произошла ошибка!");
    break;
  case ERR_SCALE_COEFF:
    QMessageBox::critical(
        NULL, "Ошибка!", "Коэффициенты масштабирования не должны равняться 0!");
    break;
  case ERR_FIGURE_NOT_LOAD:
    QMessageBox::information(NULL, "Информация!", "Фигура не загружена!");
    break;
  case ERR_WRONG_PARAMS:
    QMessageBox::critical(NULL, "Ошибка!", "Переданы некорректные параметры!");
    break;
  default:
    QMessageBox::critical(NULL, "Ошибка!", "Неизвестная ошибка!");
  }
}
