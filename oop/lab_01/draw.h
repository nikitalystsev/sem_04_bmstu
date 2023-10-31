#ifndef DRAW_H
#define DRAW_H

#include <QGraphicsScene>

#include "edge.h"
#include "figure.h"
#include "point.h"
#include "points.h"

typedef struct line_t line_t;
typedef struct draw_t draw_t;

// линия
struct line_t {
  point_t first_point;
  point_t second_point;
};

// холст
struct draw_t {
  QGraphicsScene *scene;
  double width;
  double height;
};

myerror_t clear_scene(draw_t *const view);

myerror_t draw_line(const draw_t *const view, const point_t *const p1,
                    const point_t *const p2);

myerror_t draw_lines(const draw_t *const view, points_t *const points,
                     const edges_t *const edges);

myerror_t draw_figure(figure_t *const figure, draw_t *const view);

#endif // DRAW_H
