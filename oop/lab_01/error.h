#ifndef ERROR_H
#define ERROR_H

#include <QMessageBox>

enum errors
{
    SUCCESS,
    ERR_WRONG_PARAMS,
    ERR_OPEN_FILE,
    ERR_MEM_ALLOC,
    ERR_READ_FILE,
    ERR_SCENE_WRONG,
    ERR_SIZE_POINTS,
    ERR_FIGURE_NOT_LOAD,
    ERR_SCALE_COEFF,
    ERR_SIZE_EDGES,
    COMMAND_UNDEFINED
};

typedef enum errors error_t;

void error_message(error_t &error);

#endif // ERROR_H
