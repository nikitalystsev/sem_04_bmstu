#ifndef POINT_H
#define POINT_H

#include <stdio.h>
#include <math.h>
#include "error.h"
#include "transform.h"

typedef struct point_t point_t;

struct point_t
{
    double x;
    double y;
    double z;
};

void default_point(point_t &point);

error_t read_point(point_t *const point, FILE *file);

error_t move_point(point_t *const point, const move_t *const move);

error_t rotate_point(point_t *const point, const rotate_t *const rotate);

error_t scale_point(point_t *const point, const scale_t *const scale);

#endif // POINT_H
