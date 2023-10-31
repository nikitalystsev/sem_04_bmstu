#include "figure.h"

// создали фигуру
figure_t init_figure(void) {
  figure_t figure;

  default_points(figure.points);
  default_edges(figure.edges);

  return figure;
}

// освобождаем память из-под фигуры
void free_figure(figure_t *figure) {
  if (figure) {
    free_points(&figure->points);
    free_edges(&figure->edges);
  }
}

// читаем фигуру из файла
myerror_t read_figure(figure_t &figure, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file)
    rc = ERR_OPEN_FILE;
  else {
    figure = init_figure();

    rc = read_info_about_points(&figure.points, file);

    if (rc == SUCCESS) {
      rc = read_info_about_edges(&figure.edges, file);

      if (rc)
        free_points(&figure.points);
    }
  }

  return rc;
}

myerror_t download_figure(figure_t *figure, const char *filename) {
  myerror_t rc = SUCCESS;

  if (!filename || !figure)
    rc = ERR_WRONG_PARAMS;
  else {
    FILE *file = fopen(filename, "r");

    if (!file)
      rc = ERR_OPEN_FILE;
    else {
      rc = read_figure(*figure, file);
      fclose(file);
    }
  }

  return rc;
}

myerror_t move_figure(figure_t *const figure, const move_t *const move) {
  myerror_t rc = SUCCESS;

  if (!figure || !move)
    rc = ERR_WRONG_PARAMS;
  else
    rc = move_points(&figure->points, move);

  return rc;
}

myerror_t rotate_figure(figure_t *const figure, const rotate_t *const rotate) {
  myerror_t rc = SUCCESS;

  if (!figure || !rotate)
    rc = ERR_WRONG_PARAMS;
  else
    rc = rotate_points(&figure->points, rotate);

  return rc;
}

myerror_t scale_figure(figure_t *const figure, const scale_t *const scale) {
  myerror_t rc = SUCCESS;

  if (!figure || !scale)
    rc = ERR_WRONG_PARAMS;
  else
    rc = scale_points(&figure->points, scale);

  return rc;
}
