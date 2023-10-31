#ifndef FIGURE_H
#define FIGURE_H

#include <stdio.h>

#include "edge.h"
#include "points.h"
#include "transform.h"

typedef struct figure_t figure_t;

// фигура
struct figure_t {
  points_t points;
  edges_t edges;
};

figure_t init_figure(void);

void free_figure(figure_t *figure);

myerror_t read_figure(figure_t &figure, FILE *file);

myerror_t download_figure(figure_t *figure, const char *filename);

myerror_t move_figure(figure_t *const figure, const move_t *const move);

myerror_t rotate_figure(figure_t *const figure, const rotate_t *const rotate);

myerror_t scale_figure(figure_t *const figure, const scale_t *const scale);

#endif // FIGURE_H
