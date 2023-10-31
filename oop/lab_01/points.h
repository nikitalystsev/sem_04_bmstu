#ifndef POINTS_H
#define POINTS_H

#include "error.h"
#include "point.h"
#include "transform.h"

typedef struct points_t points_t;

// структура - массив точек
struct points_t {
  point_t *points_array;
  int size;
};

void default_points(points_t &points);

myerror_t points_alloc(point_t **points, const int size);

void free_points(points_t *points);

myerror_t read_info_about_points(points_t *const points, FILE *file);

myerror_t move_points(points_t *const points, const move_t *const move);

myerror_t rotate_points(points_t *const points, const rotate_t *const rotate);

myerror_t scale_points(points_t *const points, const scale_t *const scale);

#endif // POINTS_H
