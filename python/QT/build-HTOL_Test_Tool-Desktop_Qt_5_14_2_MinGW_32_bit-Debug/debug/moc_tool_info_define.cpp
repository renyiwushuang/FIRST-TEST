/****************************************************************************
** Meta object code from reading C++ file 'tool_info_define.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.14.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../HTOL_Tool_V0.2.7/device_define/tool_info_define.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'tool_info_define.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.14.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_VToolInfoEnum_t {
    QByteArrayData data[16];
    char stringdata0[177];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_VToolInfoEnum_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_VToolInfoEnum_t qt_meta_stringdata_VToolInfoEnum = {
    {
QT_MOC_LITERAL(0, 0, 13), // "VToolInfoEnum"
QT_MOC_LITERAL(1, 14, 12), // "enToolDomain"
QT_MOC_LITERAL(2, 27, 3), // "BLE"
QT_MOC_LITERAL(3, 31, 3), // "UWB"
QT_MOC_LITERAL(4, 35, 10), // "enToolType"
QT_MOC_LITERAL(5, 46, 2), // "PC"
QT_MOC_LITERAL(6, 49, 3), // "APP"
QT_MOC_LITERAL(7, 53, 17), // "enToolForChipType"
QT_MOC_LITERAL(8, 71, 7), // "MXD265X"
QT_MOC_LITERAL(9, 79, 7), // "MXD266X"
QT_MOC_LITERAL(10, 87, 7), // "MXD267X"
QT_MOC_LITERAL(11, 95, 7), // "MXD271X"
QT_MOC_LITERAL(12, 103, 24), // "enToolForApplicationType"
QT_MOC_LITERAL(13, 128, 15), // "MCU_APPLICATION"
QT_MOC_LITERAL(14, 144, 16), // "TEST_APPLICATION"
QT_MOC_LITERAL(15, 161, 15) // "APP_APPLICATION"

    },
    "VToolInfoEnum\0enToolDomain\0BLE\0UWB\0"
    "enToolType\0PC\0APP\0enToolForChipType\0"
    "MXD265X\0MXD266X\0MXD267X\0MXD271X\0"
    "enToolForApplicationType\0MCU_APPLICATION\0"
    "TEST_APPLICATION\0APP_APPLICATION"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_VToolInfoEnum[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       0,    0, // methods
       0,    0, // properties
       4,   14, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // enums: name, alias, flags, count, data
       1,    1, 0x0,    2,   34,
       4,    4, 0x0,    2,   38,
       7,    7, 0x0,    4,   42,
      12,   12, 0x0,    3,   50,

 // enum data: key, value
       2, uint(VToolInfoEnum::BLE),
       3, uint(VToolInfoEnum::UWB),
       5, uint(VToolInfoEnum::PC),
       6, uint(VToolInfoEnum::APP),
       8, uint(VToolInfoEnum::MXD265X),
       9, uint(VToolInfoEnum::MXD266X),
      10, uint(VToolInfoEnum::MXD267X),
      11, uint(VToolInfoEnum::MXD271X),
      13, uint(VToolInfoEnum::MCU_APPLICATION),
      14, uint(VToolInfoEnum::TEST_APPLICATION),
      15, uint(VToolInfoEnum::APP_APPLICATION),

       0        // eod
};

void VToolInfoEnum::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    Q_UNUSED(_o);
    Q_UNUSED(_id);
    Q_UNUSED(_c);
    Q_UNUSED(_a);
}

QT_INIT_METAOBJECT const QMetaObject VToolInfoEnum::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_VToolInfoEnum.data,
    qt_meta_data_VToolInfoEnum,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *VToolInfoEnum::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *VToolInfoEnum::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_VToolInfoEnum.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int VToolInfoEnum::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
