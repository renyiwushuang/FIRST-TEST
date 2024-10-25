/****************************************************************************
** Meta object code from reading C++ file 'mainwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.14.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../HTOL_Tool_V0.2.7/mainwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mainwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.14.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_MainWindow_t {
    QByteArrayData data[95];
    char stringdata0[2279];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_MainWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_MainWindow_t qt_meta_stringdata_MainWindow = {
    {
QT_MOC_LITERAL(0, 0, 10), // "MainWindow"
QT_MOC_LITERAL(1, 11, 24), // "sig_download_ack_timeout"
QT_MOC_LITERAL(2, 36, 0), // ""
QT_MOC_LITERAL(3, 37, 27), // "signal_system_exception_cfg"
QT_MOC_LITERAL(4, 65, 28), // "enSystemExceptionHandleCfg_t"
QT_MOC_LITERAL(5, 94, 20), // "system_exception_cfg"
QT_MOC_LITERAL(6, 115, 20), // "signal_system_reboot"
QT_MOC_LITERAL(7, 136, 16), // "log_action_clear"
QT_MOC_LITERAL(8, 153, 15), // "log_action_copy"
QT_MOC_LITERAL(9, 169, 21), // "log_action_select_all"
QT_MOC_LITERAL(10, 191, 20), // "log_action_save_file"
QT_MOC_LITERAL(11, 212, 32), // "auto_test_recive_timeout_handler"
QT_MOC_LITERAL(12, 245, 24), // "on_test_config_triggered"
QT_MOC_LITERAL(13, 270, 25), // "on_test_manager_triggered"
QT_MOC_LITERAL(14, 296, 20), // "test_led_status_init"
QT_MOC_LITERAL(15, 317, 19), // "test_led_group_init"
QT_MOC_LITERAL(16, 337, 24), // "indicate_test_status_led"
QT_MOC_LITERAL(17, 362, 7), // "uint8_t"
QT_MOC_LITERAL(18, 370, 12), // "testModuleID"
QT_MOC_LITERAL(19, 383, 10), // "testResult"
QT_MOC_LITERAL(20, 394, 25), // "read_configer_serial_data"
QT_MOC_LITERAL(21, 420, 25), // "read_test_run_serial_data"
QT_MOC_LITERAL(22, 446, 26), // "write_configer_serial_data"
QT_MOC_LITERAL(23, 473, 10), // "sendBuffer"
QT_MOC_LITERAL(24, 484, 26), // "write_test_run_serial_data"
QT_MOC_LITERAL(25, 511, 9), // "open_uart"
QT_MOC_LITERAL(26, 521, 10), // "u8UartType"
QT_MOC_LITERAL(27, 532, 10), // "close_uart"
QT_MOC_LITERAL(28, 543, 28), // "on_runUarttoolButton_clicked"
QT_MOC_LITERAL(29, 572, 33), // "on_configerUartToolButton_cli..."
QT_MOC_LITERAL(30, 606, 23), // "read_freq_spec_tcp_data"
QT_MOC_LITERAL(31, 630, 26), // "read_digtal_power_tcp_data"
QT_MOC_LITERAL(32, 657, 28), // "read_digtal_voltage_tcp_data"
QT_MOC_LITERAL(33, 686, 32), // "read_digtal_electricity_tcp_data"
QT_MOC_LITERAL(34, 719, 35), // "slot_write_ins_freq_accuracy_..."
QT_MOC_LITERAL(35, 755, 27), // "write_digtal_power_tcp_data"
QT_MOC_LITERAL(36, 783, 29), // "write_digtal_voltage_tcp_data"
QT_MOC_LITERAL(37, 813, 33), // "write_digtal_electricity_tcp_..."
QT_MOC_LITERAL(38, 847, 11), // "open_client"
QT_MOC_LITERAL(39, 859, 12), // "u8ClientType"
QT_MOC_LITERAL(40, 872, 12), // "close_client"
QT_MOC_LITERAL(41, 885, 32), // "on_digtalPowerToolButton_clicked"
QT_MOC_LITERAL(42, 918, 37), // "on_digtaElectricityToolButton..."
QT_MOC_LITERAL(43, 956, 33), // "on_digtaVoltageToolButton_cli..."
QT_MOC_LITERAL(44, 990, 19), // "test_mode_ctrl_init"
QT_MOC_LITERAL(45, 1010, 21), // "Get_the_current_value"
QT_MOC_LITERAL(46, 1032, 21), // "set_adc_voltage_value"
QT_MOC_LITERAL(47, 1054, 12), // "voltageValue"
QT_MOC_LITERAL(48, 1067, 30), // "on_autoTestRadioButton_clicked"
QT_MOC_LITERAL(49, 1098, 29), // "mxd_serial_recive_data_handle"
QT_MOC_LITERAL(50, 1128, 24), // "stTestCtrlProcotolInfo_t"
QT_MOC_LITERAL(51, 1153, 14), // "testReturnInfo"
QT_MOC_LITERAL(52, 1168, 23), // "send_auto_test_cmd_data"
QT_MOC_LITERAL(53, 1192, 13), // "byteArrayTemp"
QT_MOC_LITERAL(54, 1206, 8), // "uint16_t"
QT_MOC_LITERAL(55, 1215, 7), // "timeout"
QT_MOC_LITERAL(56, 1223, 29), // "on_autoTestToolButton_clicked"
QT_MOC_LITERAL(57, 1253, 31), // "on_scripTestRadioButton_clicked"
QT_MOC_LITERAL(58, 1285, 20), // "read_tcp_socket_data"
QT_MOC_LITERAL(59, 1306, 21), // "write_tcp_socket_data"
QT_MOC_LITERAL(60, 1328, 11), // "send_buffer"
QT_MOC_LITERAL(61, 1340, 21), // "connect_script_server"
QT_MOC_LITERAL(62, 1362, 24), // "disconnect_script_server"
QT_MOC_LITERAL(63, 1387, 27), // "on_scriptToolButton_clicked"
QT_MOC_LITERAL(64, 1415, 33), // "on_ScriptSelectToolButton_cli..."
QT_MOC_LITERAL(65, 1449, 31), // "on_scriptTestToolButton_clicked"
QT_MOC_LITERAL(66, 1481, 25), // "on_checkBox_AllID_clicked"
QT_MOC_LITERAL(67, 1507, 7), // "checked"
QT_MOC_LITERAL(68, 1515, 28), // "slot_testCaseSelectionRecord"
QT_MOC_LITERAL(69, 1544, 14), // "TEST_CASE_TYPE"
QT_MOC_LITERAL(70, 1559, 30), // "on_radioButton_AllTest_clicked"
QT_MOC_LITERAL(71, 1590, 35), // "on_pushButton_TestInfoWrite_c..."
QT_MOC_LITERAL(72, 1626, 40), // "on_pushButton_DataSavePathBro..."
QT_MOC_LITERAL(73, 1667, 38), // "on_pushButton_SystemExcepWrit..."
QT_MOC_LITERAL(74, 1706, 33), // "on_pushButton_SaveCfgFile_cli..."
QT_MOC_LITERAL(75, 1740, 28), // "on_actionHelp_Guid_triggered"
QT_MOC_LITERAL(76, 1769, 31), // "on_actionsoft_Version_triggered"
QT_MOC_LITERAL(77, 1801, 32), // "on_toolButton_Write_Addr_clicked"
QT_MOC_LITERAL(78, 1834, 25), // "on_FreqSpecButton_clicked"
QT_MOC_LITERAL(79, 1860, 30), // "on_FreqCalibrateButton_clicked"
QT_MOC_LITERAL(80, 1891, 24), // "on_dfu_setting_triggered"
QT_MOC_LITERAL(81, 1916, 23), // "on_firmwareLoad_clicked"
QT_MOC_LITERAL(82, 1940, 29), // "on_firmware_recognize_clicked"
QT_MOC_LITERAL(83, 1970, 29), // "on_chipInfo_recognize_clicked"
QT_MOC_LITERAL(84, 2000, 34), // "on_pushButton_startUpgrade_cl..."
QT_MOC_LITERAL(85, 2035, 37), // "on_pushButton_startUpgradeAll..."
QT_MOC_LITERAL(86, 2073, 33), // "on_pushButton_stopUpgrade_cli..."
QT_MOC_LITERAL(87, 2107, 40), // "slot_set_progressBar_freq_acc..."
QT_MOC_LITERAL(88, 2148, 5), // "value"
QT_MOC_LITERAL(89, 2154, 26), // "slot_textEdit_Log_Warnning"
QT_MOC_LITERAL(90, 2181, 7), // "display"
QT_MOC_LITERAL(91, 2189, 25), // "slot_textEdit_Log_setText"
QT_MOC_LITERAL(92, 2215, 29), // "slot_freq_accracy_stop_thread"
QT_MOC_LITERAL(93, 2245, 29), // "slot_send_freq_accracy_serial"
QT_MOC_LITERAL(94, 2275, 3) // "cmd"

    },
    "MainWindow\0sig_download_ack_timeout\0"
    "\0signal_system_exception_cfg\0"
    "enSystemExceptionHandleCfg_t\0"
    "system_exception_cfg\0signal_system_reboot\0"
    "log_action_clear\0log_action_copy\0"
    "log_action_select_all\0log_action_save_file\0"
    "auto_test_recive_timeout_handler\0"
    "on_test_config_triggered\0"
    "on_test_manager_triggered\0"
    "test_led_status_init\0test_led_group_init\0"
    "indicate_test_status_led\0uint8_t\0"
    "testModuleID\0testResult\0"
    "read_configer_serial_data\0"
    "read_test_run_serial_data\0"
    "write_configer_serial_data\0sendBuffer\0"
    "write_test_run_serial_data\0open_uart\0"
    "u8UartType\0close_uart\0"
    "on_runUarttoolButton_clicked\0"
    "on_configerUartToolButton_clicked\0"
    "read_freq_spec_tcp_data\0"
    "read_digtal_power_tcp_data\0"
    "read_digtal_voltage_tcp_data\0"
    "read_digtal_electricity_tcp_data\0"
    "slot_write_ins_freq_accuracy_client\0"
    "write_digtal_power_tcp_data\0"
    "write_digtal_voltage_tcp_data\0"
    "write_digtal_electricity_tcp_data\0"
    "open_client\0u8ClientType\0close_client\0"
    "on_digtalPowerToolButton_clicked\0"
    "on_digtaElectricityToolButton_clicked\0"
    "on_digtaVoltageToolButton_clicked\0"
    "test_mode_ctrl_init\0Get_the_current_value\0"
    "set_adc_voltage_value\0voltageValue\0"
    "on_autoTestRadioButton_clicked\0"
    "mxd_serial_recive_data_handle\0"
    "stTestCtrlProcotolInfo_t\0testReturnInfo\0"
    "send_auto_test_cmd_data\0byteArrayTemp\0"
    "uint16_t\0timeout\0on_autoTestToolButton_clicked\0"
    "on_scripTestRadioButton_clicked\0"
    "read_tcp_socket_data\0write_tcp_socket_data\0"
    "send_buffer\0connect_script_server\0"
    "disconnect_script_server\0"
    "on_scriptToolButton_clicked\0"
    "on_ScriptSelectToolButton_clicked\0"
    "on_scriptTestToolButton_clicked\0"
    "on_checkBox_AllID_clicked\0checked\0"
    "slot_testCaseSelectionRecord\0"
    "TEST_CASE_TYPE\0on_radioButton_AllTest_clicked\0"
    "on_pushButton_TestInfoWrite_clicked\0"
    "on_pushButton_DataSavePathBrowse_clicked\0"
    "on_pushButton_SystemExcepWrite_clicked\0"
    "on_pushButton_SaveCfgFile_clicked\0"
    "on_actionHelp_Guid_triggered\0"
    "on_actionsoft_Version_triggered\0"
    "on_toolButton_Write_Addr_clicked\0"
    "on_FreqSpecButton_clicked\0"
    "on_FreqCalibrateButton_clicked\0"
    "on_dfu_setting_triggered\0"
    "on_firmwareLoad_clicked\0"
    "on_firmware_recognize_clicked\0"
    "on_chipInfo_recognize_clicked\0"
    "on_pushButton_startUpgrade_clicked\0"
    "on_pushButton_startUpgradeAll_clicked\0"
    "on_pushButton_stopUpgrade_clicked\0"
    "slot_set_progressBar_freq_accuracy_value\0"
    "value\0slot_textEdit_Log_Warnning\0"
    "display\0slot_textEdit_Log_setText\0"
    "slot_freq_accracy_stop_thread\0"
    "slot_send_freq_accracy_serial\0cmd"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_MainWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      73,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,  379,    2, 0x06 /* Public */,
       3,    1,  380,    2, 0x06 /* Public */,
       6,    0,  383,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       7,    0,  384,    2, 0x0a /* Public */,
       8,    0,  385,    2, 0x0a /* Public */,
       9,    0,  386,    2, 0x0a /* Public */,
      10,    0,  387,    2, 0x0a /* Public */,
      11,    0,  388,    2, 0x0a /* Public */,
      12,    0,  389,    2, 0x08 /* Private */,
      13,    0,  390,    2, 0x08 /* Private */,
      14,    0,  391,    2, 0x08 /* Private */,
      15,    0,  392,    2, 0x08 /* Private */,
      16,    2,  393,    2, 0x08 /* Private */,
      20,    0,  398,    2, 0x08 /* Private */,
      21,    0,  399,    2, 0x08 /* Private */,
      22,    1,  400,    2, 0x08 /* Private */,
      24,    1,  403,    2, 0x08 /* Private */,
      25,    1,  406,    2, 0x08 /* Private */,
      27,    1,  409,    2, 0x08 /* Private */,
      28,    0,  412,    2, 0x08 /* Private */,
      29,    0,  413,    2, 0x08 /* Private */,
      30,    0,  414,    2, 0x08 /* Private */,
      31,    0,  415,    2, 0x08 /* Private */,
      32,    0,  416,    2, 0x08 /* Private */,
      33,    0,  417,    2, 0x08 /* Private */,
      34,    1,  418,    2, 0x08 /* Private */,
      35,    1,  421,    2, 0x08 /* Private */,
      36,    1,  424,    2, 0x08 /* Private */,
      37,    1,  427,    2, 0x08 /* Private */,
      38,    1,  430,    2, 0x08 /* Private */,
      40,    1,  433,    2, 0x08 /* Private */,
      41,    0,  436,    2, 0x08 /* Private */,
      42,    0,  437,    2, 0x08 /* Private */,
      43,    0,  438,    2, 0x08 /* Private */,
      44,    0,  439,    2, 0x08 /* Private */,
      45,    0,  440,    2, 0x08 /* Private */,
      46,    1,  441,    2, 0x08 /* Private */,
      48,    0,  444,    2, 0x08 /* Private */,
      49,    1,  445,    2, 0x08 /* Private */,
      52,    2,  448,    2, 0x08 /* Private */,
      56,    0,  453,    2, 0x08 /* Private */,
      57,    0,  454,    2, 0x08 /* Private */,
      58,    0,  455,    2, 0x08 /* Private */,
      59,    1,  456,    2, 0x08 /* Private */,
      61,    0,  459,    2, 0x08 /* Private */,
      62,    0,  460,    2, 0x08 /* Private */,
      63,    0,  461,    2, 0x08 /* Private */,
      64,    0,  462,    2, 0x08 /* Private */,
      65,    0,  463,    2, 0x08 /* Private */,
      66,    1,  464,    2, 0x08 /* Private */,
      68,    2,  467,    2, 0x08 /* Private */,
      70,    1,  472,    2, 0x08 /* Private */,
      71,    0,  475,    2, 0x08 /* Private */,
      72,    0,  476,    2, 0x08 /* Private */,
      73,    0,  477,    2, 0x08 /* Private */,
      74,    0,  478,    2, 0x08 /* Private */,
      75,    0,  479,    2, 0x08 /* Private */,
      76,    0,  480,    2, 0x08 /* Private */,
      77,    0,  481,    2, 0x08 /* Private */,
      78,    0,  482,    2, 0x08 /* Private */,
      79,    0,  483,    2, 0x08 /* Private */,
      80,    0,  484,    2, 0x08 /* Private */,
      81,    0,  485,    2, 0x08 /* Private */,
      82,    0,  486,    2, 0x08 /* Private */,
      83,    0,  487,    2, 0x08 /* Private */,
      84,    0,  488,    2, 0x08 /* Private */,
      85,    0,  489,    2, 0x08 /* Private */,
      86,    0,  490,    2, 0x08 /* Private */,
      87,    1,  491,    2, 0x0a /* Public */,
      89,    1,  494,    2, 0x0a /* Public */,
      91,    1,  497,    2, 0x0a /* Public */,
      92,    0,  500,    2, 0x0a /* Public */,
      93,    2,  501,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 4,    5,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 17, 0x80000000 | 17,   18,   19,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QByteArray,   23,
    QMetaType::Void, QMetaType::QByteArray,   23,
    QMetaType::Bool, 0x80000000 | 17,   26,
    QMetaType::Bool, 0x80000000 | 17,   26,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,   23,
    QMetaType::Void, QMetaType::QByteArray,   23,
    QMetaType::Void, QMetaType::QByteArray,   23,
    QMetaType::Void, QMetaType::QByteArray,   23,
    QMetaType::Bool, 0x80000000 | 17,   39,
    QMetaType::Bool, 0x80000000 | 17,   39,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::QString,
    QMetaType::Void, QMetaType::Float,   47,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 50,   51,
    QMetaType::Bool, QMetaType::QByteArray, 0x80000000 | 54,   53,   55,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QByteArray,   60,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Bool,   67,
    QMetaType::Void, QMetaType::Int, QMetaType::Bool,   69,   67,
    QMetaType::Void, QMetaType::Bool,   67,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,   88,
    QMetaType::Void, QMetaType::QString,   90,
    QMetaType::Void, QMetaType::QString,   90,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 17, 0x80000000 | 54,   94,   88,

       0        // eod
};

