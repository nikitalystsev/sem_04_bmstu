
#ifndef ACTION_H
#define ACTION_H

#include "draw.h"
#include "error.h"
#include "transform.h"

enum actions { DOWNLOAD, DRAW, MOVE, ROTATE, SCALE, QUIT };

typedef enum actions actions_t;
typedef struct request_t request_t;

struct request_t {
  const char *filename;
  draw_t view;
  actions_t action;
  move_t move;
  rotate_t rotate;
  scale_t scale;
};

myerror_t manager_actions(request_t *request);

#endif // ACTION_H
