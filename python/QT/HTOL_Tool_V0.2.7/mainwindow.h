#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTreeWidget>
#include "qserialport.h"
#include "qtcpsocket.h"
#include "qtcpserver.h"
#include "device_processing/time_operate.h"
#include "device_processing/qt_custom_label.h"
#include "logical_data_processing/test_module_exception_handle.h"
#include "logical_thread_management/thread_recive_maxscend_device.h"
#include "device_define/tool_info_define.h"
#include "tools/thread_freq_accuracy.h"

#include <QButtonGroup>
#include <QSettings>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE


typedef enum
{
    TEST_STATUS_PASS,
    TEST_STATUS_RECIVE_TIMEOUT,
    TEST_STATUS_FAIL,
    TEST_STATUS_SECD_PASS,
    TEST_STATUS_SECD_FAIL,
    TEST_STATUS_SECD_RECIVE_TIMEOUT,
    TEST_STATUS_FAIL_NEXT_CASE,
    TEST_STATUS_FAIL_RESET_TEST_MODULE,
    TEST_STATUS_FAIL_NEXT_TEST_MODULE,
    TEST_STATUS_NO_TEST,

}enTestCaseReturnValue;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    QSerialPort *configerSerialPort         = nullptr;
    QSerialPort *testRunSerialPort          = nullptr;

    QTcpSocket* digtalPowerTcpClient        = nullptr;
    QTcpSocket* digtalVoltageTcpClient      = nullptr;
    QTcpSocket* digtalElectricityTcpClient  = nullptr;
    QTcpSocket* freqSpecTcpClient           = nullptr;

    QTcpSocket* scriptTcpSocket             = nullptr;
    QTcpServer* scriptTcpServer             = nullptr;

    QTimer* reciveTimer                     = nullptr;

    QAction* log_actionOne;
    QAction* log_actionTwo;
    QAction* log_actionThree;
    QAction* log_actionFour;

    QButtonGroup *group_test_case   = nullptr;
    QButtonGroup *group_all_id      = nullptr;

    QString m_cfg_file = {};
    int m_selected_test_case_number = 0;

    stTestResult_t g_stHighTestResult[8];

    thread_freq_accuracy* freq_accuracy = nullptr;

    thread_recive_maxscend_device   *threadParseReciveMxdChipData   = nullptr;

    TestModuleExceptionHandle       *exception_handle               = nullptr;


public:
    void radioButton_selection_init();

    void test_browser_show_log_text(QString text, enLogType logType);

    void showLogOnPlainText(QString text , enLogType logType);

    stTestInfo_t readTestInfo(int module_id);//读取测试信息配置入口

    QString acquire_data_save_path(); //获取数据保存路径
    bool high_temp_test_case(uint8_t u8TestID, enTestCaseCfg_t enTestCase, bool bCaseEnable);

    void dfu_write_configure_serial_data(QByteArray sendBuffer);
    uint8_t dfu_version_check(uint8_t u8DevNum);
    uint8_t dfu_upgrade_info_check(uint8_t u8DevNum);
    uint8_t dfu_send_shake_data(uint8_t u8DevNum);
    uint8_t dfu_upgrade_request_check(uint8_t u8DevNum);
    uint8_t dfu_send_firmware_data_check(uint8_t u8DevNum, uint32_t index, uint16_t size, uint32_t addr, uint8_t mode);
    uint8_t dfu_send_erase_flash_cmd(uint8_t u8DevNum, uint32_t addr, uint16_t length);
    uint8_t dfu_send_firmware_finish_check(uint8_t u8DevNum, uint32_t addr, uint32_t len, uint32_t crc_init);
    uint8_t dfu_send_restart_check(uint8_t u8DevNum);
    uint8_t dfu_state_machine(uint8_t u8DevNum);
    void chip_info_display(void);
    bool send_dfu_cmd_data(QByteArray byteArrayTemp, uint16_t timeout);
    bool serial_send_data_with_timeout(QByteArray sendBuffer, int time);

    EN_TIME_FLAG_T ackwait_time_s(int time_m);



