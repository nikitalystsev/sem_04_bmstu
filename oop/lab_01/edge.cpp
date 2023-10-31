#include "edge.h"

// начальные параметры
void default_edges(edges_t &edges) {
  edges.edges_array = NULL;
  edges.size = 0;
}

// выделяем память под массив ребер
myerror_t edges_alloc(edge_t **edges, const int size) {
  myerror_t rc = SUCCESS;

  if (!edges)
    rc = ERR_WRONG_PARAMS;
  else if (size <= 0)
    rc = ERR_SIZE_POINTS;
  else if (size) {
    edge_t *tmp = (edge_t *)malloc(size * sizeof(edge_t));

    if (tmp)
      *edges = tmp;
    else
      rc = ERR_MEM_ALLOC;
  }

  return rc;
}

// освободили память из под массива ребер
void free_edges(edges_t *const edges) {
  if (edges)
    free(edges->edges_array);
}

// считываем количество ребер
static myerror_t read_count_edges(int *const size_edges, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file || !size_edges)
    rc = ERR_WRONG_PARAMS;
  else if (fscanf(file, "%d", size_edges) != 1)
    rc = ERR_READ_FILE;
  else if (*size_edges <= 0)
    rc = ERR_SIZE_POINTS;

  return rc;
}

// чтение точки из файла
static myerror_t read_edge(edge_t *const edge, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file || !edge)
    rc = ERR_WRONG_PARAMS;
  else if (fscanf(file, "%d %d", &edge->first_point, &edge->second_point) != 2)
    rc = ERR_READ_FILE;

  return rc;
}

// считываем сами ребра
static myerror_t read_edges(edge_t *const edges, const int size, FILE *file) {
  myerror_t rc = SUCCESS;

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
myerror_t read_info_about_edges(edges_t *const edges, FILE *file) {
  myerror_t rc = SUCCESS;

  if (!file || !edges)
    rc = ERR_WRONG_PARAMS;
  else {
    rc = read_count_edges(&edges->size, file);

    if (!rc) {
      rc = edges_alloc(&edges->edges_array, edges->size);

      if (!rc) {
        rc = read_edges(edges->edges_array, edges->size, file);

        if (rc)
          free_edges(edges);
      }
    }
  }

  return rc;
}
