/****************************************************************************
** Meta object code from reading C++ file 'thread_freq_accuracy.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.14.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../HTOL_Tool_V0.2.7/tools/thread_freq_accuracy.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'thread_freq_accuracy.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.14.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_thread_freq_accuracy_t {
    QByteArrayData data[10];
    char stringdata0[184];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_thread_freq_accuracy_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_thread_freq_accuracy_t qt_meta_stringdata_thread_freq_accuracy = {
    {
QT_MOC_LITERAL(0, 0, 20), // "thread_freq_accuracy"
QT_MOC_LITERAL(1, 21, 25), // "sigl_tcp_send_control_cmd"
QT_MOC_LITERAL(2, 47, 0), // ""
QT_MOC_LITERAL(3, 48, 20), // "sigl_serial_send_cmd"
QT_MOC_LITERAL(4, 69, 7), // "uint8_t"
QT_MOC_LITERAL(5, 77, 8), // "uint16_t"
QT_MOC_LITERAL(6, 86, 21), // "sigl_stop_freq_thread"
QT_MOC_LITERAL(7, 108, 30), // "sigl_display_freq_accuracy_log"
QT_MOC_LITERAL(8, 139, 22), // "sigl_set_process_value"
QT_MOC_LITERAL(9, 162, 21) // "sigl_display_warnning"

    },
    "thread_freq_accuracy\0sigl_tcp_send_control_cmd\0"
    "\0sigl_serial_send_cmd\0uint8_t\0uint16_t\0"
    "sigl_stop_freq_thread\0"
    "sigl_display_freq_accuracy_log\0"
    "sigl_set_process_value\0sigl_display_warnning"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_thread_freq_accuracy[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       6,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       6,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   44,    2, 0x06 /* Public */,
       3,    2,   47,    2, 0x06 /* Public */,
       6,    0,   52,    2, 0x06 /* Public */,
       7,    1,   53,    2, 0x06 /* Public */,
       8,    1,   56,    2, 0x06 /* Public */,
       9,    1,   59,    2, 0x06 /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    2,
    QMetaType::Void, 0x80000000 | 4, 0x80000000 | 5,    2,    2,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    2,
    QMetaType::Void, QMetaType::Int,    2,
    QMetaType::Void, QMetaType::QString,    2,

       0        // eod
};

void thread_freq_accuracy::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<thread_freq_accuracy *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->sigl_tcp_send_control_cmd((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->sigl_serial_send_cmd((*reinterpret_cast< uint8_t(*)>(_a[1])),(*reinterpret_cast< uint16_t(*)>(_a[2]))); break;
        case 2: _t->sigl_stop_freq_thread(); break;
        case 3: _t->sigl_display_freq_accuracy_log((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 4: _t->sigl_set_process_value((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->sigl_display_warnning((*reinterpret_cast< QString(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (thread_freq_accuracy::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&thread_freq_accuracy::sigl_tcp_send_control_cmd)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (thread_freq_accuracy::*)(uint8_t , uint16_t );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&thread_freq_accuracy::sigl_serial_send_cmd)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (thread_freq_accuracy::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&thread_freq_accuracy::sigl_stop_freq_thread)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (thread_freq_accuracy::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&thread_freq_accuracy::sigl_display_freq_accuracy_log)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (thread_freq_accuracy::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&thread_freq_accuracy::sigl_set_process_value)) {
                *result = 4;
                return;
            }
        }
        {
            using _t = void (thread_freq_accuracy::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&thread_freq_accuracy::sigl_display_warnning)) {
                *result = 5;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject thread_freq_accuracy::staticMetaObject = { {
    QMetaObject::SuperData::link<QThread::staticMetaObject>(),
    qt_meta_stringdata_thread_freq_accuracy.data,
    qt_meta_data_thread_freq_accuracy,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *thread_freq_accuracy::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *thread_freq_accuracy::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_thread_freq_accuracy.stringdata0))
        return static_cast<void*>(this);
    return QThread::qt_metacast(_clname);
}

int thread_freq_accuracy::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QThread::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 6)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 6;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 6)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 6;
    }
    return _id;
}

// SIGNAL 0
void thread_freq_accuracy::sigl_tcp_send_control_cmd(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void thread_freq_accuracy::sigl_serial_send_cmd(uint8_t _t1, uint16_t _t2)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void thread_freq_accuracy::sigl_stop_freq_thread()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}

// SIGNAL 3
void thread_freq_accuracy::sigl_display_freq_accuracy_log(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}

// SIGNAL 4
void thread_freq_accuracy::sigl_set_process_value(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 4, _a);
}

// SIGNAL 5
void thread_freq_accuracy::sigl_display_warnning(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 5, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
