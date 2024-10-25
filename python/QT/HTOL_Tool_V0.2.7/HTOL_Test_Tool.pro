QT       += core gui
QT       += serialport
QT       += network
QT       += multimedia


greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

#release版本可调试
QMAKE_CXXFLAGS_RELEASE += $$QMAKE_CFLAGS_RELEASE_WITH_DEBUGINFO
QMAKE_LFLAGS_RELEASE = $$QMAKE_LFLAGS_RELEASE_WITH_DEBUGINFO
#release版也将生成“.pdb”后缀的调试信息文件
#QMAKE_LFLAGS_RELEASE = /INCREMENTAL:NO /DEBUG
#调用库
LIBS += -lDbgHelp


# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    Intermediate_communication_protocol/communication_common.cpp \
    Intermediate_communication_protocol/communication_protcol.cpp \
    Intermediate_communication_protocol/protocol_crc.cpp \
    Intermediate_communication_protocol/test_ctlr_procotol.cpp \
    Intermediate_memory_management/common_data_conversion.cpp \
    Intermediate_memory_management/communication_memory_manager.cpp \
    device_processing/qt_custom_combobox_net.cpp \
    device_processing/qt_custom_combobox_uart.cpp \
    device_processing/qt_custom_label.cpp \
    device_processing/send_email.cpp \
    device_processing/time_operate.cpp \
    logical_data_processing/bin_file_parse.cpp \
    logical_data_processing/test_module_exception_handle.cpp \
    logical_thread_management/thread_recive_maxscend_device.cpp \
    logical_thread_management/thread_recive_script.cpp \
    main.cpp \
    mainwindow.cpp \
    tools/thread_freq_accuracy.cpp

HEADERS += \
    Intermediate_communication_protocol/communication_common.h \
    Intermediate_communication_protocol/communication_protcol.h \
    Intermediate_communication_protocol/protocol_crc.h \
    Intermediate_communication_protocol/test_ctlr_procotol.h \
    Intermediate_memory_management/common_data_conversion.h \
    Intermediate_memory_management/communication_memory_manager.h \
    device_define/tool_info_define.h \
    device_processing/qt_custom_combobox_net.h \
    device_processing/qt_custom_combobox_uart.h \
    device_processing/qt_custom_label.h \
    device_processing/send_email.h \
    device_processing/time_operate.h \
    logical_data_processing/bin_file_parse.h \
    logical_data_processing/test_module_exception_handle.h \
    logical_thread_management/thread_recive_maxscend_device.h \
    logical_thread_management/thread_recive_script.h \
    mainwindow.h \
    tools/thread_freq_accuracy.h

FORMS += \
    mainwindow.ui

TRANSLATIONS += \
    SOC_Intermediate_Verification_Test_System_zh_CN.ts

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    resources/UI_Sources.qrc \

#DISTFILES += \
#    mxdico.ico \
#    resources/edict_undo.png \
#    resources/fileexit.png \
#    resources/filenclose.png \
#    resources/filenew.png \
#    resources/fileopen.png \
#    resources/filesave.png \
#    resources/filesaveas.png \
#    resources/go-home.png \
#    resources/help-about.png \
#    resources/help-faq.png \
#    resources/help_guide.png \
#    resources/mxdico.ico \
#    resources/run_pause.png \
#    resources/run_start.png \
#    resources/run_stop.png \
#    resources/slider_handle_g.png \
#    resources/slider_handle_r.png \
#    resources/test_cofiger.png \
#    resources/test_manager.png
#应用图标
RC_ICONS  = mxdico.ico
#版本号
VERSION = 0.2
#中文
#RC_LANG = 0x0004
# 公司名
QMAKE_TARGET_COMPANY = Maxscend Microelectronics Co.,Ltd
# 产品名称
QMAKE_TARGET_PRODUCT = Htol Test Tool
# 详细描述
QMAKE_TARGET_DESCRIPTION = Htol Test Tool - A test tool for mxd htol test
# 版权
QMAKE_TARGET_COPYRIGHT = Copyright(C) 2023 Maxscend Microelectronics Co.,Ltd
