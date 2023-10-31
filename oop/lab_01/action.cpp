#include "action.h"

myerror_t manager_actions(request_t *request) {
  // один раз создается из-за static
  static figure_t figure = init_figure();

  myerror_t rc = SUCCESS;

  switch (request->action) {
  case DOWNLOAD:
    rc = download_figure(&figure, request->filename);
    break;
  case DRAW:
    rc = draw_figure(&figure, &request->view);
    break;
  case MOVE:
    rc = move_figure(&figure, &request->move);
    break;
  case ROTATE:
    rc = rotate_figure(&figure, &request->rotate);
    break;
  case SCALE:
    rc = scale_figure(&figure, &request->scale);
    break;
  case QUIT:
    free_figure(&figure);
    break;
  default:
    rc = COMMAND_UNDEFINED;
  }

  return rc;
}
