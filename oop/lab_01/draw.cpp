#include "draw.h"


static point_t to_centre(point_t point, const draw_t *view)
{
    point.x += view->width / 2;
    point.y += view->height / 2;

    return point;
}

static void all_to_centre(points_t *const points, const draw_t *view)
{
    for (int i = 0; i < points->size; i++)
        points->points_array[i] = to_centre(points->points_array[i], view);
}

static line_t get_line(const edge_t *const edge, const point_t *const points_array)
{
    line_t line;

    line.first_point = points_array[edge->first_point];
    line.second_point = points_array[edge->second_point];

    return line;
}

error_t clear_scene(draw_t *const view)
{
    error_t rc = SUCCESS;

    if (!view)
        rc = ERR_WRONG_PARAMS;
    else if (!view->scene)
        rc = ERR_SCENE_WRONG;
    else
        view->scene->clear();

    return rc;
}

error_t draw_line(const draw_t *const view, const point_t *const p1, const point_t *const p2)
{
    error_t rc = SUCCESS;

    if (!view || !p1 || !p2)
        rc = ERR_WRONG_PARAMS;
    else if (!view->scene)
        rc = ERR_SCENE_WRONG;
    else
        view->scene->addLine(p1->x, p1->y, p2->x, p2->y);

    return rc;
}

error_t draw_lines(const draw_t *const view,
                   points_t *const points,
                   const edges_t *const edges)
{
    error_t rc = SUCCESS;

    if (!view || !points || !edges)
        rc = ERR_WRONG_PARAMS;
    else if (!points->points_array || !edges->edges_array)
        rc = ERR_MEM_ALLOC;
    else if (!view->scene)
        rc = ERR_SCENE_WRONG;
    else
    {
        all_to_centre(points, view);

        line_t line;

        for (int i = 0; rc == SUCCESS && i < edges->size; i++)
        {
            line = get_line(&edges->edges_array[i], points->points_array);
            rc = draw_line(view, &line.first_point, &line.second_point);
        }
    }

    return rc;
}

error_t draw_figure(figure_t *const figure, draw_t *const view)
{
    error_t rc = SUCCESS;

    if (!figure || !view)
        rc = ERR_WRONG_PARAMS;
    else
    {
        rc = clear_scene(view);

        if (!rc)
            rc = draw_lines(view, &figure->points, &figure->edges);
    }

    return rc;
}