void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<MainWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->sig_download_ack_timeout(); break;
        case 1: _t->signal_system_exception_cfg((*reinterpret_cast< enSystemExceptionHandleCfg_t(*)>(_a[1]))); break;
        case 2: _t->signal_system_reboot(); break;
        case 3: _t->log_action_clear(); break;
        case 4: _t->log_action_copy(); break;
        case 5: _t->log_action_select_all(); break;
        case 6: _t->log_action_save_file(); break;
        case 7: _t->auto_test_recive_timeout_handler(); break;
        case 8: _t->on_test_config_triggered(); break;
        case 9: _t->on_test_manager_triggered(); break;
        case 10: _t->test_led_status_init(); break;
        case 11: _t->test_led_group_init(); break;
        case 12: _t->indicate_test_status_led((*reinterpret_cast< uint8_t(*)>(_a[1])),(*reinterpret_cast< uint8_t(*)>(_a[2]))); break;
        case 13: _t->read_configer_serial_data(); break;
        case 14: _t->read_test_run_serial_data(); break;
        case 15: _t->write_configer_serial_data((*reinterpret_cast< QByteArray(*)>(_a[1]))); break;
        case 16: _t->write_test_run_serial_data((*reinterpret_cast< QByteArray(*)>(_a[1]))); break;
        case 17: { bool _r = _t->open_uart((*reinterpret_cast< uint8_t(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 18: { bool _r = _t->close_uart((*reinterpret_cast< uint8_t(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 19: _t->on_runUarttoolButton_clicked(); break;
        case 20: _t->on_configerUartToolButton_clicked(); break;
        case 21: _t->read_freq_spec_tcp_data(); break;
        case 22: _t->read_digtal_power_tcp_data(); break;
        case 23: _t->read_digtal_voltage_tcp_data(); break;
        case 24: _t->read_digtal_electricity_tcp_data(); break;
        case 25: _t->slot_write_ins_freq_accuracy_client((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 26: _t->write_digtal_power_tcp_data((*reinterpret_cast< QByteArray(*)>(_a[1]))); break;
        case 27: _t->write_digtal_voltage_tcp_data((*reinterpret_cast< QByteArray(*)>(_a[1]))); break;
        case 28: _t->write_digtal_electricity_tcp_data((*reinterpret_cast< QByteArray(*)>(_a[1]))); break;
        case 29: { bool _r = _t->open_client((*reinterpret_cast< uint8_t(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 30: { bool _r = _t->close_client((*reinterpret_cast< uint8_t(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 31: _t->on_digtalPowerToolButton_clicked(); break;
        case 32: _t->on_digtaElectricityToolButton_clicked(); break;
        case 33: _t->on_digtaVoltageToolButton_clicked(); break;
        case 34: _t->test_mode_ctrl_init(); break;
        case 35: { QString _r = _t->Get_the_current_value();
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 36: _t->set_adc_voltage_value((*reinterpret_cast< float(*)>(_a[1]))); break;
        case 37: _t->on_autoTestRadioButton_clicked(); break;
        case 38: _t->mxd_serial_recive_data_handle((*reinterpret_cast< stTestCtrlProcotolInfo_t(*)>(_a[1]))); break;
        case 39: { bool _r = _t->send_auto_test_cmd_data((*reinterpret_cast< QByteArray(*)>(_a[1])),(*reinterpret_cast< uint16_t(*)>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 40: _t->on_autoTestToolButton_clicked(); break;
        case 41: _t->on_scripTestRadioButton_clicked(); break;
        case 42: _t->read_tcp_socket_data(); break;
        case 43: _t->write_tcp_socket_data((*reinterpret_cast< QByteArray(*)>(_a[1]))); break;
        case 44: _t->connect_script_server(); break;
        case 45: _t->disconnect_script_server(); break;
        case 46: _t->on_scriptToolButton_clicked(); break;
        case 47: _t->on_ScriptSelectToolButton_clicked(); break;
        case 48: _t->on_scriptTestToolButton_clicked(); break;
        case 49: _t->on_checkBox_AllID_clicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 50: _t->slot_testCaseSelectionRecord((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< bool(*)>(_a[2]))); break;
        case 51: _t->on_radioButton_AllTest_clicked((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 52: _t->on_pushButton_TestInfoWrite_clicked(); break;
        case 53: _t->on_pushButton_DataSavePathBrowse_clicked(); break;
        case 54: _t->on_pushButton_SystemExcepWrite_clicked(); break;
        case 55: _t->on_pushButton_SaveCfgFile_clicked(); break;
        case 56: _t->on_actionHelp_Guid_triggered(); break;
        case 57: _t->on_actionsoft_Version_triggered(); break;
        case 58: _t->on_toolButton_Write_Addr_clicked(); break;
        case 59: _t->on_FreqSpecButton_clicked(); break;
        case 60: _t->on_FreqCalibrateButton_clicked(); break;
        case 61: _t->on_dfu_setting_triggered(); break;
        case 62: _t->on_firmwareLoad_clicked(); break;
        case 63: _t->on_firmware_recognize_clicked(); break;
        case 64: _t->on_chipInfo_recognize_clicked(); break;
        case 65: _t->on_pushButton_startUpgrade_clicked(); break;
        case 66: _t->on_pushButton_startUpgradeAll_clicked(); break;
        case 67: _t->on_pushButton_stopUpgrade_clicked(); break;
        case 68: _t->slot_set_progressBar_freq_accuracy_value((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 69: _t->slot_textEdit_Log_Warnning((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 70: _t->slot_textEdit_Log_setText((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 71: _t->slot_freq_accracy_stop_thread(); break;
        case 72: _t->slot_send_freq_accracy_serial((*reinterpret_cast< uint8_t(*)>(_a[1])),(*reinterpret_cast< uint16_t(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (MainWindow::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&MainWindow::sig_download_ack_timeout)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (MainWindow::*)(enSystemExceptionHandleCfg_t );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&MainWindow::signal_system_exception_cfg)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (MainWindow::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&MainWindow::signal_system_reboot)) {
                *result = 2;
                return;
            }
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
        if (_id < 73)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 73;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 73)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 73;
    }
    return _id;
}

// SIGNAL 0
void MainWindow::sig_download_ack_timeout()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void MainWindow::signal_system_exception_cfg(enSystemExceptionHandleCfg_t _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void MainWindow::signal_system_reboot()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
