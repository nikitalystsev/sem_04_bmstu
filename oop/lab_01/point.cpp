#include "point.h"

void default_point(point_t &point) {
  point.x = 0;
  point.y = 0;
  point.z = 0;
}

myerror_t read_point(point_t *const point, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!point || !file)
    rc = ERR_WRONG_PARAMS;
  else if (fscanf(file, "%lf %lf %lf", &point->x, &point->y, &point->z) != 3)
    rc = ERR_READ_FILE;

  return rc;
}

myerror_t move_point(point_t *const point, const move_t *const move) {
  myerror_t rc = SUCCESS;

  if (!point || !move)
    rc = ERR_WRONG_PARAMS;
  else {
    point->x += move->dx;
    point->y += move->dy;
    point->z += move->dz;
  }

  return rc;
}

static double to_radians_angle(const double angle) {
  return angle * (M_PI / 180);
}

static myerror_t rotate_around_x(point_t *const point, const double angle) {
  myerror_t rc = SUCCESS;

  if (!point)
    rc = ERR_WRONG_PARAMS;
  else {
    double cos_angle = cos(to_radians_angle(angle));
    double sin_angle = sin(to_radians_angle(angle));

    double tmp_y = point->y;

    point->y = point->y * cos_angle + point->z * sin_angle;
    point->z = -tmp_y * sin_angle + point->z * cos_angle;
  }

  return rc;
}

static myerror_t rotate_around_y(point_t *const point, const double angle) {
  myerror_t rc = SUCCESS;

  if (!point)
    rc = ERR_WRONG_PARAMS;
  else {
    double cos_angle = cos(to_radians_angle(angle));
    double sin_angle = sin(to_radians_angle(angle));

    double tmp_x = point->x;

    point->x = point->x * cos_angle + point->z * sin_angle;
    point->z = -tmp_x * sin_angle + point->z * cos_angle;
  }

  return rc;
}

static myerror_t rotate_around_z(point_t *const point, const double angle) {
  myerror_t rc = SUCCESS;

  if (!point)
    rc = ERR_WRONG_PARAMS;
  else {
    double cos_angle = cos(to_radians_angle(angle));
    double sin_angle = sin(to_radians_angle(angle));
    double tmp_x = point->x;

    point->x = point->x * cos_angle + point->y * sin_angle;
    point->y = -tmp_x * sin_angle + point->y * cos_angle;
  }

  return rc;
}

myerror_t rotate_point(point_t *const point, const rotate_t *const rotate) {
  myerror_t rc = SUCCESS;

  if (!point || !rotate)
    rc = ERR_WRONG_PARAMS;
  else {
    rc = rotate_around_x(point, rotate->angle_x);

    if (!rc) {
      rc = rotate_around_y(point, rotate->angle_y);

      if (!rc)
        rc = rotate_around_z(point, rotate->angle_z);
    }
  }

  return rc;
}

myerror_t scale_point(point_t *const point, const scale_t *const scale) {
  myerror_t rc = SUCCESS;

  if (!point || !scale)
    rc = ERR_WRONG_PARAMS;
  else {
    point->x *= scale->kx;
    point->y *= scale->ky;
    point->z *= scale->kz;
  }

  return rc;
}