public slots:
    void log_action_clear();

    void log_action_copy();

    void log_action_select_all();

    void log_action_save_file();

    void auto_test_recive_timeout_handler();

private slots:
    void on_test_config_triggered();

    void on_test_manager_triggered();

    void test_led_status_init();

    void test_led_group_init();

    void indicate_test_status_led(uint8_t testModuleID,uint8_t testResult);


    void read_configer_serial_data();

    void read_test_run_serial_data();

    void write_configer_serial_data(QByteArray sendBuffer);

    void write_test_run_serial_data(QByteArray sendBuffer);

    bool open_uart(uint8_t u8UartType);

    bool close_uart(uint8_t u8UartType);

    void on_runUarttoolButton_clicked();

    void on_configerUartToolButton_clicked();

    void read_freq_spec_tcp_data();

    void read_digtal_power_tcp_data();

    void read_digtal_voltage_tcp_data();

    void read_digtal_electricity_tcp_data();

    void slot_write_ins_freq_accuracy_client(QString sendBuffer);

    void write_digtal_power_tcp_data(QByteArray sendBuffer);

    void write_digtal_voltage_tcp_data(QByteArray sendBuffer);

    void write_digtal_electricity_tcp_data(QByteArray sendBuffer);

    bool open_client(uint8_t u8ClientType);

    bool close_client(uint8_t u8ClientType);

    void on_digtalPowerToolButton_clicked();

    void on_digtaElectricityToolButton_clicked();

    void on_digtaVoltageToolButton_clicked();


    void test_mode_ctrl_init();

    QString Get_the_current_value();

    void set_adc_voltage_value(float voltageValue);

    void on_autoTestRadioButton_clicked();

    void mxd_serial_recive_data_handle(stTestCtrlProcotolInfo_t testReturnInfo);

    bool send_auto_test_cmd_data(QByteArray byteArrayTemp, uint16_t timeout);

    void on_autoTestToolButton_clicked();

    void on_scripTestRadioButton_clicked();

    void read_tcp_socket_data();

    void write_tcp_socket_data(QByteArray send_buffer);

    void connect_script_server();

    void disconnect_script_server();

    void on_scriptToolButton_clicked();

    void on_ScriptSelectToolButton_clicked();

    void on_scriptTestToolButton_clicked();

/****************************************************************/

    void on_checkBox_AllID_clicked(bool checked);

    void slot_testCaseSelectionRecord(int TEST_CASE_TYPE, bool checked);

    void on_radioButton_AllTest_clicked(bool checked);

    void on_pushButton_TestInfoWrite_clicked();

    void on_pushButton_DataSavePathBrowse_clicked();

    void on_pushButton_SystemExcepWrite_clicked();

    void on_pushButton_SaveCfgFile_clicked();


    void on_actionHelp_Guid_triggered();

    void on_actionsoft_Version_triggered();

    void on_toolButton_Write_Addr_clicked();

    void on_FreqSpecButton_clicked();


    void on_FreqCalibrateButton_clicked();

    void on_dfu_setting_triggered();

    void on_firmwareLoad_clicked();

    void on_firmware_recognize_clicked();

    void on_chipInfo_recognize_clicked();

    void on_pushButton_startUpgrade_clicked();

    void on_pushButton_startUpgradeAll_clicked();

    void on_pushButton_stopUpgrade_clicked();

public slots:
    void slot_set_progressBar_freq_accuracy_value(int value);

    void slot_textEdit_Log_Warnning(QString display);

    void slot_textEdit_Log_setText(QString display);

    void slot_freq_accracy_stop_thread();

    void slot_send_freq_accracy_serial(uint8_t cmd, uint16_t value);


private:
    Ui::MainWindow *ui;

    stToolInfo m_toolInfo;

    void cfgfileGenerate();

signals:
    void sig_download_ack_timeout();

    void signal_system_exception_cfg(enSystemExceptionHandleCfg_t system_exception_cfg);

    void signal_system_reboot();
};


#endif // MAINWINDOW_H
