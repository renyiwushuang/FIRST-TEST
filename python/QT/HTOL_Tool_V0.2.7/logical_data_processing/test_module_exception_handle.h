#ifndef TEST_MODULE_EXCEPTION_HANDLE_H
#define TEST_MODULE_EXCEPTION_HANDLE_H

#include <QObject>
#include <QMessageBox>
#include <Windows.h>


typedef enum
{
    SEND_SYSTEM_ALARM_AND_RESTART_SYSTEM_WITH_TEST     = 0,
    RESTART_SYSTEM_WITH_TEST_AND_NO_SEND_SYSTEM_ALARM  = 1,
    SEND_SYSTEM_ALARM_AND_NO_RESTART_SYSTE             = 2,
}enSystemExceptionHandleCfg_t;

typedef enum
{
    GPIO_TEST         = 0,
    FLASH_TEST        = 1,
    TRX_CYC_TEST      = 2,
    I2C_TEST          = 3,
    SPI_TEST          = 4,
    CAN_TEST          = 5,
    RF_RX_TEST        = 6,
    RF_TX_TEST        = 7,
    ALL_TEST          = 8,
}enTestCaseCfg_t;


typedef struct
{
    enTestCaseCfg_t enTestCase;
    bool TestResult;
    uint8_t TestData[4];
}stTestResult_t;




typedef enum
{
    RESTART_CURRENT_CASE_TEST_AND_SEND_TEST_ALARM      = 0,
    START_NXET_CASE_TEST_AND_SEND_TEST_ALARM           = 1,
    RESTART_CURRENT_MODULE_TEST_AND_SEND_TEST_ALARM    = 2,
    START_NXET_MODULE_TEST_AND_SEND_TEST_ALARM         = 3,
}enTestExceptionHandleCfg_t;

typedef struct
{
    QString test_id;
    int test_case;
    enTestExceptionHandleCfg_t test_exception_handle;

}stTestInfoCfg_t;

typedef struct
{
    enSystemExceptionHandleCfg_t system_exception_handle;
    QString data_file_save_path;
    QString sendEmileName;
    QString sendEmilePassword;
    QString reciveEmileName;
    bool is_system_reboot;
}stSystemInfoCfg_t;

typedef struct
{
    int test_case;
    enTestExceptionHandleCfg_t test_exception_handle;
}stTestInfo_t;


class TestModuleExceptionHandle : public QWidget
{
    Q_OBJECT

public:
    explicit TestModuleExceptionHandle(QWidget *parent = nullptr);
    ~TestModuleExceptionHandle();

    void checkIsAutoReboot();
    bool sendAlarmBySound(int sound_time_s);
    bool sendAlarmByEmial(QString info);

private:

    QMessageBox *msgbTestException = nullptr;

    void initEmailCfg();
    void initSystemMessageBox();
    void initTestMessageBox();
    void showTestMessageBox(int time_s);

public slots:
    void slot_systemExceptionHandle(enSystemExceptionHandleCfg_t system_exception_cfg);//自定义槽

signals:
    void siganal_systemReboot();

};

extern long __stdcall   errCallback(_EXCEPTION_POINTERS*  pException);
void test();

#endif // TEST_MODULE_EXCEPTION_HANDLE_H
