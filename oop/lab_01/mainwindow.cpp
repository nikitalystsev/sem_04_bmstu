#include <QFileDialog>
#include <QMessageBox>
#include <iostream>
#include <QFileDialog>

#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent): QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QGraphicsScene *scene = new QGraphicsScene(this);

    ui->graphicsView->setScene(scene);
    ui->graphicsView->setAlignment(Qt::AlignTop | Qt::AlignLeft);
    ui->graphicsView->setStyleSheet("QGraphicsView {background-color: white}");
}

MainWindow::~MainWindow()
{
    request_t request;
    request.action = QUIT;
    manager_actions(&request);

    delete ui;
}

// вывод информационных сообщений
// #########################################################################################################
void MainWindow::on_info_about_file_triggered()
{
    QMessageBox::information(0, "Информация о входном файле", "Файл должен содержать количество точек\n"
                                 "Затем уже должны идти аргументы в строго в порядке:\n"
                                 "x y z\n"
                                 "После ввода все точек нужно отметить количество ребер\n"
                                 "Затем уже идут нумерация связи точек(нумерация с 0) в любом порядке:\n"
                                 "точка_1 точка_2\n\n"
                                 "PS. Проверяй данные в файле!");
}


void MainWindow::on_info_about_program_triggered()
{
    QMessageBox::information(0, "Информация о программе", "Привет, эта программа - 3D Viewer, созданные в целе\n"
                                  "сдачи лабораторной работы и предназначения для раcмотренние\n"
                                  "каркасных 3D моделей и не более.");
}


void MainWindow::on_info_about_developer_triggered()
{
    QMessageBox::information(0, "Информация о разработчике", "Разработчиком данной программы, является студент\n"
                                 "МГТУ им. Н.Э.Баумана, ИУ7-43Б, Лысцев Никита.");
}
// #########################################################################################################

error_t MainWindow::draw()
{
    auto rcontent = ui->graphicsView->contentsRect();
    ui->graphicsView->scene()->setSceneRect(0, 0, rcontent.width(),
                                            rcontent.height());

    // создали обработчик запросов
    request_t request;
    // определили действие обработчика
    request.action = DRAW;

    // проинициализировали данные холста
    request.view.scene = ui->graphicsView->scene();
    request.view.width = ui->graphicsView->scene()->width();
    request.view.height = ui->graphicsView->scene()->height();

    // обработали отрисовку
    return manager_actions(&request);
}

// выбор файла для загрузки
// #########################################################################################################
void MainWindow::on_choose_file_triggered()
{
    // переменная для сохранение пути файла
    QString file_path = QFileDialog::getOpenFileName(this, "Выберите файл",
                                                     "C:/Users/nikitalystsev/Documents/Studies/oop_4_sem/3d_viewer_lab1/data");

    // запрос на загрузку данных из файла
    request_t request;
    // определяем действие
    request.action = DOWNLOAD;
    // фиксируем имя файла
    request.filename = file_path.toLocal8Bit().data();

    // выполняем операцию по запросу
    error_t rc = manager_actions(&request);

    if (rc)
        error_message(rc);
    else
    {
        rc = draw();

        if (rc)
            error_message(rc);
    }
}


void MainWindow::on_move_button_clicked()
{
    request_t request;
    request.action = MOVE;

    request.move.dx = ui->move_dx->value();
    request.move.dy = ui->move_dy->value();
    request.move.dz = ui->move_dz->value();

    error_t rc = manager_actions(&request);

    if (rc)
        error_message(rc);
    else
    {
        rc = draw();

        if (rc)
            error_message(rc);
    }
}


void MainWindow::on_rotate_button_clicked()
{
    request_t request;
    request.action = ROTATE;

    request.rotate.angle_x = ui->rotate_angle_x->value();
    request.rotate.angle_y = ui->rotate_angle_y->value();
    request.rotate.angle_z = ui->rotate_angle_z->value();

    error_t rc = manager_actions(&request);

    if (rc)
        error_message(rc);
    else
    {
        rc = draw();

        if (rc)
            error_message(rc);
    }
}


void MainWindow::on_scale_button_clicked()
{
    request_t request;
    request.action = SCALE;

    request.scale.kx = ui->kx->value();
    request.scale.ky = ui->ky->value();
    request.scale.kz = ui->kz->value();

    error_t rc = manager_actions(&request);

    if (rc)
        error_message(rc);
    else
    {
        rc = draw();

        if (rc)
            error_message(rc);
    }
}

