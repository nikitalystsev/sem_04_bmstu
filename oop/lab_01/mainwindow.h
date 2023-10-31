#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include "action.h"
#include "error.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
  Q_OBJECT

public:
  MainWindow(QWidget *parent = nullptr);
  ~MainWindow();

private slots:
  myerror_t draw();

  void on_info_about_file_triggered();

  void on_info_about_program_triggered();

  void on_info_about_developer_triggered();

  void on_choose_file_triggered();

  void on_move_button_clicked();

  void on_rotate_button_clicked();

  void on_scale_button_clicked();

private:
  Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
