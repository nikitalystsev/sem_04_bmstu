/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *choose_file;
    QAction *info_about_file;
    QAction *info_about_program;
    QAction *info_about_developer;
    QWidget *centralwidget;
    QGraphicsView *graphicsView;
    QFrame *frame;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout_2;
    QLabel *label_3;
    QDoubleSpinBox *kx;
    QLabel *label;
    QLabel *label_2;
    QDoubleSpinBox *ky;
    QDoubleSpinBox *kz;
    QPushButton *scale_button;
    QLabel *label_scale;
    QLabel *label_scale_2;
    QFrame *frame_2;
    QWidget *gridLayoutWidget_2;
    QGridLayout *gridLayout_3;
    QLabel *label_4;
    QDoubleSpinBox *move_dx;
    QLabel *label_5;
    QLabel *label_6;
    QDoubleSpinBox *move_dy;
    QDoubleSpinBox *move_dz;
    QPushButton *move_button;
    QLabel *label_scale_3;
    QFrame *frame_3;
    QWidget *gridLayoutWidget_3;
    QGridLayout *gridLayout_4;
    QDoubleSpinBox *rotate_angle_y;
    QLabel *label_7;
    QLabel *label_8;
    QDoubleSpinBox *rotate_angle_x;
    QLabel *label_9;
    QDoubleSpinBox *rotate_angle_z;
    QPushButton *rotate_button;
    QStatusBar *statusbar;
    QMenuBar *menubar;
    QMenu *menu;
    QMenu *menu_2;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1184, 611);
        choose_file = new QAction(MainWindow);
        choose_file->setObjectName(QString::fromUtf8("choose_file"));
        info_about_file = new QAction(MainWindow);
        info_about_file->setObjectName(QString::fromUtf8("info_about_file"));
        info_about_program = new QAction(MainWindow);
        info_about_program->setObjectName(QString::fromUtf8("info_about_program"));
        info_about_developer = new QAction(MainWindow);
        info_about_developer->setObjectName(QString::fromUtf8("info_about_developer"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        graphicsView = new QGraphicsView(centralwidget);
        graphicsView->setObjectName(QString::fromUtf8("graphicsView"));
        graphicsView->setGeometry(QRect(340, 0, 841, 561));
        QFont font;
        font.setStrikeOut(true);
        graphicsView->setFont(font);
        frame = new QFrame(centralwidget);
        frame->setObjectName(QString::fromUtf8("frame"));
        frame->setGeometry(QRect(0, 40, 341, 91));
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        gridLayoutWidget = new QWidget(frame);
        gridLayoutWidget->setObjectName(QString::fromUtf8("gridLayoutWidget"));
        gridLayoutWidget->setGeometry(QRect(0, 0, 341, 91));
        gridLayout_2 = new QGridLayout(gridLayoutWidget);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        label_3 = new QLabel(gridLayoutWidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        QFont font1;
        font1.setFamily(QString::fromUtf8("Courier New"));
        font1.setPointSize(14);
        font1.setBold(true);
        label_3->setFont(font1);
        label_3->setAlignment(Qt::AlignCenter);

        gridLayout_2->addWidget(label_3, 1, 1, 1, 1);

        kx = new QDoubleSpinBox(gridLayoutWidget);
        kx->setObjectName(QString::fromUtf8("kx"));

        gridLayout_2->addWidget(kx, 2, 0, 1, 1);

        label = new QLabel(gridLayoutWidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setFont(font1);
        label->setAlignment(Qt::AlignCenter);

        gridLayout_2->addWidget(label, 1, 2, 1, 1);

        label_2 = new QLabel(gridLayoutWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setFont(font1);
        label_2->setAlignment(Qt::AlignCenter);

        gridLayout_2->addWidget(label_2, 1, 0, 1, 1);

        ky = new QDoubleSpinBox(gridLayoutWidget);
        ky->setObjectName(QString::fromUtf8("ky"));

        gridLayout_2->addWidget(ky, 2, 1, 1, 1);

        kz = new QDoubleSpinBox(gridLayoutWidget);
        kz->setObjectName(QString::fromUtf8("kz"));

        gridLayout_2->addWidget(kz, 2, 2, 1, 1);

        scale_button = new QPushButton(gridLayoutWidget);
        scale_button->setObjectName(QString::fromUtf8("scale_button"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(scale_button->sizePolicy().hasHeightForWidth());
        scale_button->setSizePolicy(sizePolicy);
        scale_button->setMaximumSize(QSize(16777212, 16777215));
        scale_button->setSizeIncrement(QSize(0, 3));
        QFont font2;
        font2.setFamily(QString::fromUtf8("Courier New"));
        font2.setPointSize(14);
        scale_button->setFont(font2);
        scale_button->setAutoDefault(false);
        scale_button->setFlat(false);

        gridLayout_2->addWidget(scale_button, 3, 0, 1, 3);

        label_scale = new QLabel(centralwidget);
        label_scale->setObjectName(QString::fromUtf8("label_scale"));
        label_scale->setGeometry(QRect(10, 10, 321, 31));
        QFont font3;
        font3.setFamily(QString::fromUtf8("Courier New"));
        font3.setPointSize(21);
        font3.setBold(true);
        font3.setUnderline(true);
        label_scale->setFont(font3);
        label_scale->setScaledContents(false);
        label_scale->setAlignment(Qt::AlignCenter);
        label_scale_2 = new QLabel(centralwidget);
        label_scale_2->setObjectName(QString::fromUtf8("label_scale_2"));
        label_scale_2->setGeometry(QRect(10, 150, 321, 31));
        label_scale_2->setFont(font3);
        label_scale_2->setScaledContents(false);
        label_scale_2->setAlignment(Qt::AlignCenter);
        frame_2 = new QFrame(centralwidget);
        frame_2->setObjectName(QString::fromUtf8("frame_2"));
        frame_2->setGeometry(QRect(0, 180, 341, 91));
        frame_2->setFrameShape(QFrame::StyledPanel);
        frame_2->setFrameShadow(QFrame::Raised);
        gridLayoutWidget_2 = new QWidget(frame_2);
        gridLayoutWidget_2->setObjectName(QString::fromUtf8("gridLayoutWidget_2"));
        gridLayoutWidget_2->setGeometry(QRect(0, 0, 341, 106));
        gridLayout_3 = new QGridLayout(gridLayoutWidget_2);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        gridLayout_3->setContentsMargins(0, 0, 0, 0);
        label_4 = new QLabel(gridLayoutWidget_2);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setFont(font1);
        label_4->setAlignment(Qt::AlignCenter);

        gridLayout_3->addWidget(label_4, 1, 1, 1, 1);

        move_dx = new QDoubleSpinBox(gridLayoutWidget_2);
        move_dx->setObjectName(QString::fromUtf8("move_dx"));

        gridLayout_3->addWidget(move_dx, 2, 0, 1, 1);

        label_5 = new QLabel(gridLayoutWidget_2);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setFont(font1);
        label_5->setAlignment(Qt::AlignCenter);

        gridLayout_3->addWidget(label_5, 1, 2, 1, 1);

        label_6 = new QLabel(gridLayoutWidget_2);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setFont(font1);
        label_6->setAlignment(Qt::AlignCenter);

        gridLayout_3->addWidget(label_6, 1, 0, 1, 1);

        move_dy = new QDoubleSpinBox(gridLayoutWidget_2);
        move_dy->setObjectName(QString::fromUtf8("move_dy"));

        gridLayout_3->addWidget(move_dy, 2, 1, 1, 1);

        move_dz = new QDoubleSpinBox(gridLayoutWidget_2);
        move_dz->setObjectName(QString::fromUtf8("move_dz"));

        gridLayout_3->addWidget(move_dz, 2, 2, 1, 1);

        move_button = new QPushButton(gridLayoutWidget_2);
        move_button->setObjectName(QString::fromUtf8("move_button"));
        sizePolicy.setHeightForWidth(move_button->sizePolicy().hasHeightForWidth());
        move_button->setSizePolicy(sizePolicy);
        move_button->setMaximumSize(QSize(16777212, 16777215));
        move_button->setSizeIncrement(QSize(0, 3));
        move_button->setFont(font2);
        move_button->setAutoDefault(false);
        move_button->setFlat(false);

        gridLayout_3->addWidget(move_button, 3, 0, 1, 3);

        label_scale_3 = new QLabel(centralwidget);
        label_scale_3->setObjectName(QString::fromUtf8("label_scale_3"));
        label_scale_3->setGeometry(QRect(10, 290, 321, 31));
        label_scale_3->setFont(font3);
        label_scale_3->setScaledContents(false);
        label_scale_3->setAlignment(Qt::AlignCenter);
        frame_3 = new QFrame(centralwidget);
        frame_3->setObjectName(QString::fromUtf8("frame_3"));
        frame_3->setGeometry(QRect(0, 320, 341, 91));
        frame_3->setFrameShape(QFrame::StyledPanel);
        frame_3->setFrameShadow(QFrame::Raised);
        gridLayoutWidget_3 = new QWidget(frame_3);
        gridLayoutWidget_3->setObjectName(QString::fromUtf8("gridLayoutWidget_3"));
        gridLayoutWidget_3->setGeometry(QRect(0, -5, 341, 106));
        gridLayout_4 = new QGridLayout(gridLayoutWidget_3);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        gridLayout_4->setContentsMargins(0, 0, 0, 0);
        rotate_angle_y = new QDoubleSpinBox(gridLayoutWidget_3);
        rotate_angle_y->setObjectName(QString::fromUtf8("rotate_angle_y"));

        gridLayout_4->addWidget(rotate_angle_y, 2, 1, 1, 1);

        label_7 = new QLabel(gridLayoutWidget_3);
        label_7->setObjectName(QString::fromUtf8("label_7"));
        label_7->setFont(font1);
        label_7->setAlignment(Qt::AlignCenter);

        gridLayout_4->addWidget(label_7, 1, 1, 1, 1);

        label_8 = new QLabel(gridLayoutWidget_3);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        label_8->setFont(font1);
        label_8->setAlignment(Qt::AlignCenter);

        gridLayout_4->addWidget(label_8, 1, 2, 1, 1);

        rotate_angle_x = new QDoubleSpinBox(gridLayoutWidget_3);
        rotate_angle_x->setObjectName(QString::fromUtf8("rotate_angle_x"));

        gridLayout_4->addWidget(rotate_angle_x, 2, 0, 1, 1);

        label_9 = new QLabel(gridLayoutWidget_3);
        label_9->setObjectName(QString::fromUtf8("label_9"));
        label_9->setFont(font1);
        label_9->setAlignment(Qt::AlignCenter);

        gridLayout_4->addWidget(label_9, 1, 0, 1, 1);

        rotate_angle_z = new QDoubleSpinBox(gridLayoutWidget_3);
        rotate_angle_z->setObjectName(QString::fromUtf8("rotate_angle_z"));

        gridLayout_4->addWidget(rotate_angle_z, 2, 2, 1, 1);

        rotate_button = new QPushButton(gridLayoutWidget_3);
        rotate_button->setObjectName(QString::fromUtf8("rotate_button"));
        sizePolicy.setHeightForWidth(rotate_button->sizePolicy().hasHeightForWidth());
        rotate_button->setSizePolicy(sizePolicy);
        rotate_button->setMaximumSize(QSize(16777212, 16777215));
        rotate_button->setSizeIncrement(QSize(0, 3));
        rotate_button->setFont(font2);
        rotate_button->setAutoDefault(false);
        rotate_button->setFlat(false);

        gridLayout_4->addWidget(rotate_button, 3, 0, 1, 3);

        MainWindow->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 1184, 25));
        menu = new QMenu(menubar);
        menu->setObjectName(QString::fromUtf8("menu"));
        menu_2 = new QMenu(menubar);
        menu_2->setObjectName(QString::fromUtf8("menu_2"));
        MainWindow->setMenuBar(menubar);

        menubar->addAction(menu->menuAction());
        menubar->addAction(menu_2->menuAction());
        menu->addAction(choose_file);
        menu->addAction(info_about_file);
        menu_2->addAction(info_about_program);
        menu_2->addAction(info_about_developer);

        retranslateUi(MainWindow);

        scale_button->setDefault(false);
        move_button->setDefault(false);
        rotate_button->setDefault(false);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        choose_file->setText(QCoreApplication::translate("MainWindow", "\320\222\321\213\320\261\321\200\320\260\321\202\321\214 \321\204\320\260\320\271\320\273", nullptr));
        info_about_file->setText(QCoreApplication::translate("MainWindow", "\320\230\320\275\321\204\320\276\321\200\320\274\320\260\321\206\320\270\321\217 \320\276 \321\204\320\260\320\271\320\273\320\265", nullptr));
        info_about_program->setText(QCoreApplication::translate("MainWindow", "\320\230\320\275\321\204\320\276\321\200\320\274\320\260\321\206\320\270\321\217 \320\276 \320\277\321\200\320\276\320\263\321\200\320\260\320\274\320\274\320\265", nullptr));
        info_about_developer->setText(QCoreApplication::translate("MainWindow", "\320\230\320\275\321\204\320\276\321\200\320\274\320\260\321\206\320\270\321\217 \320\276 \321\200\320\260\320\267\321\200\320\260\320\261\320\276\321\202\321\207\320\270\320\272\320\265", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "ky", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "kz", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "kx", nullptr));
        scale_button->setText(QCoreApplication::translate("MainWindow", "\320\234\320\260\321\201\321\210\321\202\320\260\320\261\320\270\321\200\320\276\320\262\320\260\321\202\321\214", nullptr));
        label_scale->setText(QCoreApplication::translate("MainWindow", "\320\234\320\260\321\201\321\210\321\202\320\260\320\261\320\270\321\200\320\276\320\262\320\260\320\275\320\270\320\265", nullptr));
        label_scale_2->setText(QCoreApplication::translate("MainWindow", "\320\237\320\265\321\200\320\265\320\275\320\276\321\201", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "dy", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "dz", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "dx", nullptr));
        move_button->setText(QCoreApplication::translate("MainWindow", "\320\237\320\265\321\200\320\265\320\275\320\265\321\201\321\202\320\270", nullptr));
        label_scale_3->setText(QCoreApplication::translate("MainWindow", "\320\237\320\276\320\262\320\276\321\200\320\276\321\202", nullptr));
        label_7->setText(QCoreApplication::translate("MainWindow", "angle_y", nullptr));
        label_8->setText(QCoreApplication::translate("MainWindow", "angle_z", nullptr));
        label_9->setText(QCoreApplication::translate("MainWindow", "angle_x", nullptr));
        rotate_button->setText(QCoreApplication::translate("MainWindow", "\320\237\320\276\320\262\320\265\321\200\320\275\321\203\321\202\321\214", nullptr));
        menu->setTitle(QCoreApplication::translate("MainWindow", "\320\244\320\260\320\271\320\273", nullptr));
        menu_2->setTitle(QCoreApplication::translate("MainWindow", "\320\241\320\277\321\200\320\260\320\262\320\272\320\260", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
