#include "edge.h"

// начальные параметры
void default_edges(edges_t &edges)
{
    edges.edges_array = NULL;
    edges.size = 0;
}

// выделяем память под массив ребер
error_t edges_alloc(edge_t **edges, const int size)
{
    error_t rc = SUCCESS;

    if (!edges)
        rc = ERR_WRONG_PARAMS;
    else if (size <= 0)
        rc = ERR_SIZE_POINTS;
    else if (size)
    {
        edge_t *tmp = (edge_t *) malloc(size * sizeof(edge_t));

        if (tmp)
            *edges = tmp;
        else
            rc = ERR_MEM_ALLOC;
    }

    return rc;
}

// освободили память из под массива ребер
void free_edges(edges_t *const edges)
{
    if (edges)
        free(edges->edges_array);
}

// считываем количество ребер
static error_t read_count_edges(int *const size_edges, FILE *file)
{
    error_t rc = SUCCESS;

    if (!file || !size_edges)
        rc = ERR_WRONG_PARAMS;
    else if (fscanf_s(file, "%d", size_edges) != 1)
        rc = ERR_READ_FILE;
    else if (*size_edges <= 0)
        rc = ERR_SIZE_POINTS;

    return rc;
}

// чтение точки из файла
static error_t read_edge(edge_t *const edge, FILE *file)
{
    error_t rc = SUCCESS;

    if (!file || !edge)
        rc = ERR_WRONG_PARAMS;
    else if(fscanf_s(file, "%d %d", &edge->first_point, &edge->second_point) != 2)
        rc = ERR_READ_FILE;

    return rc;
}

// считываем сами ребра
static error_t read_edges(edge_t *const edges, const int size, FILE *file)
{
    error_t rc = SUCCESS;

    if (!file || !edges)
        rc = ERR_WRONG_PARAMS;
    else if (size <= 0)
        rc = ERR_SIZE_EDGES;
    else if (!edges)
        rc = ERR_MEM_ALLOC;
    else
        for (int i = 0; rc == SUCCESS && i < size; i++)
            rc = read_edge(&edges[i], file);

    return rc;
}

// считываем все точки
error_t read_info_about_edges(edges_t *const edges, FILE *file)
{
    error_t rc = SUCCESS;

    if (!file || !edges)
        rc = ERR_WRONG_PARAMS;
    else
    {
        rc = read_count_edges(&edges->size, file);

        if (!rc)
        {
            rc = edges_alloc(&edges->edges_array, edges->size);

            if (!rc)
            {
                rc = read_edges(edges->edges_array, edges->size, file);

                if (rc)
                    free_edges(edges);
            }
        }
    }

    return rc;
}
