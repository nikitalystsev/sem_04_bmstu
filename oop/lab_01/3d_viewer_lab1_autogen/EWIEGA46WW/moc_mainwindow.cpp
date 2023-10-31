/****************************************************************************
** Meta object code from reading C++ file 'mainwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../mainwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mainwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_MainWindow_t {
    QByteArrayData data[11];
    char stringdata0[217];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_MainWindow_t qt_meta_stringdata_MainWindow = {
    {
QT_MOC_LITERAL(0, 0, 10), // "MainWindow"
QT_MOC_LITERAL(1, 11, 4), // "draw"
QT_MOC_LITERAL(2, 16, 7), // "error_t"
QT_MOC_LITERAL(3, 24, 0), // ""
QT_MOC_LITERAL(4, 25, 28), // "on_info_about_file_triggered"
QT_MOC_LITERAL(5, 54, 31), // "on_info_about_program_triggered"
QT_MOC_LITERAL(6, 86, 33), // "on_info_about_developer_trigg..."
QT_MOC_LITERAL(7, 120, 24), // "on_choose_file_triggered"
QT_MOC_LITERAL(8, 145, 22), // "on_move_button_clicked"
QT_MOC_LITERAL(9, 168, 24), // "on_rotate_button_clicked"
QT_MOC_LITERAL(10, 193, 23) // "on_scale_button_clicked"

    },
    "MainWindow\0draw\0error_t\0\0"
    "on_info_about_file_triggered\0"
    "on_info_about_program_triggered\0"
    "on_info_about_developer_triggered\0"
    "on_choose_file_triggered\0"
    "on_move_button_clicked\0on_rotate_button_clicked\0"
    "on_scale_button_clicked"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_MainWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   54,    3, 0x08 /* Private */,
       4,    0,   55,    3, 0x08 /* Private */,
       5,    0,   56,    3, 0x08 /* Private */,
       6,    0,   57,    3, 0x08 /* Private */,
       7,    0,   58,    3, 0x08 /* Private */,
       8,    0,   59,    3, 0x08 /* Private */,
       9,    0,   60,    3, 0x08 /* Private */,
      10,    0,   61,    3, 0x08 /* Private */,

 // slots: parameters
    0x80000000 | 2,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<MainWindow *>(_o);
        (void)_t;
        switch (_id) {
        case 0: { error_t _r = _t->draw();
            if (_a[0]) *reinterpret_cast< error_t*>(_a[0]) = std::move(_r); }  break;
        case 1: _t->on_info_about_file_triggered(); break;
        case 2: _t->on_info_about_program_triggered(); break;
        case 3: _t->on_info_about_developer_triggered(); break;
        case 4: _t->on_choose_file_triggered(); break;
        case 5: _t->on_move_button_clicked(); break;
        case 6: _t->on_rotate_button_clicked(); break;
        case 7: _t->on_scale_button_clicked(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject MainWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_meta_stringdata_MainWindow.data,
    qt_meta_data_MainWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *MainWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MainWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_MainWindow.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int MainWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 8;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
