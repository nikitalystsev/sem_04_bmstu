#ifndef TRANSFORM_H
#define TRANSFORM_H

typedef struct move_t move_t;
typedef struct scale_t scale_t;
typedef struct rotate_t rotate_t;

// структура перемещения
struct move_t
{
    double dx;
    double dy;
    double dz;
};

// структура масштабирования
struct scale_t
{
    double kx;
    double ky;
    double kz;
};

// структура поворота
struct rotate_t
{
    double angle_x;
    double angle_y;
    double angle_z;
};


#endif // TRANSFORM_H
