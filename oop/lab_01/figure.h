#ifndef FIGURE_H
#define FIGURE_H

#include <stdio.h>

#include "points.h"
#include "edge.h"
#include "transform.h"

typedef struct figure_t figure_t;

// фигура
struct figure_t
{
    points_t points;
    edges_t edges;
};

figure_t init_figure(void);

void free_figure(figure_t *figure);

error_t read_figure(figure_t &figure, FILE *file);

error_t download_figure(figure_t *figure, const char *filename);

error_t move_figure(figure_t *const figure, const move_t *const move);

error_t rotate_figure(figure_t *const figure, const rotate_t *const rotate);

error_t scale_figure(figure_t *const figure, const scale_t *const scale);

#endif // FIGURE_H
