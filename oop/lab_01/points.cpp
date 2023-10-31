#include "points.h"

// начальные параметры
void default_points(points_t &points) {
  points.points_array = NULL;
  points.size = 0;
}

// выделяем память под массив точек
myerror_t points_alloc(point_t **points, const int size) {
  myerror_t rc = SUCCESS;

  if (!points || !size)
    rc = ERR_WRONG_PARAMS;
  else if (size <= 0)
    rc = ERR_SIZE_POINTS;
  else {
    point_t *tmp = (point_t *)malloc(size * sizeof(point_t));

    if (tmp)
      *points = tmp;
    else
      rc = ERR_MEM_ALLOC;
  }

  return rc;
}

// освободили память из под массива точек
void free_points(points_t *const points) {
  if (points)
    free(points->points_array);
}

// считываем количество точек
static myerror_t read_count_points(int *const size_points, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file || !size_points)
    rc = ERR_WRONG_PARAMS;
  else if (fscanf(file, "%d", size_points) != 1)
    rc = ERR_READ_FILE;
  else if (*size_points <= 0)
    rc = ERR_SIZE_POINTS;

  return rc;
}

// считываем сами точки
static myerror_t read_points(point_t *const points, const int size,
                             FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file || !points)
    rc = ERR_WRONG_PARAMS;
  else if (size <= 0)
    rc = ERR_SIZE_POINTS;
  else
    for (int i = 0; rc == SUCCESS && i < size; i++)
      rc = read_point(&points[i], file);

  return rc;
}

// считываем все точки
myerror_t read_info_about_points(points_t *const points, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file || !points)
    rc = ERR_WRONG_PARAMS;
  else {
    rc = read_count_points(&points->size, file);

    if (!rc) {
      rc = points_alloc(&points->points_array, points->size);

      if (!rc) {
        rc = read_points(points->points_array, points->size, file);

        if (rc)
          free_points(points);
      }
    }
  }

  return rc;
}

myerror_t move_points(points_t *const points, const move_t *const move) {
  myerror_t rc = SUCCESS;

  if (!points || !move)
    rc = ERR_WRONG_PARAMS;
  else if (!points->points_array)
    rc = ERR_FIGURE_NOT_LOAD;
  else
    for (int i = 0; rc == SUCCESS && i < points->size; i++)
      rc = move_point(&points->points_array[i], move);

  return rc;
}

myerror_t rotate_points(points_t *const points, const rotate_t *const rotate) {
  myerror_t rc = SUCCESS;

  if (!points || !rotate)
    rc = ERR_WRONG_PARAMS;
  else if (!points->points_array)
    return ERR_FIGURE_NOT_LOAD;
  else
    for (int i = 0; rc == SUCCESS && i < points->size; i++)
      rc = rotate_point(&points->points_array[i], rotate);

  return rc;
}

myerror_t scale_points(points_t *const points, const scale_t *const scale) {
  myerror_t rc = SUCCESS;

  if (!points || !scale)
    rc = ERR_WRONG_PARAMS;
  else if (!points->points_array)
    rc = ERR_FIGURE_NOT_LOAD;
  else if (scale->kx == 0 || scale->ky == 0 || scale->kz == 0)
    rc = ERR_SCALE_COEFF;
  else
    for (int i = 0; rc == SUCCESS && i < points->size; i++)
      rc = scale_point(&points->points_array[i], scale);

  return rc;
}
