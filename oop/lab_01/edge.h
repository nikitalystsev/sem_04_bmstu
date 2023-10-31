#ifndef EGDE_H
#define EGDE_H

#include "error.h"
#include <stdio.h>

typedef struct edge_t edge_t;

// ребро
struct edge_t {
  int first_point;
  int second_point;
};

// массив ребер
struct edges_t {
  edge_t *edges_array;
  int size;
};

void default_edges(edges_t &edges);

myerror_t edges_alloc(edges_t *const edges);

void free_edges(edges_t *const edges);

myerror_t read_info_about_edges(edges_t *const edges, FILE *file);

#endif // EGDE_H
