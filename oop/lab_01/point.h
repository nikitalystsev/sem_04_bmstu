#ifndef POINT_H
#define POINT_H

#include "error.h"
#include "transform.h"
#include <math.h>
#include <stdio.h>

typedef struct point_t point_t;

struct point_t {
  double x;
  double y;
  double z;
};

void default_point(point_t &point);

myerror_t read_point(point_t *const point, FILE *file);

myerror_t move_point(point_t *const point, const move_t *const move);

myerror_t rotate_point(point_t *const point, const rotate_t *const rotate);

myerror_t scale_point(point_t *const point, const scale_t *const scale);

#endif // POINT_H
