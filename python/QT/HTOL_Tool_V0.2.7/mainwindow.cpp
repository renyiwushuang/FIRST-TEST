#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QMessageBox>
#include <QDebug>
#include <QFileDialog>
#include <QDateTime>
#include <QTimer>
#include <QFile>
#include <QFileDialog>
#include <QProcess>
#include "Intermediate_communication_protocol/communication_common.h"
#include "Intermediate_communication_protocol/communication_protcol.h"
#include "Intermediate_communication_protocol/test_ctlr_procotol.h"
#include "Intermediate_memory_management/common_data_conversion.h"
#include "Intermediate_memory_management/communication_memory_manager.h"
#include "logical_data_processing/test_module_exception_handle.h"
#include "device_processing/time_operate.h"
#include "logical_data_processing/bin_file_parse.h"



/***********************************************************************************************************************************
 * Location temp value define.
 **********************************************************************************************************************************/
//display ui index
#define TEST_MODULE_WIDGET                  (0)     //testModule    ui index
#define TEST_MANAGER_WIDGET                 (1)     //testManager   ui index
#define DFU_SETTING_WIDGET                  (2)     //dfu setting   ui index

#define TEST_START_INDEX    (enTestCaseCfg_t::FLASH_TEST)
static const uint8_t u8StartChipID  = 1;
static const uint8_t u8TotalChipNum = 11;//芯片总数

stTestCtrlProcotolInfo_t g_stTestReturnInfo;//芯片端回包数据


volatile uint8_t        testCaseResult = 0;
stTestInfo_t            g_stTestModuleInfo;
stTestCtrlProcotolPkg   g_stTestCtrlProcotolPkg;
QByteArray              g_sendTestCtrlProcotolPkg;
uint16_t                g_testCheckValue;
uint16_t                testCmdReciveTimeOut    = 10;
uint16_t                adcTestResultTemp       = 0;

uint16_t  allTestCaseTestResult      = 0;

bool g_reciveTestReturnDataFlage    = false;
bool g_reciveTimeoutFlage           = false;

bool testExternFlage                = false;
uint8_t testExternNumber            = 0x09;

uint8_t rfTestParaOpen  = 0x01;
uint8_t rfTestParaClose = 0x00;

uint32_t testNum = 0;  //for test

//#define HTOL_TEST_PRE  0;

QFile g_AllDataCsvFile; //汇总测试数据
QFile g_CuntDataCsvFile;//单次测试数据
QString testFileSavePachName;

enTestCaseReturnValue autoTestStatus = TEST_STATUS_NO_TEST;



#define CONFIGER_UART   1
#define TEST_RUN_UART   2

static bool  gConfigeUartOpenStatus = false;
static bool  gTestRunUartOpenStatus = false;
extern stRingBuff_t *g_uartTestProtocolReciveRingBuff;

static uint16_t  gConfigeUartClickNumber = 0;
static uint16_t  gTestRunUartClickNumber = 0;



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    /***********************************configer init*****************************************/
    test_led_status_init();
    test_led_group_init();
    test_mode_ctrl_init();

    /*********************************** device init *****************************************/
    configerSerialPort = new QSerialPort();
    testRunSerialPort  = new QSerialPort();

    connect(configerSerialPort  , SIGNAL(readyRead()), this, SLOT(read_configer_serial_data()));
    connect(testRunSerialPort   , SIGNAL(readyRead()), this, SLOT(read_test_run_serial_data()));

    digtalPowerTcpClient        = new QTcpSocket();
    digtalVoltageTcpClient      = new QTcpSocket();
    digtalElectricityTcpClient  = new QTcpSocket();
    freqSpecTcpClient           = new QTcpSocket();

    freqSpecTcpClient->abort();
    digtalPowerTcpClient->abort();
    digtalVoltageTcpClient->abort();
    digtalElectricityTcpClient->abort();

    connect(freqSpecTcpClient           , SIGNAL(readyRead()), this, SLOT(read_freq_spec_tcp_data()));
    connect(digtalPowerTcpClient        , SIGNAL(readyRead()), this, SLOT(read_digtal_power_tcp_data()));
    connect(digtalVoltageTcpClient      , SIGNAL(readyRead()), this, SLOT(read_digtal_voltage_tcp_data()));
    connect(digtalElectricityTcpClient  , SIGNAL(readyRead()), this, SLOT(read_digtal_electricity_tcp_data()));


    threadParseReciveMxdChipData = new thread_recive_maxscend_device();  //解析maxscend发送的数据
    connect(threadParseReciveMxdChipData, &thread_recive_maxscend_device::recive_maxscend_data_thread_signal,
            this,&MainWindow::mxd_serial_recive_data_handle);

    reciveTimer      = new QTimer();
    connect(reciveTimer, SIGNAL(timeout()),this,SLOT(auto_test_recive_timeout_handler()));

    /********************************* exception_handle ***************************************/
    this->exception_handle = new TestModuleExceptionHandle(this);

    connect(this, &MainWindow::signal_system_exception_cfg,
            exception_handle, &TestModuleExceptionHandle::slot_systemExceptionHandle);
    //如果系统自动重启后处理,自动测试开始
    connect(exception_handle, &TestModuleExceptionHandle::siganal_systemReboot,
            this, &MainWindow::MainWindow::on_autoTestToolButton_clicked);

    /******************************* test_configer_handle ************************************/
    radioButton_selection_init();
    void (QButtonGroup::*signal_case_selection)(int,bool) = &QButtonGroup::buttonToggled;
    connect(group_test_case, signal_case_selection, this, &MainWindow::slot_testCaseSelectionRecord);


    QRegExp rx("^[1-7]?[1-9]|[1-8][0]|All$"); //hash select astrict input value 1-64/All
    QRegExpValidator *pReg = new QRegExpValidator(rx, this);
    ui->lineEdit_TestID->setValidator(pReg);

    /****************************** Right click operation ************************************/
    ui->testLogTextBrowser->setContextMenuPolicy(Qt::ActionsContextMenu);
    log_actionOne   = new QAction(this);
    log_actionTwo   = new QAction(this);
    log_actionThree = new QAction(this);
    log_actionFour  = new QAction(this);

    log_actionOne->setText("Clear");
    log_actionTwo->setText("Copy");
    log_actionThree->setText("Select_All");
    log_actionFour->setText("Save_File");

    ui->testLogTextBrowser->addAction(log_actionOne);
    ui->testLogTextBrowser->addAction(log_actionTwo);
    ui->testLogTextBrowser->addAction(log_actionThree);
    ui->testLogTextBrowser->addAction(log_actionFour);

    connect(log_actionOne,      SIGNAL(triggered()), this, SLOT(log_action_clear()));
    connect(log_actionTwo,      SIGNAL(triggered()), this, SLOT(log_action_copy()));
    connect(log_actionThree,    SIGNAL(triggered()), this, SLOT(log_action_select_all()));
    connect(log_actionFour,     SIGNAL(triggered()), this, SLOT(log_action_save_file()));

    this->m_cfg_file = QCoreApplication::applicationDirPath()+ "\\cfg.ini";

    //this->exception_handle->checkIsAutoReboot(); //是否检查异常重启
    //生成软件配置信息
    cfgfileGenerate();

    on_radioButton_AllTest_clicked(true);

    slot_set_progressBar_freq_accuracy_value(0);

    freq_accuracy = new thread_freq_accuracy();
    connect(freq_accuracy, &thread_freq_accuracy::sigl_tcp_send_control_cmd, this, &MainWindow::slot_write_ins_freq_accuracy_client);
    connect(freq_accuracy, &thread_freq_accuracy::sigl_serial_send_cmd, this, &MainWindow::slot_send_freq_accracy_serial);
    connect(freq_accuracy, &thread_freq_accuracy::sigl_stop_freq_thread, this, &MainWindow::slot_freq_accracy_stop_thread);
    connect(freq_accuracy, &thread_freq_accuracy::sigl_display_freq_accuracy_log, this, &MainWindow::slot_textEdit_Log_setText);
    connect(freq_accuracy, &thread_freq_accuracy::sigl_set_process_value, this, &MainWindow::slot_set_progressBar_freq_accuracy_value);
    connect(freq_accuracy, &thread_freq_accuracy::sigl_display_warnning, this, &MainWindow::slot_textEdit_Log_Warnning);

    on_checkBox_AllID_clicked(true);
}

MainWindow::~MainWindow()
{
    delete ui;
    delete exception_handle;
}

//生成软件配置信息
void MainWindow::cfgfileGenerate()
{
    QDateTime curDateTime = QDateTime::currentDateTime();

    m_toolInfo.toolName = "Htol_Test_Tool";
    m_toolInfo.toolDomian = VToolInfoEnum::enToolDomain::UWB;
    m_toolInfo.toolType = VToolInfoEnum::enToolType::PC;
    m_toolInfo.toolForChipType = 1 << VToolInfoEnum::enToolForChipType::MXD271X;
    m_toolInfo.toolForApplicationType = 1 << VToolInfoEnum::enToolForApplicationType::TEST_APPLICATION;
    m_toolInfo.toolBrief = "This software is only used to finish High Temperature Operating Life (HTOL) test of maxscend soc chips.";
    m_toolInfo.toolVersion = "V0.2.7";
    m_toolInfo.toolUpdataData = curDateTime.toString("yyyy-MM-dd");

    setWindowTitle(m_toolInfo.toolName+ "_" + m_toolInfo.toolVersion);

    QString current_path = QCoreApplication::applicationDirPath() + "/" + m_toolInfo.toolName + ".ini";
    bool IsNeedRegeneration = false;

    if(QFile::exists(current_path))
    {
        //QFile::remove(current_path); //删除文件
        QSettings *settings = new QSettings(current_path, QSettings::IniFormat);
        settings->beginGroup(CFG_GROUP);
        if(settings->value(CFG_KEY_TOOL_VERSION).toString() == m_toolInfo.toolVersion)
        {
            qDebug() << "cfg is exist and not updata!" << endl;
            IsNeedRegeneration = false;
        }else{
            IsNeedRegeneration = true;
            QFile::remove(current_path); //删除文件
            qDebug() << "cfg is exist and updata!" << endl;
        }
    } else {IsNeedRegeneration = true;}

    if(IsNeedRegeneration){
        //重新生成配置文件;
        QSettings *settings = new QSettings(current_path, QSettings::IniFormat);
        settings->beginGroup(CFG_GROUP);
        settings->setValue(CFG_KEY_TOOL_NAME,m_toolInfo.toolName);
        settings->setValue(CFG_KEY_TOOL_DOMAIN,m_toolInfo.toolDomian);
        settings->setValue(CFG_KEY_TOOL_TYPE,m_toolInfo.toolType);
        settings->setValue(CFG_KEY_TOOL_FOR_CHIP_TYPE, m_toolInfo.toolForChipType);
        settings->setValue(CFG_KEY_TOOL_FOR_APPLICATION_TYPE, m_toolInfo.toolForApplicationType);
        settings->setValue(CFG_KEY_TOOL_BRIEF, m_toolInfo.toolBrief);
        settings->setValue(CFG_KEY_TOOL_VERSION, m_toolInfo.toolVersion);
        settings->setValue(CFG_KEY_UPTATA_DATA, m_toolInfo.toolUpdataData);
        settings->endGroup();
    }
}


/***********************************************************************************************************************************
 * notic: munubar and tool sorts.
 **********************************************************************************************************************************/
void MainWindow::on_test_config_triggered()
{
    qDebug("TRIGGER TEST CONFIG");
    ui->stackedWidget->setCurrentIndex(TEST_MODULE_WIDGET);
}

void MainWindow::on_test_manager_triggered()
{
    qDebug("TRIGGER TEST MANAGER");
    ui->stackedWidget->setCurrentIndex(TEST_MANAGER_WIDGET);
}

/************************************************************************************
 * notic: test status init.
 ************************************************************************************/
void MainWindow::test_led_status_init()
{
    set_led(ui->label_15, 0, 16);
    set_led(ui->label_16, 0, 16);
    set_led(ui->label_17, 0, 16);
    set_led(ui->label_18, 0, 16);
    set_led(ui->label_19, 0, 16);
    set_led(ui->label_20, 0, 16);
    set_led(ui->label_21, 0, 16);
    set_led(ui->label_22, 0, 16);
    set_led(ui->label_23, 0, 16);
    set_led(ui->label_24, 0, 16);
    set_led(ui->label_25, 0, 16);
    set_led(ui->label_26, 0, 16);
    set_led(ui->label_27, 0, 16);
    set_led(ui->label_28, 0, 16);
    set_led(ui->label_29, 0, 16);
    set_led(ui->label_30, 0, 16);
    set_led(ui->label_31, 0, 16);
    set_led(ui->label_32, 0, 16);
    set_led(ui->label_33, 0, 16);
    set_led(ui->label_34, 0, 16);
    set_led(ui->label_35, 0, 16);
    set_led(ui->label_36, 0, 16);
    set_led(ui->label_37, 0, 16);
    set_led(ui->label_38, 0, 16);
    set_led(ui->label_39, 0, 16);
    set_led(ui->label_40, 0, 16);
    set_led(ui->label_41, 0, 16);
    set_led(ui->label_42, 0, 16);
    set_led(ui->label_43, 0, 16);
    set_led(ui->label_44, 0, 16);
    set_led(ui->label_45, 0, 16);
    set_led(ui->label_46, 0, 16);
    set_led(ui->label_47, 0, 16);
    set_led(ui->label_48, 0, 16);
    set_led(ui->label_49, 0, 16);
    set_led(ui->label_50, 0, 16);
    set_led(ui->label_51, 0, 16);
    set_led(ui->label_52, 0, 16);
    set_led(ui->label_53, 0, 16);
    set_led(ui->label_54, 0, 16);
    set_led(ui->label_55, 0, 16);
    set_led(ui->label_56, 0, 16);
    set_led(ui->label_57, 0, 16);
    set_led(ui->label_58, 0, 16);
    set_led(ui->label_59, 0, 16);
    set_led(ui->label_60, 0, 16);
    set_led(ui->label_61, 0, 16);
    set_led(ui->label_62, 0, 16);
    set_led(ui->label_63, 0, 16);
    set_led(ui->label_64, 0, 16);
    set_led(ui->label_65, 0, 16);
    set_led(ui->label_66, 0, 16);
    set_led(ui->label_67, 0, 16);
    set_led(ui->label_68, 0, 16);
    set_led(ui->label_69, 0, 16);
    set_led(ui->label_70, 0, 16);
    set_led(ui->label_71, 0, 16);
    set_led(ui->label_72, 0, 16);
    set_led(ui->label_73, 0, 16);
    set_led(ui->label_74, 0, 16);
    set_led(ui->label_75, 0, 16);
    set_led(ui->label_76, 0, 16);
    set_led(ui->label_77, 0, 16);
    set_led(ui->label_78, 0, 16);
    set_led(ui->label_79, 0, 16);
    set_led(ui->label_80, 0, 16);
    set_led(ui->label_81, 0, 16);
    set_led(ui->label_82, 0, 16);
    set_led(ui->label_83, 0, 16);
    set_led(ui->label_84, 0, 16);
    set_led(ui->label_85, 0, 16);
    set_led(ui->label_86, 0, 16);
    set_led(ui->label_87, 0, 16);
    set_led(ui->label_88, 0, 16);
    set_led(ui->label_89, 0, 16);
    set_led(ui->label_90, 0, 16);
    set_led(ui->label_91, 0, 16);
    set_led(ui->label_92, 0, 16);
    set_led(ui->label_93, 0, 16);
    set_led(ui->label_94, 0, 16);
}

QMap<int,QLabel*>  lablelMap;

void MainWindow:: test_led_group_init()
{
    lablelMap.insert(1,ui->label_15);
    lablelMap.insert(2,ui->label_16);
    lablelMap.insert(3,ui->label_17);
    lablelMap.insert(4,ui->label_18);
    lablelMap.insert(5,ui->label_19);
    lablelMap.insert(6,ui->label_20);
    lablelMap.insert(7,ui->label_21);
    lablelMap.insert(8,ui->label_22);
    lablelMap.insert(9,ui->label_23);
    lablelMap.insert(10,ui->label_24);
    lablelMap.insert(11,ui->label_25);
    lablelMap.insert(12,ui->label_26);
    lablelMap.insert(13,ui->label_27);
    lablelMap.insert(14,ui->label_28);
    lablelMap.insert(15,ui->label_29);
    lablelMap.insert(16,ui->label_30);
    lablelMap.insert(17,ui->label_31);
    lablelMap.insert(18,ui->label_32);
    lablelMap.insert(19,ui->label_33);
    lablelMap.insert(20,ui->label_34);
    lablelMap.insert(21,ui->label_35);
    lablelMap.insert(22,ui->label_36);
    lablelMap.insert(23,ui->label_37);
    lablelMap.insert(24,ui->label_38);
    lablelMap.insert(25,ui->label_39);
    lablelMap.insert(26,ui->label_40);
    lablelMap.insert(27,ui->label_41);
    lablelMap.insert(28,ui->label_42);
    lablelMap.insert(29,ui->label_43);
    lablelMap.insert(30,ui->label_44);
    lablelMap.insert(31,ui->label_45);
    lablelMap.insert(32,ui->label_46);
    lablelMap.insert(33,ui->label_47);
    lablelMap.insert(34,ui->label_48);
    lablelMap.insert(35,ui->label_49);
    lablelMap.insert(36,ui->label_50);
    lablelMap.insert(37,ui->label_51);
    lablelMap.insert(38,ui->label_52);
    lablelMap.insert(39,ui->label_53);
    lablelMap.insert(40,ui->label_54);
    lablelMap.insert(41,ui->label_55);
    lablelMap.insert(42,ui->label_56);
    lablelMap.insert(43,ui->label_57);
    lablelMap.insert(44,ui->label_58);
    lablelMap.insert(45,ui->label_59);
    lablelMap.insert(46,ui->label_60);
    lablelMap.insert(47,ui->label_61);
    lablelMap.insert(48,ui->label_62);
    lablelMap.insert(49,ui->label_63);
    lablelMap.insert(50,ui->label_64);
    lablelMap.insert(51,ui->label_65);
    lablelMap.insert(52,ui->label_66);
    lablelMap.insert(53,ui->label_67);
    lablelMap.insert(54,ui->label_68);
    lablelMap.insert(55,ui->label_69);
    lablelMap.insert(56,ui->label_70);
    lablelMap.insert(57,ui->label_71);
    lablelMap.insert(58,ui->label_72);
    lablelMap.insert(59,ui->label_73);
    lablelMap.insert(60,ui->label_74);
    lablelMap.insert(61,ui->label_75);
    lablelMap.insert(62,ui->label_76);
    lablelMap.insert(63,ui->label_77);
    lablelMap.insert(64,ui->label_78);
    lablelMap.insert(65,ui->label_79);
    lablelMap.insert(66,ui->label_80);
    lablelMap.insert(67,ui->label_81);
    lablelMap.insert(68,ui->label_82);
    lablelMap.insert(69,ui->label_83);
    lablelMap.insert(70,ui->label_84);
    lablelMap.insert(71,ui->label_85);
    lablelMap.insert(72,ui->label_86);
    lablelMap.insert(73,ui->label_87);
    lablelMap.insert(74,ui->label_88);
    lablelMap.insert(75,ui->label_89);
    lablelMap.insert(76,ui->label_90);
    lablelMap.insert(77,ui->label_91);
    lablelMap.insert(78,ui->label_92);
    lablelMap.insert(79,ui->label_93);
    lablelMap.insert(80,ui->label_94);
}

void MainWindow:: indicate_test_status_led(uint8_t testModuleID,uint8_t testResult)
{
    set_led(lablelMap[testModuleID], testResult,16);
}

void MainWindow:: radioButton_selection_init()
{
    group_test_case = new QButtonGroup(this);
    group_all_id = new QButtonGroup(this);
    this->group_test_case->addButton(ui->radioButtonGpioTest,   enTestCaseCfg_t::GPIO_TEST);
    this->group_test_case->addButton(ui->radioButtonFlashTest,  enTestCaseCfg_t::FLASH_TEST);
    this->group_test_case->addButton(ui->radioButtonTrxTest,    enTestCaseCfg_t::TRX_CYC_TEST);
    this->group_test_case->addButton(ui->radioButtonI2cTest,   enTestCaseCfg_t::I2C_TEST);
    this->group_test_case->addButton(ui->radioButtonSpiTest,    enTestCaseCfg_t::SPI_TEST);
    this->group_test_case->addButton(ui->radioButtonCanTest,   enTestCaseCfg_t::CAN_TEST);
    this->group_test_case->addButton(ui->radioButtonRfRxTest,   enTestCaseCfg_t::RF_RX_TEST);
    this->group_test_case->addButton(ui->radioButtonRfTxTest,   enTestCaseCfg_t::RF_TX_TEST);
    this->group_test_case->addButton(ui->radioButton_AllTest,   enTestCaseCfg_t::ALL_TEST);
    this->group_test_case->setExclusive(false);

    this->group_all_id->addButton(ui->checkBox_AllID,0);
    this->group_all_id->setExclusive(false);
    this->m_selected_test_case_number =0;
}

/***********************************************************************************************************************************
 * notic: test configer handler.
 **********************************************************************************************************************************/

/************************************************************************************
 * 1、logType : 0:configer  1:send data  2:recive data.
 ************************************************************************************/
void MainWindow::showLogOnPlainText(QString text , enLogType logType)
{
    QTime current_time = QTime::currentTime();
    QString current_time_string = current_time.toString("hh:mm:ss.zzz");
    ui->testLogTextBrowser->insertPlainText("[");
    ui->testLogTextBrowser->insertPlainText(current_time_string);
    switch (logType) {
    case CONFIGER_TYPE:
        ui->testLogTextBrowser->insertPlainText("]:C<-->");
        break;
    case SEND_DATA_TYPE:
        ui->testLogTextBrowser->insertPlainText("]:S->");
        break;
    case RECIVE_DATA_TYPE:
        ui->testLogTextBrowser->insertPlainText("]:R<-");
        break;
    default:
        break;
    }
    ui->testLogTextBrowser->insertPlainText(text);
    ui->testLogTextBrowser->insertPlainText("\r\n");
}

/************************************************************************************
 * 1、test configer click operation.
 ************************************************************************************/
void MainWindow::on_checkBox_AllID_clicked(bool checked)
{
    if(checked){
        ui->lineEdit_TestID->setText("All");
    } else {
        ui->lineEdit_TestID->clear();
    }
}

void MainWindow::slot_testCaseSelectionRecord(int TEST_CASE_TYPE, bool checked)
{
    qDebug() << "更改前测试number" << this->m_selected_test_case_number << "\r\n";
    qDebug() << "选定case id：" << TEST_CASE_TYPE << "\r\n";

    if(checked){
        this->m_selected_test_case_number |= 1 << TEST_CASE_TYPE;
        qDebug() << "点击后测试number：" << this->m_selected_test_case_number;
    } else {
        this->m_selected_test_case_number &= ~(1 << TEST_CASE_TYPE);
        qDebug() << "取消后测试number：" << this->m_selected_test_case_number;
    }
}

void MainWindow::on_radioButton_AllTest_clicked(bool checked)
{
    qDebug() << "更改前测试number" << this->m_selected_test_case_number << "\r\n";
    qDebug() << "选定case id：all" << "\r\n";

    if(checked){
        this->m_selected_test_case_number |= 0xFF;
        for (int i = 0; i < enTestCaseCfg_t::ALL_TEST; i++)
        {
            this->group_test_case->button(i)->setChecked(true);
        }
        qDebug() << "点击后测试number：" << this->m_selected_test_case_number;
    } else {
        this->m_selected_test_case_number &= ~0xFF;

        for (int i = 0; i < enTestCaseCfg_t::ALL_TEST; i++)
        {
            this->group_test_case->button(i)->setChecked(false);
        }
        qDebug() << "取消后测试number：" << this->m_selected_test_case_number;
    }
}

void MainWindow::on_pushButton_TestInfoWrite_clicked()
{
    if(ui->lineEdit_TestID->text().isEmpty() || m_selected_test_case_number == 0 ){
        QMessageBox::warning(this, u8"提示", u8"请核查测试信息是否完整：测试模块ID，测试项", u8"确定");
    }else{

        stTestInfoCfg_t stTestInfoCfg;

        stTestInfoCfg.test_id = ui->lineEdit_TestID->text();
        stTestInfoCfg.test_case = this->m_selected_test_case_number;
        stTestInfoCfg.test_exception_handle = (enTestExceptionHandleCfg_t)ui->comboBox_TestExceptionHandle->currentIndex();

        qDebug() << "保存系统默认路径";

        //保存配置文件到默认程序运行路径
        QString current_path = QCoreApplication::applicationDirPath();
        current_path = current_path + "\\cfg.ini";
        QSettings *system_settings = new QSettings(current_path, QSettings::IniFormat);

        if(stTestInfoCfg.test_id == "All"){
            for(int i = 1; i < 81;  i++)
            {
                system_settings->beginGroup(QString("%1").arg(i));
                system_settings->setValue(QString("TEST_CASE_TYPE"), QVariant(stTestInfoCfg.test_case));
                system_settings->setValue(QString("TEST_EXCEPTION_HANDLE"), QVariant(stTestInfoCfg.test_exception_handle));
                system_settings->endGroup();
                system_settings->sync();
            }
        } else {
               system_settings->beginGroup(QString(stTestInfoCfg.test_id));
               system_settings->setValue(QString("TEST_CASE_TYPE"), QVariant(stTestInfoCfg.test_case));
               system_settings->setValue(QString("TEST_EXCEPTION_HANDLE"), QVariant(stTestInfoCfg.test_exception_handle));
               system_settings->endGroup();
               system_settings->sync();
        }

        this->showLogOnPlainText("测试信息写入成功！",CONFIGER_TYPE);
    }
}

void MainWindow::on_pushButton_SystemExcepWrite_clicked()
{
    enSystemExceptionHandleCfg_t current_system_exception_handle = (enSystemExceptionHandleCfg_t)ui->
                comboBox_SystemExceptionHandle->currentIndex();
    //写入系统默认路径配置文件
    QString current_path = QCoreApplication::applicationDirPath();
    current_path = current_path + "\\cfg.ini";
    QSettings *system_settings = new QSettings(current_path, QSettings::IniFormat);
    system_settings->beginGroup(QString("SYS_CFG"));
    system_settings->setValue(QString("SYSTEM_EXCEPTION_HANDLE"), QVariant(current_system_exception_handle));
    system_settings->endGroup();
    system_settings->sync();

    this->showLogOnPlainText("系统异常处理写入成功！",CONFIGER_TYPE);
    emit signal_system_exception_cfg(current_system_exception_handle);
}

void MainWindow::on_pushButton_SaveCfgFile_clicked()
{
    if(ui->lineEdit_DataSavePath->text().isEmpty()|| ui->lineEdit_TestID->text().isEmpty() || m_selected_test_case_number == 0 ){
           QMessageBox::warning(this, u8"提示", u8"请核查配置信息是否完整：数据保存路径，测试模块ID, 测试项", u8"确定");
    }else {

        stTestInfoCfg_t stTestInfoCfg;
        stSystemInfoCfg_t stSystemInfoCfg;

        stTestInfoCfg.test_id = ui->lineEdit_TestID->text();
        stTestInfoCfg.test_case = this->m_selected_test_case_number;
        stTestInfoCfg.test_exception_handle = (enTestExceptionHandleCfg_t)ui->comboBox_TestExceptionHandle->currentIndex();

        stSystemInfoCfg.system_exception_handle = (enSystemExceptionHandleCfg_t)ui->comboBox_SystemExceptionHandle->currentIndex();
        stSystemInfoCfg.sendEmileName           = ui->lineEdit_sendEmilName->text();
        stSystemInfoCfg.sendEmilePassword       = ui->lineEdit_sendEmilPassword->text();
        stSystemInfoCfg.reciveEmileName         = ui->lineEdit_ReciveEmilName->text();
        stSystemInfoCfg.data_file_save_path     = ui->lineEdit_DataSavePath->text();
        stSystemInfoCfg.is_system_reboot        = false;

        //保存配置文件到默认程序运行路径
        QString current_path = QCoreApplication::applicationDirPath();
        current_path = current_path + "\\cfg.ini";
        if(!QFile::exists(current_path)){
            QSettings *settings = new QSettings(current_path, QSettings::IniFormat);
            settings->beginGroup(QString("EMAIL_CFG"));
            settings->setValue(QString("SENDER_EMAIL_USER_NAME"), QVariant(stSystemInfoCfg.sendEmileName));
            settings->setValue(QString("SENDER_EMAIL_PASSWORD"), QVariant(stSystemInfoCfg.sendEmilePassword ));
            settings->setValue(QString("RECEIVER_EMAIL_USER_NAME"), QVariant(stSystemInfoCfg.reciveEmileName ));
            settings->endGroup();
            settings->sync();
        }

        QSettings *system_settings = new QSettings(current_path, QSettings::IniFormat);
        system_settings->beginGroup(QString("SYS_CFG"));
        system_settings->setValue(QString("SYSTEM_EXCEPTION_HANDLE"), QVariant(stSystemInfoCfg.system_exception_handle));
        system_settings->setValue(QString("DATA_FILE_SAVE_PATH"), QVariant(stSystemInfoCfg.data_file_save_path));
        system_settings->setValue(QString("IS_SYSTEM_RESTART"), QVariant(stSystemInfoCfg.is_system_reboot));
        system_settings->endGroup();
        system_settings->sync();

        if(stTestInfoCfg.test_id == "All"){
            for(int i = 1; i < 81;  i++)
            {
                system_settings->beginGroup(QString("%1").arg(i));
                system_settings->setValue(QString("TEST_CASE_TYPE"), QVariant(stTestInfoCfg.test_case));
                system_settings->setValue(QString("TEST_EXCEPTION_HANDLE"), QVariant(stTestInfoCfg.test_exception_handle));
                system_settings->endGroup();
            }
            system_settings->sync();
        } else {
            system_settings->beginGroup(QString(stTestInfoCfg.test_id));
            system_settings->setValue(QString("TEST_CASE_TYPE"), QVariant(stTestInfoCfg.test_case));
            system_settings->setValue(QString("TEST_EXCEPTION_HANDLE"), QVariant(stTestInfoCfg.test_exception_handle));
            system_settings->endGroup();
            system_settings->sync();
        }

        QMessageBox::warning(this, u8"提示", u8"配置文件保存成功！", u8"确定");

        this->showLogOnPlainText("配置文件保存成功！",CONFIGER_TYPE);
        current_path.replace("/","\\");
        ui->lineEdit_CfgFilePath->setText(current_path);
        this->m_cfg_file = current_path;
        emit signal_system_exception_cfg(stSystemInfoCfg.system_exception_handle);
    }
}

void MainWindow::on_pushButton_DataSavePathBrowse_clicked()
{
    QString data_save_path;

    data_save_path = QFileDialog::getExistingDirectory(this, u8"选择文件夹","../",
                                                       QFileDialog::ShowDirsOnly |QFileDialog::DontResolveSymlinks);

    data_save_path.replace("/","\\");

    ui->lineEdit_DataSavePath->setText(data_save_path);

}

stTestInfo_t MainWindow::readTestInfo(int module_id)
{
    stTestInfo_t stTestInfo = {};

    if(QFile::exists(this->m_cfg_file )){
//        qDebug() << "读取配置文件存在！" << "\r\n";
        QSettings *settings = new QSettings(this->m_cfg_file, QSettings::IniFormat);
        settings->beginGroup(QString("%1").arg(module_id));
        stTestInfo.test_case = (enTestCaseCfg_t)settings->value("TEST_CASE_TYPE").toInt();
        stTestInfo.test_exception_handle = (enTestExceptionHandleCfg_t)settings->value("TEST_EXCEPTION_HANDLE").toInt();
        settings->endGroup();
//        qDebug() << "测试配置信息：test_id, test_case, test_exception_handle, " << module_id
//                 << stTestInfo.test_case << stTestInfo.test_exception_handle<< "\r\n";
    } else {
        qDebug() << "读取配置文件不存在！";
    }
    return stTestInfo;
}

QString MainWindow::acquire_data_save_path()
{
    QString data_save_path = {};

    if(QFile::exists(this->m_cfg_file)) {
        //qDebug() << "读取配置文件存在！";
        QSettings *settings = new QSettings(this->m_cfg_file, QSettings::IniFormat);
        settings->beginGroup(QString("SYS_CFG"));
        data_save_path = settings->value("DATA_FILE_SAVE_PATH").toString();
        settings->endGroup();
        //qDebug() << "数据保存路径："<< data_save_path;
    } else {
        qDebug() << "读取配置文件不存在";
    }
    return data_save_path;
}

/************************************************************************************
 * 2、Right click operation.
 ************************************************************************************/
void MainWindow::log_action_clear()
{
    qDebug("dlog_action_clear");
    ui->testLogTextBrowser->clear();
}

void MainWindow::log_action_copy()
{
    qDebug("dut_log_action_copy");
    ui->testLogTextBrowser->copy();
}

void MainWindow::log_action_select_all()
{
    qDebug("dut_log_action_select_all");
    ui->testLogTextBrowser->selectAll();
}

void MainWindow::log_action_save_file()
{
    QString text;
    QByteArray text_temp;

    text = ui->testLogTextBrowser->toPlainText();
    text_temp = text.toUtf8();

    QString current_path = QFileDialog::getExistingDirectory(this, u8"选择文件夹","../",
                                                             QFileDialog::ShowDirsOnly |QFileDialog::DontResolveSymlinks);
    ui->testLogTextBrowser->insertPlainText(current_path + "\r\n");
    current_path.replace("/","\\");
    ui->testLogTextBrowser->insertPlainText(current_path + "\r\n");

    QString file_name = current_path + "/[";
    QDateTime data_time = QDateTime::currentDateTime();
    QString data_time_string = data_time.toString("yyyy_MM_dd_hh_mm");
    file_name += data_time_string;
    file_name += "]_log.txt";

    QFile file(file_name);

    if (!file.open(QFile::WriteOnly | QFile::Text))
    {
        QMessageBox::information(this, "Error Message", "Please Select a Text File!");
        return;
    }
    file.write(text_temp);
    file.close();
}

/***********************************************************************************************************************************
 * notic: test manager handler.
 **********************************************************************************************************************************/

/************************************************************************************
 * 1、 test device uart handler.
 ************************************************************************************/

bool MainWindow:: open_uart(uint8_t u8UartType)
{
    QString selectBaudRate;
    bool uartOpenStatue = 0;

    switch(u8UartType)
    {
        case CONFIGER_UART:
        {
            if(ui->UartComboBox->currentText().isEmpty()){
                QMessageBox::warning(this, u8"提示", u8"CONFIGER_UART未选中任何可用串口", u8"确定");
            }
            else{
                selectBaudRate = ui->UartBoartComboBox->currentText();
                configerSerialPort->setBaudRate(selectBaudRate.toInt());
                configerSerialPort->setDataBits(QSerialPort::Data8);
                configerSerialPort->setParity(QSerialPort::NoParity);
                configerSerialPort->setStopBits(QSerialPort::OneStop);
                configerSerialPort->setFlowControl(QSerialPort::NoFlowControl);

                configerSerialPort->setPortName(ui->UartComboBox->currentText());
                uartOpenStatue = configerSerialPort->open(QIODevice::ReadWrite);
                if(uartOpenStatue)
                {
                    configerSerialPort->setDataTerminalReady(true);
                }
                return uartOpenStatue;
            }
            return false; break;
        }
        case TEST_RUN_UART:
        {
            if(ui->runUartComboBox->currentText().isEmpty()){
                QMessageBox::warning(this, u8"提示", u8"TEST_RUN_UART未选中任何可用串口", u8"确定");
            }
            else{
                selectBaudRate = ui->runUartBaudRateComboBox->currentText();
                testRunSerialPort->setBaudRate(selectBaudRate.toInt());
                testRunSerialPort->setDataBits(QSerialPort::Data8);
                testRunSerialPort->setParity(QSerialPort::NoParity);
                testRunSerialPort->setStopBits(QSerialPort::OneStop);
                testRunSerialPort->setFlowControl(QSerialPort::NoFlowControl);

                testRunSerialPort->setPortName(ui->runUartComboBox->currentText());
                uartOpenStatue = testRunSerialPort->open(QIODevice::ReadWrite);
                if(uartOpenStatue)
                {
                    testRunSerialPort->setDataTerminalReady(true);
                }
                return uartOpenStatue;
            }
            return false; break;
        }
        default :
        {
            qDebug(u8"没有选择指定设备");
            return false; break;
        }
    }
    return true;
}

bool MainWindow:: close_uart(uint8_t u8UartType)
{
    switch(u8UartType)
    {
        case CONFIGER_UART:
        {
            configerSerialPort->close();
            return true;
        }
        case TEST_RUN_UART:
        {
            testRunSerialPort->close();
            return true;
        }
    }
    return true;
}

void MainWindow:: read_configer_serial_data()
{
    QByteArray  configerReadTemp;
    QString     reciveStringTemp;
    configerReadTemp = configerSerialPort->readAll();

    reciveStringTemp = ByteArrayToString(configerReadTemp);
    qDebug()<<"Recv1:"<<reciveStringTemp;
    qDebug()<<"DataLen = "<<configerReadTemp.size();

    for (int i = 0;i < configerReadTemp.size();i++)
    {
        push_ring_buf(g_uartTestProtocolReciveRingBuff, configerReadTemp.at(i));
    }

    showLogOnPlainText(reciveStringTemp, RECIVE_DATA_TYPE);
}

void MainWindow:: read_test_run_serial_data()
{
    QByteArray  testRunReadTemp;
    QString     reciveStringTemp;
    testRunReadTemp = testRunSerialPort->readAll();

    //qDebug("---------recive data ----------");
    reciveStringTemp = ByteArrayToString(testRunReadTemp);
    //showLogOnPlainText(reciveStringTemp, RECIVE_DATA_TYPE);

    for (int i = 0;i < testRunReadTemp.size();i++) {
        push_ring_buf(g_uartTestProtocolReciveRingBuff,testRunReadTemp.at(i));
    }
}


/*******************************************************************************
 * Set ackwait time.
 * signal ack with close timeout.
 *******************************************************************************/
EN_TIME_FLAG_T MainWindow::ackwait_time_s(int time_m)
{
    QEventLoop loop;
    QTimer timeout_t;
    timeout_t.setSingleShot(true);
    connect(&timeout_t,SIGNAL(timeout()),&loop,SLOT(quit()));
    connect(this,SIGNAL(sig_download_ack_timeout()),&loop,SLOT(quit()));
    timeout_t.start(time_m);
    loop.exec();

    if(timeout_t.isActive())
    {
        qDebug()<<"ack is ok!";
        return Right_reponse;
    }
    else
    {
        qDebug()<<"ack is Timeout!";
        return Timeout_flag;
    }
}

void MainWindow:: dfu_write_configure_serial_data(QByteArray sendBuffer)
{
    if (true == gConfigeUartOpenStatus)
    {
        configerSerialPort->write(sendBuffer);

        QString  sendStringTemp;
        sendStringTemp = ByteArrayToString(sendBuffer);
        test_browser_show_log_text(sendStringTemp, CONFIGER_TYPE);
    }
    else
    {
        test_browser_show_log_text(u8"配置串口没有打开", CONFIGER_TYPE);
    }
}


void MainWindow:: write_configer_serial_data(QByteArray sendBuffer)
{
    if(true == gConfigeUartOpenStatus) {
        configerSerialPort->write(sendBuffer);

        QString  sendStringTemp;
        sendStringTemp = ByteArrayToString(sendBuffer);
        showLogOnPlainText(sendStringTemp, CONFIGER_TYPE);
    }
    else{
       showLogOnPlainText(u8"配置串口没有打开", CONFIGER_TYPE);
    }
}

bool MainWindow::serial_send_data_with_timeout(QByteArray sendBuffer, int time)
{
    write_configer_serial_data(sendBuffer);
    //write_test_run_serial_data(sendBuffer);

    //2、start timer
    //qDebug("--------- 3/3/2 start timer -------------");
    reciveTimer->start(time* 500);

    //3、wait test return value
    //qDebug("--------- 3/3/3 wait return -------------");
    while(true){
        //g_reciveTestReturnDataFlage = true;
        if(g_reciveTimeoutFlage == false){
            if(g_reciveTestReturnDataFlage){
                reciveTimer->stop();
                g_reciveTestReturnDataFlage = false;
                return true;
            } else{
                delay_msec(10,1); //wait recive data.
            }
        } else{ //recive timeout
            return false;
        }
    }

    return false;
}


void MainWindow:: write_test_run_serial_data(QByteArray sendBuffer)
{
    if(true == gTestRunUartOpenStatus) {
        testRunSerialPort->write(sendBuffer);

        QString  sendStringTemp;
        sendStringTemp = ByteArrayToString(sendBuffer);
        showLogOnPlainText(sendStringTemp, SEND_DATA_TYPE);
    }
    else{
        showLogOnPlainText(u8"模块控制串口没有打开", CONFIGER_TYPE);
    }
}

void MainWindow:: on_runUarttoolButton_clicked()
{
    gTestRunUartClickNumber++;

    if(0 == (gTestRunUartClickNumber % 2)){
        ui->runUarttoolButton->setText(u8"连接");
        close_uart(TEST_RUN_UART);
        showLogOnPlainText("模块控制串口关闭成功", CONFIGER_TYPE);
        gTestRunUartOpenStatus = false;

        //recive thread handler
        communication_memory_ring_buff_deinit(MXD_RUN_UART);
        threadParseReciveMxdChipData->terminate();  //关闭解析线程

    }
    else{
        gTestRunUartOpenStatus = open_uart(TEST_RUN_UART);
        if(true == gTestRunUartOpenStatus ) {
            ui->runUarttoolButton->setText(u8"断连");
            showLogOnPlainText("模块控制串口打开成功", CONFIGER_TYPE);

            //thread handler
            communication_memory_ring_buff_init(MXD_RUN_UART);
            threadParseReciveMxdChipData->start();  //开启解析线程
        }
        else{
            gTestRunUartClickNumber -= 1;
            QMessageBox::warning(this, u8"提示", u8"TEST_RUN_UART串口打开失败", u8"确定");
        }
    }
    if(65530 == gTestRunUartClickNumber){ gTestRunUartClickNumber = 0; }
}

void MainWindow:: on_configerUartToolButton_clicked()
{
    gConfigeUartClickNumber++;

    if(0 == (gConfigeUartClickNumber % 2)){
        ui->configerUartToolButton->setText(u8"连接");
        close_uart(CONFIGER_UART);
        showLogOnPlainText("配置串口关闭成功", CONFIGER_TYPE);

        //recive thread handler
        communication_memory_ring_buff_deinit(MXD_RUN_UART);
        threadParseReciveMxdChipData->terminate();  //关闭解析线程

        gConfigeUartOpenStatus = false;
    }
    else{
        gConfigeUartOpenStatus = open_uart(CONFIGER_UART);
        if(true == gConfigeUartOpenStatus ) {
            ui->configerUartToolButton->setText(u8"断连");
            showLogOnPlainText("配置串口打开成功", CONFIGER_TYPE);

            //recive thread handler
            communication_memory_ring_buff_init(MXD_RUN_UART);
            threadParseReciveMxdChipData->start();  //开启解析线程
        }
        else{
            gConfigeUartClickNumber -= 1;
            QMessageBox::warning(this, u8"提示", u8"TEST_RUN_UART串口打开失败", u8"确定");
        }
    }
    if(65530 == gConfigeUartClickNumber){ gConfigeUartClickNumber = 0; }
}

/************************************************************************************
 * 2、 test device client handler.
 ************************************************************************************/
#define POWER_CLIENT        1
#define VOLTAGE_CLIENT      2
#define ELECTRICITY_CLIENT  3
#define FREQ_SPEC_CLIENT    4

static bool  gDigtalPowerOpenStatus         = false;
static bool  gDigtalVoltageOpenStatus       = false;
static bool  gDigtalElectricityOpenStatus   = false;
static bool  gFreqSpecOpenStatus            = false;

static uint16_t  gDigtalPowerClickNumber        = 0;
static uint16_t  gDigtalVoltageClickNumber      = 0;
static uint16_t  gDigtalElectricityClickNumber  = 0;

QString gReadElectricityTemp= {};
extern QByteArray g_RecvDataFreqSpecTcp;     //TCP接收数据缓存区

bool MainWindow:: open_client(uint8_t u8ClientType)
{
    //QString Net_info;
    QString IP_Addr;
    QString Net_Port;

    switch (u8ClientType) {
        case POWER_CLIENT:
        {
            IP_Addr = ui->digtalPowerLineEdit->text();
            Net_Port = ui->digtalPowerPortlineEdit->text();
            digtalPowerTcpClient->connectToHost(IP_Addr,Net_Port.toInt());
            gDigtalPowerOpenStatus = digtalPowerTcpClient->waitForConnected(300);
            return gDigtalPowerOpenStatus;
        }
        case VOLTAGE_CLIENT:
        {
            IP_Addr = ui->digtaVoltagelineEdit->text();
            Net_Port = ui->digtaVoltagePortlineEdit->text();
            digtalVoltageTcpClient->connectToHost(IP_Addr,Net_Port.toInt());
            gDigtalVoltageOpenStatus = digtalVoltageTcpClient->waitForConnected(300);
            return gDigtalVoltageOpenStatus;
        }
        case ELECTRICITY_CLIENT:
        {
            IP_Addr = ui->digtaElectricityllineEdit->text();
            Net_Port = ui->digtaElectricityPortlineEdit->text();
            digtalElectricityTcpClient->connectToHost(IP_Addr,Net_Port.toInt());
            gDigtalElectricityOpenStatus = digtalElectricityTcpClient->waitForConnected(300);
            return gDigtalElectricityOpenStatus;
        }
        case FREQ_SPEC_CLIENT:
        {
            IP_Addr = ui->FreqSpecAddrLineEdit->text();
            Net_Port = ui->FreqSpecPortlineEdit->text();
            freqSpecTcpClient->connectToHost(IP_Addr,Net_Port.toInt());
            gFreqSpecOpenStatus = freqSpecTcpClient->waitForConnected(300);
            return gFreqSpecOpenStatus;
        }
        default:
            break;
        }
        return true;
}

bool MainWindow:: close_client(uint8_t u8ClientType)
{
    switch (u8ClientType) {
    case POWER_CLIENT:
    {
        digtalPowerTcpClient->disconnectFromHost();
        gDigtalPowerOpenStatus = false;
        break;
    }
    case VOLTAGE_CLIENT:
    {
        digtalVoltageTcpClient->disconnectFromHost();
        gDigtalVoltageOpenStatus = false;
        break;
    }
    case ELECTRICITY_CLIENT:
    {
        digtalElectricityTcpClient->disconnectFromHost();
        gDigtalElectricityOpenStatus = false;
        break;
    }
    case FREQ_SPEC_CLIENT:
    {
        freqSpecTcpClient->disconnectFromHost();
        gFreqSpecOpenStatus = false;
        break;
    }
    default:
        break;
    }
    return true;
}


void MainWindow:: read_freq_spec_tcp_data()
{
    g_RecvDataFreqSpecTcp = freqSpecTcpClient->readAll();
}

void MainWindow:: read_digtal_power_tcp_data()
{
    QByteArray  digtalPowerTcpReadTemp;
    digtalPowerTcpReadTemp = digtalPowerTcpClient->readAll();

}

void MainWindow:: read_digtal_voltage_tcp_data()
{
    QByteArray  digtalVoltageTcpReadTemp;
    digtalVoltageTcpReadTemp = digtalVoltageTcpClient->readAll();
}

void MainWindow:: read_digtal_electricity_tcp_data()
{
    gReadElectricityTemp = digtalElectricityTcpClient->readAll();
}

void MainWindow::slot_write_ins_freq_accuracy_client(QString sendBuffer)
{
    if(freqSpecTcpClient->isValid()){
        int send_status = freqSpecTcpClient->write((sendBuffer + "\r\n").toUtf8().data());
        if(-1 == send_status){
            qDebug(u8"freqSpecTcpClient 发送数据失败！\r\n");
        }
    }
    else{
       qDebug(u8"freqSpecTcpClient 套接字无效！\r\n");
    }
}

void MainWindow:: write_digtal_power_tcp_data(QByteArray sendBuffer)
{
    if(digtalPowerTcpClient->isValid()){
        int send_status = digtalPowerTcpClient->write(sendBuffer);
        if(-1 == send_status){
            qDebug(u8"digtalPowerTcpClient 发送数据失败！\r\n");
        }
    }
    else{
       qDebug(u8"digtalPowerTcpClient 套接字无效！\r\n");
    }
}

void MainWindow:: write_digtal_voltage_tcp_data(QByteArray sendBuffer)
{
    if(digtalVoltageTcpClient->isValid()){
        int send_status = digtalVoltageTcpClient->write(sendBuffer);
        if(-1 == send_status){
            qDebug(u8"digtalVoltageTcpClient 发送数据失败！\r\n");
        }
    }
    else{
       qDebug(u8"digtalVoltageTcpClient 套接字无效！\r\n");
    }
}

void MainWindow:: write_digtal_electricity_tcp_data(QByteArray sendBuffer)
{
    if(digtalElectricityTcpClient->isValid()){
        int send_status = digtalElectricityTcpClient->write(sendBuffer);
        if(-1 == send_status){
            qDebug(u8"digtalElectricityTcpClient 发送数据失败！\r\n");
        }
    }
    else{
       qDebug(u8"digtalElectricityTcpClient 套接字无效！\r\n");
    }
}

void MainWindow:: on_digtalPowerToolButton_clicked()
{
    gDigtalPowerClickNumber++;
    if(0 == (gDigtalPowerClickNumber % 2)){
        if(true == close_client(POWER_CLIENT)) {
            ui->digtalPowerToolButton->setText("连接");
        }
        else{
            gDigtalPowerClickNumber -= 1;
        }
    }
    else{
        if(true == open_client(POWER_CLIENT)) {
           ui->digtalPowerToolButton->setText("断链");
        }
        else{
           gDigtalPowerClickNumber -= 1;
        }
    }
    if(65530 == gDigtalPowerClickNumber){ gDigtalPowerClickNumber = 0;}
}

void MainWindow:: on_digtaVoltageToolButton_clicked()
{
    gDigtalVoltageClickNumber++;
    if(0 == (gDigtalVoltageClickNumber % 2)){
        if(true == close_client(VOLTAGE_CLIENT)) {
            ui->digtaVoltageToolButton->setText("连接");
        }
        else{
            gDigtalVoltageClickNumber -= 1;
        }
    }
    else{
        if(true == open_client(VOLTAGE_CLIENT)) {
           ui->digtaVoltageToolButton->setText("断链");
        }
        else{
           gDigtalVoltageClickNumber -= 1;
        }
    }
    if(65530 == gDigtalVoltageClickNumber){ gDigtalVoltageClickNumber = 0;}
}

void MainWindow:: on_digtaElectricityToolButton_clicked()
{
    gDigtalElectricityClickNumber++;
    if(0 == (gDigtalElectricityClickNumber % 2)){
        qDebug("close electricity device");
        if(true == close_client(ELECTRICITY_CLIENT)) {;
            ui->digtaElectricityToolButton->setText("连接");
        }
        else{
            gDigtalElectricityClickNumber -= 1;
        }
    }
    else{
        qDebug("open electricity device");
        if(true == open_client(ELECTRICITY_CLIENT)) {
           ui->digtaElectricityToolButton->setText("断链");
        }
        else{
           gDigtalElectricityClickNumber -= 1;
        }
    }
    if(65530 == gDigtalElectricityClickNumber){ gDigtalElectricityClickNumber = 0;}
}

/************************************************************************************
 * 3、 test mode ctrl handler.
 ************************************************************************************/
void MainWindow::test_mode_ctrl_init()
{
    //1、enable auto test
    ui->autoTestToolButton->setEnabled(true);

    //2、disable script test
    ui->scripTestRadioButton->setChecked(false);

    ui->scriptNetcomboBox->setDisabled(true);
    ui->scriptPortlineEdit->setDisabled(true);
    ui->scriptToolButton->setDisabled(true);

    ui->ScriptSelectToolButton->setDisabled(true);
    ui->scriptPatchlineEdit->setDisabled(true);
    ui->scriptTestToolButton->setDisabled(true);
}

/********* 1、auto test mode test handler ************/
/* 0:fail  1:pass
 * bit1 _test_result_gpio
 * bit2 _test_result_gpadc
 * bit3 _test_result_vbat_adc
 * bit4 _test_result_flash
 * bit5 _test_result_ipc
 * bit6 _test_result_rf_tx
 * bit7 _test_result_rf_rx
 * */


void MainWindow::on_autoTestRadioButton_clicked()
{
    //1、enable auto test
    ui->autoTestToolButton->setEnabled(true);

    //2、disable script test
    ui->scripTestRadioButton->setChecked(false);

    ui->scriptNetcomboBox->setDisabled(true);
    ui->scriptPortlineEdit->setDisabled(true);
    ui->scriptToolButton->setDisabled(true);

    ui->ScriptSelectToolButton->setDisabled(true);
    ui->scriptPatchlineEdit->setDisabled(true);
    ui->scriptTestToolButton->setDisabled(true);

}

QString MainWindow::Get_the_current_value()
{
    QString testCmd = "MEAS:CURR? CH1\r\n";

    if(digtalElectricityTcpClient->isValid()){
        digtalElectricityTcpClient->write(testCmd.toLatin1());
    } else{

        qDebug("NO Connect device");
    }

    // wait test return value
    delay_msec(400,1);

    return gReadElectricityTemp;

}

void MainWindow::set_adc_voltage_value(float voltageValue)
{
    QString voltagetemp = QString("%1").arg(voltageValue);

    QString testCmd = "APPL P6V,"+ voltagetemp +",0.2 \r\n";

    //qDebug()<< testCmd.toLatin1();

    if(digtalPowerTcpClient->isValid()){
        digtalPowerTcpClient->write(testCmd.toLatin1());
    } else{
        qDebug("NO Connect device");
    }

    QDateTime dateTime(QDateTime::currentDateTime());
    QString testTime = dateTime.toString("[yy-MM-dd]_[hh-mm-ss]_[zzz]");
    delay_msec(10,1); //电源稳定

    qDebug()<<testTime;

}

static QString test_case_type_cover(enTestCaseCfg_t testCaseType)
{
    QString testCmdTempString;

    switch(testCaseType){
        case enTestCaseCfg_t::GPIO_TEST:{
            testCmdTempString = "GPIO_INPUT_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::FLASH_TEST:{
            testCmdTempString = "FLASH_RW_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::TRX_CYC_TEST:{
            testCmdTempString = "TRX_CYC_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::I2C_TEST:{
            testCmdTempString = "I2C_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::SPI_TEST:{
            testCmdTempString = "SPI_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::CAN_TEST:{
            testCmdTempString = "CAN_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::RF_RX_TEST:{
            testCmdTempString = "RF_RX_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::RF_TX_TEST:{
            testCmdTempString = "RF_TX_TEST";
            return testCmdTempString;}
    case enTestCaseCfg_t::ALL_TEST:{
            testCmdTempString = "Total_Current_Test";
            return testCmdTempString;}
        default : break;
    }
    testCmdTempString =  "no mich test case";
    return testCmdTempString;
}

static QString test_result_cover(enTestCaseReturnValue testResultType)
{
    QString testResultTempString;

    switch(testResultType){
        case TEST_STATUS_PASS:{
            testResultTempString = "TEST_STATUS_PASS";
            return testResultTempString;}
        case TEST_STATUS_RECIVE_TIMEOUT:{
            testResultTempString = "TEST_STATUS_RECIVE_TIMEOUT";
            return testResultTempString;}
        case TEST_STATUS_FAIL:{
            testResultTempString = "TEST_STATUS_FAIL";
            return testResultTempString;}
        case TEST_STATUS_SECD_PASS:{
            testResultTempString = "TEST_STATUS_SECD_PASS";
            return testResultTempString;}
        case TEST_STATUS_SECD_FAIL:{
            testResultTempString = "TEST_STATUS_SECD_FAIL";
            return testResultTempString;}
        case TEST_STATUS_SECD_RECIVE_TIMEOUT:{
            testResultTempString = "TEST_STATUS_SECD_RECIVE_TIMEOUT";
            return testResultTempString;}
        case TEST_STATUS_FAIL_NEXT_CASE:{
            testResultTempString = "TEST_STATUS_FAIL_NEXT_CASE";
            return testResultTempString;}
        case TEST_STATUS_FAIL_RESET_TEST_MODULE:{
            testResultTempString = "TEST_STATUS_FAIL_RESET_TEST_MODULE";
            return testResultTempString;}
        case TEST_STATUS_FAIL_NEXT_TEST_MODULE:{
            testResultTempString = "TEST_STATUS_FAIL_NEXT_TEST_MODULE";
            return testResultTempString;}
        default : break;
    }
    testResultTempString =  "TEST_STATUS_NO_TEST";
    return testResultTempString;
}

//QFile adcTestCsvFile;

//static QString creat_cvs_adc_test_file(QString csvfile_path, uint32_t testNumber)
//{
//    QDateTime dateTime(QDateTime::currentDateTime());
//    QString testTime = dateTime.toString("[yy-MM-dd]_[hh-mm-ss]");

//    QString cvsFileName = csvfile_path.append("/");
//    cvsFileName.append(testTime);
//    cvsFileName.append("_[");
//    cvsFileName.append(QString::number(testNumber));
//    cvsFileName.append("]_");
//    cvsFileName.append("adc_test.csv");

//    QString csvFistLine = u8"test_time,test_module_ID, test_stand_volatage,get_ADC_value\n";

//    adcTestCsvFile.setFileName(cvsFileName);

//    if (adcTestCsvFile.open(QIODevice::WriteOnly | QFile::Truncate)) {
//        adcTestCsvFile.write(csvFistLine.toStdString().c_str());
//        return cvsFileName;
//    }
//    else{
//        qDebug("adcTestCsvFile is empt");
//        return NULL;
//    }
//}

//static bool write_adc_test_file(uint8_t testModuleID, uint8_t voltageNum ,uint16_t testResult)
//{
//    QDateTime dateTime(QDateTime::currentDateTime());
//    QString testTime = dateTime.toString("yy-MM-dd hh:mm::ss");

//    QString writeInfo;
//    writeInfo.append(testTime.append(","));
//    writeInfo.append((QString::number(testModuleID)).append(","));
//    writeInfo.append((QString("%1").arg(voltageNum*0.05)).append(","));
//    writeInfo.append((QString::number(testResult)).append(",\n"));

//    adcTestCsvFile.write(writeInfo.toStdString().c_str());

//    return true;
//}

//static void close_adc_test_file()
//{
//    adcTestCsvFile.close();
//}


static QString creat_cvs_test_file(QFile &csvFile, QString csvfile_path, uint32_t testNumber)
{
    QDateTime dateTime(QDateTime::currentDateTime());
    QString testTime = dateTime.toString("[yy-MM-dd]_[hh-mm-ss]");

    QString cvsFileName = csvfile_path.append("/");
    cvsFileName.append(testTime);
    cvsFileName.append("_[");
    cvsFileName.append(QString::number(testNumber));
    cvsFileName.append("]_");
    cvsFileName.append("times.csv");

    QString csvFistLine = "TestTime,testModuleID,TestCaseType,TestResult,TestValue\n";

    csvFile.setFileName(cvsFileName);

    if (csvFile.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Append))//QFile::Truncate
    {
        QTextStream out(&csvFile);
        out << csvFistLine.toStdString().c_str();
        //csvFile.write(csvFistLine.toStdString().c_str());
        //csvFile.close();
        return cvsFileName;
    }
    else{
        qDebug("cvsFileName is empt");
        return NULL;
    }
}

static void open_csv_file(QFile &csvFile)
{
    csvFile.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Append);
}

static bool write_csv_file(QFile &csvFile, uint8_t testModuleID, enTestCaseCfg_t testCaseType,
                           enTestCaseReturnValue testResult, QString testString)
{
    QDateTime dateTime(QDateTime::currentDateTime());
    QString testTime = dateTime.toString("yy-MM-dd hh:mm::ss");

    QString writeInfo;
    writeInfo.append(testTime.append(","));
    writeInfo.append((QString::number(testModuleID)).append(","));
    writeInfo.append(test_case_type_cover(testCaseType).append(","));

    writeInfo.append(test_result_cover(testResult).append(","));
    writeInfo.append(testString.append(",\n"));
    //csvFile.write(writeInfo.toStdString().c_str());

    QTextStream out(&csvFile);
    out << writeInfo.toStdString().c_str();

    return true;
}

static void close_csv_file(QFile &csvFile)
{
    csvFile.close();
}

static QByteArray format_test_ctrl_procotol_pkge(stTestCtrlProcotolPkg testCtrlProcotolPkgTemp)
{
    QByteArray protocolPackege;
    protocolPackege.clear();
#ifdef DEBUG_LOG_ENABLE
    qDebug("head_code   %04x",  testCtrlProcotolPkgTemp.head_code);
    qDebug("adv_addr    %04x",  testCtrlProcotolPkgTemp.adv_addr);
    qDebug("operat_code %04x",  testCtrlProcotolPkgTemp.operat_code);
    qDebug("data_leng   %04x",  testCtrlProcotolPkgTemp.data_leng);
    qDebug("operat_data %04x",  testCtrlProcotolPkgTemp.operat_data);
    qDebug("tail_code   %04x",  testCtrlProcotolPkgTemp.tail_code);
#endif

    protocolPackege.append(testCtrlProcotolPkgTemp.head_code & 0xFF);
    protocolPackege.append((testCtrlProcotolPkgTemp.head_code & 0xFF00)>>8);
    protocolPackege.append(testCtrlProcotolPkgTemp.adv_addr);
    protocolPackege.append(testCtrlProcotolPkgTemp.operat_code);
    protocolPackege.append(testCtrlProcotolPkgTemp.data_leng);
    if(testCtrlProcotolPkgTemp.data_leng != 0){
        for(uint8_t i =0 ; i<testCtrlProcotolPkgTemp.data_leng;i++)
        {
            protocolPackege.append(*(testCtrlProcotolPkgTemp.operat_data+i));
        }
    }
    protocolPackege.append(testCtrlProcotolPkgTemp.u8crc);
    protocolPackege.append(testCtrlProcotolPkgTemp.tail_code & 0xFF);
    protocolPackege.append((testCtrlProcotolPkgTemp.tail_code & 0xFF00)>>8);

    return protocolPackege;
}

void MainWindow::mxd_serial_recive_data_handle(stTestCtrlProcotolInfo_t testReturnInfo)
{
    g_reciveTestReturnDataFlage = true;

    qDebug("testReturnInfo.testCaseType %d ",testReturnInfo.testCaseType);
    qDebug("testReturnInfo.dataLength %d",testReturnInfo.dataLength);
    qDebug("testReturnInfo.testDataResult %02x ",testReturnInfo.testDataResult[0]);
    qDebug("testReturnInfo.testDataResult %02x ",testReturnInfo.testDataResult[1]);
    qDebug("testReturnInfo.testDataResult %02x ",testReturnInfo.testDataResult[2]);
    qDebug("testReturnInfo.testDataResult %02x ",testReturnInfo.testDataResult[3]);
    qDebug("testReturnInfo.testDataResult %02x ",testReturnInfo.testDataResult[4]);
    emit sig_download_ack_timeout();
    g_stTestReturnInfo = testReturnInfo;
}

void MainWindow::auto_test_recive_timeout_handler()
{
    if(reciveTimer->isActive()){
         reciveTimer->stop();
         g_reciveTimeoutFlage = true;
         qDebug("into timeout");
     }
}

bool MainWindow::send_dfu_cmd_data(QByteArray byteArrayTemp, uint16_t timeout)
{
    g_reciveTimeoutFlage = false;

    // 1. Send Data
    dfu_write_configure_serial_data(byteArrayTemp);

    // 2. Start Timer
    reciveTimer->start(timeout * 500);

    while(true)
    {
        if(g_reciveTimeoutFlage == false)
        {
            if(g_reciveTestReturnDataFlage)
            {
                reciveTimer->stop();
                g_reciveTestReturnDataFlage = false;
                return true;
            }
            else
            {
                delay_msec(10, 1); //wait recive data.
            }
        }
        else
        {
            return false;
        }
    }
}

bool MainWindow::send_auto_test_cmd_data(QByteArray byteArrayTemp, uint16_t timeout)
{
    g_reciveTimeoutFlage = false;

    //1、send data
    //qDebug("--------- 3/3/1 send data -------------");
    //write_test_run_serial_data(byteArrayTemp);
    write_configer_serial_data(byteArrayTemp);

    //2、start timer
    //qDebug("--------- 3/3/2 start timer -------------");
    reciveTimer->start(timeout * 500);

    //3、wait test return value
    //qDebug("--------- 3/3/3 wait return -------------");
    while(true){
        //g_reciveTestReturnDataFlage = true;
        if(g_reciveTimeoutFlage == false){
            if(g_reciveTestReturnDataFlage){
                reciveTimer->stop();
                g_reciveTestReturnDataFlage = false;
                return true;
            } else{
                delay_msec(10, 1); //wait recive data.
            }
        } else{ //recive timeout
            return false;
        }
    }
}


bool MainWindow::high_temp_test_case(uint8_t u8TestID, enTestCaseCfg_t enTestCase, bool bCaseEnable)
{
    uint8_t timeout_s = 20;
    uint8_t u8SendData[8] = {0};
    bool ResultFlg = bool(0);
    uint8_t u8SendNackNum = 3;

    switch(enTestCase)
    {
        case enTestCaseCfg_t::GPIO_TEST://GPIO输入测试
        {
            qDebug("GPIO_TEST");
            //控制电源输出3.3V电压
            set_adc_voltage_value(3.3);
            u8SendData[0] = 1;
            //下发指令开启测试
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, GPIO_TEST_CMD,1,u8SendData);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
                qDebug()<<"SendNum = "<<u8SendNackNum;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == GPIO_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }

            //控制电源输出3.3V电压
            set_adc_voltage_value(0.2);

            u8SendData[0] = 0;
            u8SendNackNum = 3;
            //下发指令开启测试
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, GPIO_TEST_CMD,1,u8SendData);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == GPIO_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::FLASH_TEST:
        {
            qDebug("FLASH_TEST");
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, FLASH_TEST_CMD,0,NULL);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == FLASH_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::TRX_CYC_TEST:
        {
            qDebug("TRX_CYC_TEST");
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, TRX_CYC_TEST_CMD,0,NULL);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == TRX_CYC_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::I2C_TEST:
        {
            qDebug("I2C_TEST");
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, I2C_TEST_CMD,0,NULL);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == I2C_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::SPI_TEST:
        {
            qDebug("SPI_TEST");
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, SPI_TEST_CMD,0,NULL);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == SPI_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::CAN_TEST:
        {
            qDebug("CAN_TEST");
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, CAN_TEST_CMD,0,NULL);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == CAN_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::RF_RX_TEST:
        {
            qDebug("RF_RX_TEST");
            u8SendData[0] = uint8_t(bCaseEnable);
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, RF_RX_TEST_CMD,1,u8SendData);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == RF_RX_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        case enTestCaseCfg_t::RF_TX_TEST:
        {
            qDebug("RF_TX_TEST");
            u8SendData[0] = uint8_t(bCaseEnable);
            test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8TestID, RF_TX_TEST_CMD,1,u8SendData);
            g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
            //serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, timeout_s);
            do{
                send_auto_test_cmd_data(g_sendTestCtrlProcotolPkg, timeout_s);
                u8SendNackNum -= 1;
              }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

            if(!g_reciveTimeoutFlage)
            {
                if(g_stTestReturnInfo.testCaseType == RF_TX_TEST_CMD)
                {
                    if(g_stTestReturnInfo.testDataResult[0] == EN_RET_STA_T::EN_RET_OK)
                    {
                        ResultFlg = bool(1);
                    }
                    else
                    {
                        ResultFlg = bool(0);
                        return ResultFlg;
                    }
                }
            }
            break;
        }
        default:break;
    }

    return ResultFlg;
}

void MainWindow::on_autoTestToolButton_clicked()
{
    QString testCurrentTemp ={};
    QString testCurrentValue ={};

    //1、检查测试相关接口是否打开
    if((true != gConfigeUartOpenStatus))//gTestRunUartOpenStatus))
    {
        QMessageBox::warning(this, u8"提示", u8"存在测试设备没有打开", u8"确定");
        return;
    }

    // 2、检测是否循环执行测试步骤
    while(true)
    {
        testNum++;

        if(testNum == 4294960000){testNum = 0;}

        testFileSavePachName = acquire_data_save_path();
        testFileSavePachName = creat_cvs_test_file(g_CuntDataCsvFile, testFileSavePachName, testNum);

        delay_msec(100,1);
        close_csv_file(g_CuntDataCsvFile);
        bool flag;

        delay_msec(100,1);
        open_csv_file(g_CuntDataCsvFile);//单次测试数据

#if 1
        for(uint8_t advAddrIndex = u8StartChipID; advAddrIndex < u8TotalChipNum; advAddrIndex++)
        {
            testCaseResult = 0;

            for(int init=0; init<8; init++)
            {
                this->g_stHighTestResult[init].TestResult = 0;
            }

            //qDebug()<<("----------- 2、read configer file ------------");
            g_stTestModuleInfo = readTestInfo(advAddrIndex);

            /*执行测试项*/
            uint8_t u8TestValue = this->m_selected_test_case_number;

            allTestCaseTestResult = 0;

            //GPIO_TEST去掉，所以从1开始
            for(uint8_t u8TestCase=TEST_START_INDEX; u8TestCase<enTestCaseCfg_t::ALL_TEST-2; u8TestCase++)// -2是需排除TX RX测试
            {
                if(u8TestValue & (0x01 << u8TestCase))
                {
                    flag = high_temp_test_case(advAddrIndex, enTestCaseCfg_t(u8TestCase), true);

                    this->g_stHighTestResult[u8TestCase].enTestCase = enTestCaseCfg_t(u8TestCase);
                    this->g_stHighTestResult[u8TestCase].TestResult = flag;
                }

                //单次测试间隔时长
                delay_msec(300,1);
            }

            for(uint8_t u8TestCase=TEST_START_INDEX; u8TestCase<enTestCaseCfg_t::ALL_TEST-2; u8TestCase++)
            {
                //allTestCaseTestResult += this->g_stHighTestResult[u8TestCase].TestResult;
                if(this->g_stHighTestResult[u8TestCase].TestResult)
                {
                    allTestCaseTestResult |= (0x01 << u8TestCase);
                }
            }

            /***********************************************************************
             * 判断测试结果，设置LED显示
             * 0 灰色默认状态  1 All测试失败红色  2 All测试通过绿色 3 部分测试未通过黄色
             **********************************************************************/
            if(allTestCaseTestResult != 0)
            {                               //(0x01 << All Test Case -1)all=1, (-1)去除GPIO测试
                if(allTestCaseTestResult == ((0x01 << (enTestCaseCfg_t::ALL_TEST-2)) - 1 - 1))
                {
                    indicate_test_status_led(advAddrIndex,2); // All测试通过绿色
                }
                else
                {
                    indicate_test_status_led(advAddrIndex,3); // 部分测试未通过黄色
                }
                allTestCaseTestResult = 0;
            }
            else
            {
                indicate_test_status_led(advAddrIndex,1);//All测试失败红色
            }

            //将测试数据写入excel中进行保存
            for(uint8_t u8TestCase=TEST_START_INDEX; u8TestCase<enTestCaseCfg_t::ALL_TEST-2; u8TestCase++)
            {
                if(this->g_stHighTestResult[u8TestCase].TestResult)
                {
                    write_csv_file(g_CuntDataCsvFile, advAddrIndex, enTestCaseCfg_t(u8TestCase), TEST_STATUS_PASS, "Pass");
                    delay_msec(100,1);
                }
                else
                {
                    write_csv_file(g_CuntDataCsvFile, advAddrIndex, enTestCaseCfg_t(u8TestCase), TEST_STATUS_FAIL, "Fail");
                    delay_msec(100,1);
                }
            }
        }
#endif
#if 1
        /*Test All Tx on Current*/
        for(uint8_t advAddrIndex = u8StartChipID; advAddrIndex < u8TotalChipNum; advAddrIndex++)
        {
            /*RF Tx On*/
            flag = high_temp_test_case(advAddrIndex, enTestCaseCfg_t::RF_TX_TEST, false);
            this->g_stHighTestResult[enTestCaseCfg_t::RF_TX_TEST].enTestCase = enTestCaseCfg_t::RF_TX_TEST;
            this->g_stHighTestResult[enTestCaseCfg_t::RF_TX_TEST].TestResult = flag;
        }
        delay_msec(1000*5,1); //5s

        /*测试All RF TX ON Total Current*/
        // get and check currel.
        testCurrentTemp = Get_the_current_value();
        testCurrentValue = testCurrentTemp.mid(1,5);
        write_csv_file(g_CuntDataCsvFile, u8TotalChipNum, enTestCaseCfg_t::RF_TX_TEST, TEST_STATUS_PASS, testCurrentTemp);

        delay_msec(1000*10,1); //10s

        /*All Tx OFF*/
        for(uint8_t advAddrIndex = u8StartChipID; advAddrIndex < u8TotalChipNum; advAddrIndex++)
        {
            /*RF Tx Off*/
            flag = high_temp_test_case(advAddrIndex, enTestCaseCfg_t::RF_TX_TEST, true);
            this->g_stHighTestResult[enTestCaseCfg_t::RF_TX_TEST].enTestCase = enTestCaseCfg_t::RF_TX_TEST;
            this->g_stHighTestResult[enTestCaseCfg_t::RF_TX_TEST].TestResult = flag;
        }

        delay_msec(1000*10,1); //10s

        /*Test All Rx on Current*/
        for(uint8_t advAddrIndex = u8StartChipID; advAddrIndex < u8TotalChipNum; advAddrIndex++)
        {
            /*RF Rx On*/
            flag = high_temp_test_case(advAddrIndex, enTestCaseCfg_t::RF_RX_TEST, false);
            this->g_stHighTestResult[enTestCaseCfg_t::RF_RX_TEST].enTestCase = enTestCaseCfg_t::RF_RX_TEST;
            this->g_stHighTestResult[enTestCaseCfg_t::RF_RX_TEST].TestResult = flag;
        }

        testCurrentTemp.clear();
        testCurrentValue.clear();
        testCurrentTemp = Get_the_current_value();
        testCurrentValue = testCurrentTemp.mid(1,5);
        qDebug()<<testCurrentValue;
        write_csv_file(g_CuntDataCsvFile, u8TotalChipNum, enTestCaseCfg_t::RF_RX_TEST, TEST_STATUS_PASS, testCurrentTemp);

        /*All Rx OFF*/
        for(uint8_t advAddrIndex = u8StartChipID; advAddrIndex < u8TotalChipNum; advAddrIndex++)
        {
            /*RF Rx On*/
            flag = high_temp_test_case(advAddrIndex, enTestCaseCfg_t::RF_RX_TEST, true);
            this->g_stHighTestResult[enTestCaseCfg_t::RF_RX_TEST].enTestCase = enTestCaseCfg_t::RF_RX_TEST;
            this->g_stHighTestResult[enTestCaseCfg_t::RF_RX_TEST].TestResult = flag;
        }

#endif

        delay_msec(1000*10,1); //10s

        /*Total Current Test*/
        testCurrentTemp.clear();
        testCurrentValue.clear();
        testCurrentTemp = Get_the_current_value();
        testCurrentValue = testCurrentTemp.mid(0,10);
        write_csv_file(g_CuntDataCsvFile, u8TotalChipNum, enTestCaseCfg_t::ALL_TEST, TEST_STATUS_PASS, testCurrentTemp);

        delay_msec(100,1);
        close_csv_file(g_CuntDataCsvFile);

        // 一轮测试4次 周期为360min 6h
#if 1
        for(uint16_t j = 0; j< 10; j++)//3600*6
        {
            delay_msec(1000,1); //1s
        }
#else
        delay_msec(1000, 3);
#endif
        test_led_status_init();

        qDebug()<<("----------- 6、end ones test ----------------");
    }
}

/********* 2、 script test mode test handler ************/
uint16_t testScriptRunClickNumber       = 0;
static bool  gtestScripConnectStatus    = false;

void MainWindow:: on_scripTestRadioButton_clicked()
{
    //1、disable auto test
    ui->autoTestRadioButton->setChecked(false);
    ui->autoTestToolButton->setDisabled(true);

    //2、enable script test
    ui->scriptNetcomboBox->setEnabled(true);
    ui->scriptPortlineEdit->setEnabled(true);
    ui->scriptToolButton->setEnabled(true);

    ui->ScriptSelectToolButton->setEnabled(true);
    ui->scriptPatchlineEdit->setEnabled(true);
    ui->scriptTestToolButton->setEnabled(true);

    //Get_the_current_value();
}

void MainWindow:: read_tcp_socket_data()
{
    QByteArray  scriptSocketReadTemp;
    scriptSocketReadTemp = scriptTcpSocket->readAll();
}

void MainWindow:: write_tcp_socket_data(QByteArray send_buffer)
{
    if(scriptTcpSocket != nullptr){
        if(scriptTcpSocket->isValid()){
            int script_send_length = scriptTcpSocket->write(send_buffer);
            qDebug("script_send_length: %d", script_send_length);
            if(-1 == script_send_length){
                qDebug(u8"Script_LAN 服务端发送数据失败！\r\n");
                return;
            }
        } else{
            qDebug(u8"Script_LAN 套接字无效！ \r\n");
        }
    }
    if(scriptTcpSocket == nullptr){
        qDebug(u8"脚本没有连接，请连接后操作！ \r\n");
    }
}

void MainWindow:: connect_script_server()
{
    scriptTcpSocket = scriptTcpServer->nextPendingConnection();
    if(NULL==scriptTcpSocket){
        QMessageBox::information(this, u8"QT网络通信", u8"Script_LAN 服务端未正确获取客户端连接！");
    } else{
        qDebug(u8"Script_LAN 客户端成功连接服务端！\r\n");
        gtestScripConnectStatus = true;
        connect(scriptTcpSocket, SIGNAL(readyRead()), this, SLOT(read_tcp_socket_data()));
        connect(scriptTcpSocket, SIGNAL(disconnected()), this, SLOT(disconnect_script_server()));
    }
}

void MainWindow:: disconnect_script_server(void)
{
    gtestScripConnectStatus = false;
    qDebug(u8"Script_LAN 客户端断开连接! \r\n");
}

void MainWindow:: on_scriptToolButton_clicked()
{
    testScriptRunClickNumber++;
    if(1 == (testScriptRunClickNumber % 2)){

        scriptTcpServer = new QTcpServer();
        if(nullptr != scriptTcpServer){
            int port =  ui->scriptPortlineEdit->text().toInt();
            if(!scriptTcpServer->listen(QHostAddress::Any, port)){
                 QMessageBox::information(this, u8"QT网络通信",u8"服务器端监听失败");
                 testScriptRunClickNumber -= 1;
                 qDebug("Script_LAN listen file!\r\n");
            }
            else{
                 ui->scriptToolButton->setText(u8"断连");
                 qDebug("Script_LAN listen Success!\r\n");
            }
            connect(scriptTcpServer, SIGNAL(newConnection()), this, SLOT(connect_script_server()));
         } else{
                qDebug("Script_LAN_tcpServer creat file!\r\n");
         }
     } else{
        if(gtestScripConnectStatus==false){//只有客户端关闭后或者客户端从来没连接, 服务端才可以关闭
            scriptTcpServer->close();
            delete  scriptTcpServer;
            ui->scriptToolButton->setText("连接");
            qDebug("Script_LAN Close Success!\r\n");
        } else {
            testScriptRunClickNumber -= 1;
        }
     }
     if(65530 == testScriptRunClickNumber){ testScriptRunClickNumber = 0; }
}

void MainWindow:: on_ScriptSelectToolButton_clicked()
{
    QString test_script_file_path = QFileDialog::getOpenFileName(this, u8"选择文件","../","*.py");
    test_script_file_path.replace("/","\\");
    QStringList files_name_list = test_script_file_path.split("\\");
    ui->scriptPatchlineEdit->setText(files_name_list.last());
}

void MainWindow:: on_scriptTestToolButton_clicked()
{
    //调用接口进行测试
}

void MainWindow::on_actionHelp_Guid_triggered()
{
    QString chmName = "\\Htol_Test_Tool_User_Guide.chm";
    QString chmPathName = QCoreApplication::applicationDirPath() + chmName;
    chmPathName = chmPathName.replace("/", "\\");
    //QDesktopServices::openUrl(QUrl::fromLocalFile(chmPathName));
    if(QFile(chmPathName).exists()){
        QString filePath = QString("hh.exe %1").arg(chmPathName);
        static QProcess proc;
        proc.close();
        proc.start(filePath);
        qDebug() << "current path exist" <<endl;
    }else{
        qDebug() << "current path not exist" <<endl;

        QString EXEName_src = ":/new/prefix3/Htol_Test_Tool_User_Guide.chm";
        if(QFile(EXEName_src).exists()){
            qDebug() << "and Resource path exist" <<endl;
            QString EXEName_Dst = "~A.chm";
            QFile EXEFile_src(EXEName_src);
            QFile EXEFile_Dst(EXEName_Dst);
           //对资源里的exe进行重新生成
            if(EXEFile_Dst.open (QIODevice::WriteOnly)){
               if(EXEFile_src.open(QIODevice::ReadOnly)){
               QByteArray tmp = EXEFile_src.readAll();
               EXEFile_Dst.write(tmp);
               }
            }
            EXEFile_Dst.close();
            EXEFile_src.close();
            QString filePath = QString("hh.exe %1").arg(EXEName_Dst);
            static QProcess proc;
            proc.close();
            proc.start(filePath);
            while(true){
                if(QProcess::NotRunning == proc.state()){
                    QFile::remove(EXEName_Dst); //删掉chm文件
                    break;
                }
                QEventLoop loop;
                QTimer::singleShot(10, &loop, SLOT(quit()));
                loop.exec();
            }
        }else{
            qDebug() << "And Resource path not exist" <<endl;
            QMessageBox::warning(this, u8"Warning", u8"*.chm file is not exist!", u8"OK");
        }
    }
}

void MainWindow::on_actionsoft_Version_triggered()
{
    QMessageBox *msg = new QMessageBox(QMessageBox::Information, u8"About Htol_Test_Tool",
                                     u8"Htol_Test_Tool Version: 0.2.7\r\n"
                                     "This software is only used to finish High Temperature Operating Life (HTOL) test of maxscend soc chips.\r\n\r\n"
                                     "Copyright ©2024 Maxscend Microelectronics Co.,Ltd All Rights Reserved.\r\n\r\n"
                                     "E-mail: chong.peng@maxscend.com\r\n"
                                     "Developers: Chong Peng", QMessageBox::NoButton | QMessageBox::Ok, this);
    QFont font;
    font.setFamily("Microsoft YaHei");
    font.setPointSize(10);
    msg->setFont(font);
    msg->exec();
}


void MainWindow::on_toolButton_Write_Addr_clicked()
{
    uint8_t Write_Addr = ui->testIdLineEdit->text().toInt(nullptr, 16);
    qDebug("Write_Addr = %d\n", Write_Addr);

    g_reciveTimeoutFlage = false;

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg,0x00, DEVICE_ID_WRITE, 1, &Write_Addr);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
    if(!serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, 10))
    {
        return;
    }


    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg,0x00, DEVICE_ID_READ, 0, nullptr);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);
    //1、send data
    //qDebug("--------- 3/3/1 send data -------------");
    serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, 10);
}


/**************************************************************************************************
* @brief  : slot_set_progressBar_freq_accuracy_value
* @param  : int
* @return : none
* @note   : 设置频偏校准进度条
***************************************************************************************************/
void MainWindow::slot_set_progressBar_freq_accuracy_value(int value)
{
    ui->progressBar->setValue(value);
}

/**************************************************************************************************
* @brief  : slot_textEdit_Log_Warnning
* @param  : int
* @return : none
* @note   : Log显示界面打印关键信息
***************************************************************************************************/
void MainWindow::slot_textEdit_Log_Warnning(QString display)
{
    // 获取 QTextEdit 的文本光标
    QTextCursor cursor(ui->testLogTextBrowser->textCursor());

    // 创建一个 QTextCharFormat 对象，并设置字体样式
    QTextCharFormat format;
    format.setFontWeight(QFont::Bold); // 设置字体加粗

    // 使用 QTextCursor 设置格式
    cursor.setCharFormat(format);

    // 写入文本到 QTextEdit 中
    cursor.insertText(display.append("\r\n"));

    // 滚动到底部
    ui->testLogTextBrowser->moveCursor(QTextCursor::End);
}


/**************************************************************************************************
* @brief  : connect_client
* @param  : int
* @return : none
* @note   : 建立TCP连接
***************************************************************************************************/
void MainWindow::slot_textEdit_Log_setText(QString display)
{
    QDateTime time = QDateTime::currentDateTime();
    QString datatime = time.toString("MM-dd-hh:mm");
    QString time_str = "[";time_str.append(datatime);time_str.append("]");
    //time_str.append(display);
    ui->testLogTextBrowser->insertPlainText(time_str);
    ui->testLogTextBrowser->moveCursor(QTextCursor::End);

    // 获取 QTextEdit 的文本光标
    QTextCursor cursor(ui->testLogTextBrowser->textCursor());

    // 创建一个 QTextCharFormat 对象，并设置字体样式
    QTextCharFormat format;
    format.setFontWeight(QFont::Bold); // 设置字体加粗

    // 使用 QTextCursor 设置格式
    cursor.setCharFormat(format);

    // 写入文本到 QTextEdit 中
    cursor.insertText(display.append("\r\n"));

    // 滚动到底部
    ui->testLogTextBrowser->moveCursor(QTextCursor::End);
}

/**************************************************************************************************
* @brief  : slot_freq_accracy_stop_thread
* @param  : none
* @return : none
* @note   : 停止频偏校准线程
***************************************************************************************************/
void MainWindow::slot_freq_accracy_stop_thread(void)
{
    QDateTime time = QDateTime::currentDateTime();
    QString datatime = time.toString("MM-dd-hh:mm");
    QString time_str = "[";time_str.append(datatime);time_str.append("]");

    ui->FreqCalibrateButton->setText(tr("停止校准"));
    ui->FreqCalibrateButton->setStyleSheet("background-color: rgb(255,255,127)");//黄色
    freq_accuracy->quit();
    freq_accuracy->wait();
    //delete freq_accuracy;
    ui->FreqCalibrateButton->setText(tr("开始校准"));
    ui->FreqCalibrateButton->setStyleSheet("background-color: rgb(0,255,0)");//绿色
    freq_accuracy->terminate();//立即终止线程

    slot_set_progressBar_freq_accuracy_value(100);
}


/**************************************************************************************************
* @brief  : slot_send_freq_accracy_serial
* @param  : uint8_t,uint8_t
* @return : none
* @note   : 频偏校准串口通信控制
***************************************************************************************************/
void MainWindow::slot_send_freq_accracy_serial(uint8_t cmd, uint16_t value)
{
    uint8_t send_data[8] = {0};

    static uint16_t u16CaliValue = 0;

    u16CaliValue = value;

    switch ((EN_FREQ_ACCURACY_T)cmd)
    {
        case Freq_single_tone:
        {
            send_data[0] = 0x01;//Start Single Tone
            send_data[1] = (u16CaliValue >> 0) & 0xFF;
            send_data[2] = (u16CaliValue >> 8) & 0xFF;
            qDebug()<<"Freq_single_tone"<<endl;
            break;
        }
        case Freq_cap_save:
        {
            send_data[0] = 0x00;//Stop Single Tone And Save Value to Flash OTP
            send_data[1] = (u16CaliValue >> 0) & 0xFF;
            send_data[2] = (u16CaliValue >> 8) & 0xFF;
            qDebug()<<"Freq_cap_save,value = "<<value<<endl;
            break;
        }
        default:break;
    }

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg,0x00, DCXO_CALIBRAT_CMD, 3, send_data);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    //1、send data
    //qDebug("--------- 3/3/1 send data -------------");
    serial_send_data_with_timeout(g_sendTestCtrlProcotolPkg, 5);


    if( EN_RET_STA_T::EN_RET_OK != g_stTestReturnInfo.testDataResult[0]){
        //异常报警
        qDebug()<<"Program_Freq_Accuracy_CMD Send Error!"<<endl;
    }

    /*回包解析处理*/
    //回包数据在全局结构体数组中，可直接在线程中获取
}


void MainWindow::on_FreqSpecButton_clicked()
{
    static int clicked_num = 0;
    QDateTime time = QDateTime::currentDateTime();
    QString datatime = time.toString("MM-dd-hh:mm");
    QString time_str = "[";time_str.append(datatime);time_str.append("]");

    if((clicked_num % 2) == 0)
    {
        if(open_client(FREQ_SPEC_CLIENT))
        {
            ui->FreqSpecButton->setText("断连");
            ui->FreqSpecButton->setStyleSheet("background-color: rgb(255,255,127)");//黄色
            ui->FreqSpecAddrLineEdit->setEnabled(false);
            ui->FreqSpecPortlineEdit->setEnabled(false);
            ui->testLogTextBrowser->insertPlainText(time_str.append("TCP Connection Success!\r\n"));
            clicked_num += 1;
        }
        else {
            ui->testLogTextBrowser->insertPlainText(time_str.append("TCP Connection Fail!\r\n"));
            ui->testLogTextBrowser->insertPlainText(time_str.append("Please Check the TCP IP address and hardware connection\r\n"));
        }
    }
    else
    {
        if(close_client(FREQ_SPEC_CLIENT))
        {
            ui->FreqSpecButton->setText("连接");
            ui->FreqSpecButton->setStyleSheet("background-color: rgb(0,255,0)");//绿色
            ui->FreqSpecAddrLineEdit->setEnabled(true);
            ui->FreqSpecPortlineEdit->setEnabled(true);
            ui->testLogTextBrowser->insertPlainText(time_str.append("TCP Disconnection Success!\r\n"));
        }
        clicked_num += 1;
    }
    ui->testLogTextBrowser->moveCursor(QTextCursor::End);
    if(65530 == clicked_num){ clicked_num = 0; }
}

void MainWindow::on_FreqCalibrateButton_clicked()
{
    if(!gFreqSpecOpenStatus)
    {
        ui->testLogTextBrowser->insertPlainText("TCP Disconnection!\r\n");
        QMessageBox::warning(this, u8"提示", u8"未连接频谱仪", u8"确定");
        return;
    }

    if(!gConfigeUartOpenStatus)
    {
        ui->testLogTextBrowser->insertPlainText("未连接测试设备!\r\n");
        QMessageBox::warning(this, u8"提示", u8"串口未连接", u8"确定");
        return;
    }

    static uint16_t clicked_num = 0;
    clicked_num += 1;
    if((clicked_num % 2) == 0)//stop
    {
        ui->FreqCalibrateButton->setText(tr("Start Calibration"));
        ui->FreqCalibrateButton->setStyleSheet("background-color: rgb(0,255,0)");//绿色
        freq_accuracy->terminate();//立即终止线程
    }
    else//start
    {
        ui->FreqCalibrateButton->setText(tr("Stop Calibration"));
        ui->FreqCalibrateButton->setStyleSheet("background-color: rgb(255,255,127)");//黄色
        if(freq_accuracy == nullptr){
            freq_accuracy = new thread_freq_accuracy();
        }
        freq_accuracy->start();
    }
    if(65530 == clicked_num){ clicked_num = 0; }
}

// dfu process

// Macro
#define TARGET_CHIP_FW_UPGRADE_CODE_FLASH_ADDR    0x40000

#define BUILD_UINT32(Byte0, Byte1, Byte2, Byte3)     \
                                       ((uint32_t)((uint32_t)((Byte0)&0x00FF)        + \
                                                  ((uint32_t)((Byte1)&0x00FF) << 8)  + \
                                                  ((uint32_t)((Byte2)&0x00FF) << 16) + \
                                                  ((uint32_t)((Byte3)&0x00FF) << 24)))

// Variable
QString                 localUpgradeFrimwareFileName = {};
stMxdBinInfo            localMxdBinInfo = {};
stChipFirmwareInfo_t    upgradeChipFirmwareInfo;
stFirmwareRestart_t     stFirmwareRestart;
stUpgradeRspInfo_t      upgradeRspInfo;
uint8_t                 g_u8ShakeEnable = 0;
uint8_t                 u8ChipIndex = 0;
uint32_t                g_u32WriteAddr = TARGET_CHIP_FW_UPGRADE_CODE_FLASH_ADDR;



void MainWindow::test_browser_show_log_text(QString text, enLogType logType)
{
    QTime current_time = QTime::currentTime();
    QString current_time_string = current_time.toString("hh:mm:ss.zzz");

    ui->textBrowser_firmwareUpgradeLog->insertPlainText("[");
    ui->textBrowser_firmwareUpgradeLog->insertPlainText(current_time_string);

    switch (logType)
    {
        case CONFIGER_TYPE:
            ui->textBrowser_firmwareUpgradeLog->insertPlainText("]:C--");
            break;

        case SEND_DATA_TYPE:
            ui->textBrowser_firmwareUpgradeLog->insertPlainText("]:S->");
            break;

        case RECIVE_DATA_TYPE:
            ui->textBrowser_firmwareUpgradeLog->insertPlainText("]:R<-");
            break;

        default:
            break;
    }

    ui->textBrowser_firmwareUpgradeLog->insertPlainText(text);
    ui->textBrowser_firmwareUpgradeLog->insertPlainText("\r\n");
    ui->textBrowser_firmwareUpgradeLog->moveCursor(QTextCursor::End);
}


void MainWindow::on_dfu_setting_triggered()
{
    qDebug("TRIGGER DFU SETTING");
    ui->stackedWidget->setCurrentIndex(DFU_SETTING_WIDGET);
}

void MainWindow::on_firmwareLoad_clicked()
{
    localUpgradeFrimwareFileName = QFileDialog::getOpenFileName(this, u8"选择升级文件",
                                                                "../",
                                                                 tr("(*.bin);;(*.hex);"));
    localUpgradeFrimwareFileName.replace("/","\\");
    QStringList FilesNameList = localUpgradeFrimwareFileName.split("\\");
    ui->lineEdit_firmwarePath->setText(FilesNameList.first()+"/../"+FilesNameList.last());
}


void MainWindow::on_firmware_recognize_clicked()
{
    get_mxd_bin_file_info(localUpgradeFrimwareFileName, &localMxdBinInfo);
    qDebug("The crc is:0x%x", localMxdBinInfo.binCrc);

    // clear display
    ui->lineEdit_upgradeChipInfo->clear();
    ui->lineEdit_upgradeRomVersion->clear();
    ui->lineEdit_upgradeBoot2Version->clear();
    ui->lineEdit_upgradeAppVersion->clear();

    // set chiptype
    switch (localMxdBinInfo.chipType)
    {
        case UPGRADE_CHIP_MXD2710:
            ui->lineEdit_upgradeChipInfo->setText("MXD2710");
        break;

       // To do
        default:
            ui->lineEdit_upgradeChipInfo->setText("unknow");
        break;
    }

    // set romversion
    if(localMxdBinInfo.romVersion / 16 < 1)
    {
        ui->lineEdit_upgradeRomVersion->setText("0X0" + QString::number(localMxdBinInfo.romVersion, 16));
    }
    else
    {
        ui->lineEdit_upgradeRomVersion->setText("0X" + QString::number(localMxdBinInfo.romVersion, 16));
    }

    // set bootVersion
    if(localMxdBinInfo.bootVersion / 16 < 1)
    {
        ui->lineEdit_upgradeBoot2Version->setText("0X0" + QString::number(localMxdBinInfo.bootVersion, 16));
    }
    else
    {
        ui->lineEdit_upgradeBoot2Version->setText("0X" + QString::number(localMxdBinInfo.bootVersion, 16));
    }

    // set app version
    if(localMxdBinInfo.appVersion / 4096 > 1)
    {
        ui->lineEdit_upgradeAppVersion->setText("0X" + QString::number(localMxdBinInfo.appVersion, 16));
    }
    else
    {
        if(localMxdBinInfo.appVersion / 256 > 1)
        {
            ui->lineEdit_upgradeAppVersion->setText("0X0" + QString::number(localMxdBinInfo.appVersion, 16));
        }
        else
        {
            if(localMxdBinInfo.appVersion / 16 > 1)
            {
                ui->lineEdit_upgradeAppVersion->setText("0X00" + QString::number(localMxdBinInfo.appVersion,16));
            }
            else
            {
                ui->lineEdit_upgradeAppVersion->setText("0X000" + QString::number(localMxdBinInfo.appVersion,16));
            }
        }
    }

    // Set Bin Size
    float binSize = (float)localMxdBinInfo.binSize/1024;
    qDebug("The bin size is:%f", binSize);

    if(localMxdBinInfo.binSize > 1024 * 512)
    {
        ui->lineEdit_upgradeBinSize->setText("0X" + QString::number(localMxdBinInfo.binSize, 16));
    }
    else
    {
        // display nKB
        ui->lineEdit_upgradeBinSize->setText(QString::number(binSize, 'f', 4) + "KB");
    }
}

void MainWindow::chip_info_display(void)
{
    ui->lineEdit_localChipInfo->clear();
    ui->lineEdit_localromVersion->clear();
    ui->lineEdit_localBoot2Version->clear();
    ui->lineEdit_localAppVersion->clear();

    switch(upgradeChipFirmwareInfo.enUpgradeChipInfo)
    {
        case UPGRADE_CHIP_MXD2710:
        {
            ui->lineEdit_localChipInfo->setText("MXD2710");
        }
        break;

        // ...
        default:
        {
            ui->lineEdit_localChipInfo->setText("unknow");
        }
        break;
    }

    if (upgradeChipFirmwareInfo.u8UpgradeRomVersion / 16 < 1)
    {
        ui->lineEdit_localromVersion->setText("0x0" + QString::number(upgradeChipFirmwareInfo.u8UpgradeRomVersion, 16));
    }
    else
    {
        ui->lineEdit_localromVersion->setText("0x" + QString::number(upgradeChipFirmwareInfo.u8UpgradeRomVersion, 16));
    }

    if(upgradeChipFirmwareInfo.u8UpgradeBoot2Version/16 < 1)
    {
        ui->lineEdit_localBoot2Version->setText("0X0" +QString::number(upgradeChipFirmwareInfo.u8UpgradeBoot2Version,16));
    }
    else
    {
        ui->lineEdit_localBoot2Version->setText("0X" +QString::number(upgradeChipFirmwareInfo.u8UpgradeBoot2Version,16));
    }

    if (upgradeChipFirmwareInfo.u16UpgradeAppVersion / 4096 >= 1)
    {
        ui->lineEdit_localAppVersion->setText("0X" + QString::number(upgradeChipFirmwareInfo.u16UpgradeAppVersion,16));
    }
    else
    {
        if (upgradeChipFirmwareInfo.u16UpgradeAppVersion / 256 >= 1)
        {
            ui->lineEdit_localAppVersion->setText("0X0" + QString::number(upgradeChipFirmwareInfo.u16UpgradeAppVersion,16));
        }
        else
        {
            if (upgradeChipFirmwareInfo.u16UpgradeAppVersion / 16 >= 1)
            {
                ui->lineEdit_localAppVersion->setText("0X00" + QString::number(upgradeChipFirmwareInfo.u16UpgradeAppVersion,16));
            }
            else
            {
                ui->lineEdit_localAppVersion->setText("0X000" + QString::number(upgradeChipFirmwareInfo.u16UpgradeAppVersion,16));
            }
        }
    }
}

void MainWindow::on_chipInfo_recognize_clicked()
{
    uint8_t u8DevNum = ui->lineEdit_localDevNum->text().toInt(nullptr, 16);
    uint8_t u8SendNackNum = 3;

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, GET_CHIP_INFO, 0, NULL);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    do
    {
        send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 2);
        u8SendNackNum -= 1;
        qDebug() << "SendNum = " << u8SendNackNum;

    }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

    if(!g_reciveTimeoutFlage)
    {
        if(g_stTestReturnInfo.testCaseType == GET_CHIP_INFO)
        {
            upgradeChipFirmwareInfo.enUpgradeChipInfo = (enUpgradeChipInfo_t)g_stTestReturnInfo.testDataResult[0];
            upgradeChipFirmwareInfo.u8UpgradeRomVersion  = g_stTestReturnInfo.testDataResult[1];
            upgradeChipFirmwareInfo.u8UpgradeBoot2Version = g_stTestReturnInfo.testDataResult[2];
            upgradeChipFirmwareInfo.u16UpgradeAppVersion = g_stTestReturnInfo.testDataResult[3] + (g_stTestReturnInfo.testDataResult[4] << 8);
            qDebug("The Result data:%d,%d, %d", g_stTestReturnInfo.testDataResult[3], g_stTestReturnInfo.testDataResult[4], upgradeChipFirmwareInfo.u16UpgradeAppVersion);

            chip_info_display();
            test_browser_show_log_text(u8"获取芯片信息成功", CONFIGER_TYPE);
        }
        else
        {
            test_browser_show_log_text(u8"获取芯片信息失败", CONFIGER_TYPE);
        }
    }
}

uint8_t MainWindow::dfu_version_check(uint8_t u8DevNum)
{
    uint8_t u8DfuVersion = 0x00;

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, GET_DFU_INFO, 0, NULL);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    if (true == send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 50))
    {
        if (g_stTestReturnInfo.testCaseType == GET_DFU_INFO)
        {
            u8DfuVersion = g_stTestReturnInfo.testDataResult[0];
            g_u8ShakeEnable = g_stTestReturnInfo.testDataResult[1];
            if (u8DfuVersion != DFU_VERSION)
            {
                return 1;
            }
            else
            {
                return 0;
            }
        }
        else
        {
            // To do
            return 2;
        }
    }
    else
    {
        return 3;
    }
}

uint8_t MainWindow::dfu_send_shake_data(uint8_t u8DevNum)
{
    uint8_t u8handshareFlowBuff[6] = {0};

    //To do
    if (ui->lineEdit_shakeData->text().isEmpty())
    {
        // To do
        QMessageBox::warning(this, u8"提示", u8"握手数据流没有填写", u8"确定");
    }
    else
    {
        QString handshakeDataTemp;
        QString handshakeDataString = ui->lineEdit_shakeData->text();
        QStringList handshakeDataStringlist = handshakeDataString.split(",");

        if (handshakeDataStringlist.size() == 6)
        {
            for (uint8_t i = 0; i < 6; ++i)
            {
                handshakeDataTemp = handshakeDataStringlist[i];
                if (handshakeDataTemp.length() > 2)
                {
                    test_browser_show_log_text(u8"step3:握手数据——输入内容格式错误",CONFIGER_TYPE);
                    return 4;
                }
                u8handshareFlowBuff[i] = handshakeDataTemp.toInt();
            }
        }
        else
        {
            test_browser_show_log_text(u8"step3:握手数据——输入长度格式错误",CONFIGER_TYPE);
            return 5;
        }
    }

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, SHAKE_HAND, 6, u8handshareFlowBuff);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    if (true == send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 50))
    {
        if (g_stTestReturnInfo.testCaseType == SHAKE_HAND)
        {
            if (g_stTestReturnInfo.testDataResult[0] == 0x00)
            {
                return 0;
            }
            else
            {
//                test_browser_show_log_text(u8"step3:step2:握手数据_握手数据失败",CONFIGER_TYPE);
                return 6;
            }
        }
        else
        {
            return 7;
        }
    }
    else
    {
        return 8;
    }
}

uint8_t MainWindow::dfu_upgrade_info_check(uint8_t u8DevNum)
{
    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, GET_CHIP_INFO, 0, NULL);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    if (true == send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 50))
    {
        if (false == get_mxd_bin_file_info(localUpgradeFrimwareFileName, &localMxdBinInfo))
        {
            test_browser_show_log_text(u8"step2.1: upgrade info get fail", CONFIGER_TYPE);
            return 1;
        }

        if (localMxdBinInfo.binFlag != 0x2a4b)
        {
            test_browser_show_log_text(u8"step2.2: chip flag verify fail", CONFIGER_TYPE);
            return 2;
        }

        if (g_stTestReturnInfo.testCaseType == GET_CHIP_INFO)
        {
            upgradeChipFirmwareInfo.enUpgradeChipInfo     = (enUpgradeChipInfo_t)g_stTestReturnInfo.testDataResult[0];
            upgradeChipFirmwareInfo.u8UpgradeRomVersion   = g_stTestReturnInfo.testDataResult[1];
            upgradeChipFirmwareInfo.u8UpgradeBoot2Version = g_stTestReturnInfo.testDataResult[2];
            upgradeChipFirmwareInfo.u16UpgradeAppVersion  = g_stTestReturnInfo.testDataResult[3] + (g_stTestReturnInfo.testDataResult[4] << 8);

            if (upgradeChipFirmwareInfo.enUpgradeChipInfo != localMxdBinInfo.chipType)
            {
                test_browser_show_log_text(u8"step2.3: chip type verify fail", CONFIGER_TYPE);
                return 3;
            }

            if (upgradeChipFirmwareInfo.u8UpgradeRomVersion != localMxdBinInfo.romVersion)
            {
                test_browser_show_log_text(u8"step2.4: rom version verify fail", CONFIGER_TYPE);
                return 4;
            }

            if (upgradeChipFirmwareInfo.u8UpgradeBoot2Version != localMxdBinInfo.bootVersion)
            {
                test_browser_show_log_text(u8"step2.4: boot version verify fail", CONFIGER_TYPE);
                return 5;
            }

//            if (upgradeChipFirmwareInfo.u16UpgradeAppVersion != localMxdBinInfo.appVersion)
//            {
//                test_browser_show_log_text(u8"step2.5:  version verify fail", CONFIGER_TYPE);
//            }
            return 0;
        }
        else
        {
            return 6;
        }
    }
    else
    {
        return 7;
    }
}

uint8_t MainWindow::dfu_upgrade_request_check(uint8_t u8DevNum)
{
    // 1. Send request cmd
    stChipFirmwareInfo_t    upgradeFirmwareInfo;

    upgradeFirmwareInfo.enUpgradeChipInfo     = (enUpgradeChipInfo_t)localMxdBinInfo.chipType;
    upgradeFirmwareInfo.u8UpgradeRomVersion   = localMxdBinInfo.romVersion;
    upgradeFirmwareInfo.u8UpgradeBoot2Version = localMxdBinInfo.bootVersion;
    upgradeFirmwareInfo.u16UpgradeAppVersion  = localMxdBinInfo.appVersion;
    upgradeFirmwareInfo.u32UpgradeCodeSize    = localMxdBinInfo.binSize;
    upgradeFirmwareInfo.u32UpgradeCodeCrc     = localMxdBinInfo.binCrc;

    uint8_t sendCmdBuff[14] = {};
    sendCmdBuff[0] = UPGRADE_CODE_TYPE;
    sendCmdBuff[1] = upgradeFirmwareInfo.enUpgradeChipInfo;
    memcpy(&sendCmdBuff[2], &upgradeFirmwareInfo.u8UpgradeRomVersion, 12);

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, UPGRADE_REQ, sizeof(sendCmdBuff), sendCmdBuff);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    if (true == send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 50))
    {
        if (g_stTestReturnInfo.testCaseType == UPGRADE_REQ)
        {
            upgradeRspInfo.upgradeEnableType       = (enUpgradeEnableType_t)g_stTestReturnInfo.testDataResult[0];
            upgradeRspInfo.upgradeMaxPackageLength = g_stTestReturnInfo.testDataResult[1];

            if (upgradeRspInfo.upgradeEnableType == UPGRADE_ALLOW)
            {
                test_browser_show_log_text(u8"step4.1:upgrade request transmit leng is"+
                                           QString::number(upgradeRspInfo.upgradeMaxPackageLength,10), CONFIGER_TYPE);
                return 0;
            }
            else
            {
                return 1;
            }
        }
        else
        {
            return 2;
        }
    }
    else
    {
        return 3;
    }
}

uint8_t MainWindow::dfu_send_erase_flash_cmd(uint8_t u8DevNum, uint32_t addr, uint16_t length)
{
    uint8_t sendCmdBuf[6] = {0x00};

    sendCmdBuf[0] = addr         & 0xFF;
    sendCmdBuf[1] = (addr >> 8)  & 0xFF;
    sendCmdBuf[2] = (addr >> 16) & 0xFF;
    sendCmdBuf[3] = (addr >> 24) & 0xFF;

    sendCmdBuf[4] = length         & 0xFF;
    sendCmdBuf[5] = (length >> 8)  & 0xFF;

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, ERASE_FLASH, sizeof(sendCmdBuf), sendCmdBuf);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    if (true == send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 50))
    {
        uint8_t flashEraseState;

        flashEraseState = g_stTestReturnInfo.testDataResult[0];
        if ((g_stTestReturnInfo.testCaseType == ERASE_FLASH) && (flashEraseState == 0x00)) //Erase success
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 2;
    }
}

uint8_t MainWindow::dfu_send_firmware_finish_check(uint8_t u8DevNum, uint32_t addr, uint32_t len, uint32_t crc_init)
{
    uint8_t u8SendNackNum = 3;

    stFirmwareCheckInfo_t stFirmwareCheckInfo;
    uint8_t sendCmdBuff[12];

    stFirmwareCheckInfo.u32CrcAddr = addr;
    stFirmwareCheckInfo.u32CrcLen  = len;
    stFirmwareCheckInfo.u32CrcInit = crc_init;
    memcpy(sendCmdBuff, &stFirmwareCheckInfo, sizeof(stFirmwareCheckInfo_t));

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, CHECK_DATA, sizeof(sendCmdBuff), sendCmdBuff);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    do
    {
        send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 2);
        u8SendNackNum -= 1;
        qDebug() << "SendNum = " << u8SendNackNum;

    }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

    if (!g_reciveTimeoutFlage)
    {
        uint32_t u32ReceiveCrc = BUILD_UINT32(g_stTestReturnInfo.testDataResult[0], g_stTestReturnInfo.testDataResult[1],
                                                g_stTestReturnInfo.testDataResult[2], g_stTestReturnInfo.testDataResult[3]);

        qDebug("the Rece crc is:%x", u32ReceiveCrc);
        qDebug("the local crc is:%x",localMxdBinInfo.binCrc);

        if ((g_stTestReturnInfo.testCaseType == CHECK_DATA) && (u32ReceiveCrc == localMxdBinInfo.binCrc))
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 2;
    }
}

uint8_t MainWindow::dfu_send_firmware_data_check(uint8_t u8DevNum, uint32_t index, uint16_t size, uint32_t addr, uint8_t mode)
{
    uint8_t sendCmdBuf[256] = {};
    uint8_t u8SendNackNum = 5;

    sendCmdBuf[0] = addr & 0xFF;
    sendCmdBuf[1] = (addr >> 8) & 0xFF;
    sendCmdBuf[2] = (addr >> 16) & 0xFF;
    sendCmdBuf[3] = (addr >> 24) & 0xFF;

    if (mode == 0)
    {
        get_mxd_bin_file_data(localUpgradeFrimwareFileName, index * size, size, &sendCmdBuf[4]);
    }
    else
    {
        qDebug("SEND FINISH PKAGE");
        qDebug("size is:%d, the index is:%d",size, index);
        get_mxd_bin_file_data(localUpgradeFrimwareFileName, index, size, &sendCmdBuf[4]);
        for (uint8_t i = 0; i < size; i++)
        {
            qDebug("%02x", sendCmdBuf[i + 4]);
        }
    }

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, WRITE_DATA, size + 4, sendCmdBuf);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    do
    {
        send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 5);
        u8SendNackNum -= 1;
        qDebug() << "SendNum = " << u8SendNackNum;

    }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);


    if (!g_reciveTimeoutFlage)
    {
        uint8_t firmwarewWriteState;

        firmwarewWriteState = g_stTestReturnInfo.testDataResult[0];

        if (firmwarewWriteState == 0x00) // Write Success
        {
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 2;
    }
}

uint8_t MainWindow::dfu_send_restart_check(uint8_t u8DevNum)
{
    uint8_t u8SendNackNum = 3;

    test_ctrl_protocol_package_format(&g_stTestCtrlProcotolPkg, u8DevNum, RESET_CHIP, 0, NULL);
    g_sendTestCtrlProcotolPkg = format_test_ctrl_procotol_pkge(g_stTestCtrlProcotolPkg);

    do
    {
        send_dfu_cmd_data(g_sendTestCtrlProcotolPkg, 2);
        u8SendNackNum -= 1;
        qDebug() << "SendNum = " << u8SendNackNum;

    }while((u8SendNackNum > 0) && g_reciveTimeoutFlage);

    if (!g_reciveTimeoutFlage)
    {
        if (g_stTestReturnInfo.testCaseType == RESET_CHIP)
        {
            stFirmwareRestart.u8RstMode    = g_stTestReturnInfo.testDataResult[0];
            stFirmwareRestart.u16DelayTime = g_stTestReturnInfo.testDataResult[1] + (g_stTestReturnInfo.testDataResult[1] << 8);
            return 0;
        }
        else
        {
            return 1;
        }
    }
    else
    {
        return 2;
    }
}

uint8_t MainWindow::dfu_state_machine(uint8_t u8DevNum)
{
    ui->progressBar_upgradeProgress->setValue(0);

    // 1. Check DFU Version
    if (0 != dfu_version_check(u8DevNum))
    {
        test_browser_show_log_text(u8"step1:DFU版本信息校验失败", CONFIGER_TYPE);
        return 1;
    }
    test_browser_show_log_text(u8"step1:DFU版本信息校验成功", CONFIGER_TYPE);
    ui->progressBar_upgradeProgress->setValue(1);

    // 2. Check upgrade info
    if (0 != dfu_upgrade_info_check(u8DevNum))
    {
        test_browser_show_log_text(u8"step2:升级信息校验失败", CONFIGER_TYPE);
        return 2;
    }
    test_browser_show_log_text(u8"step2:升级信息校验成功", CONFIGER_TYPE);
    ui->progressBar_upgradeProgress->setValue(2);

    // 3. DFU Shake Data
    if (g_u8ShakeEnable == UPGRADE_WITH_SHAKE)
    {
        // 3. Send Shake Data
        if (0 != dfu_send_shake_data(u8DevNum))
        {
            test_browser_show_log_text(u8"step3:升级握手失败", CONFIGER_TYPE);
            return 3;
        }
        else
        {
            test_browser_show_log_text(u8"step3:升级握手成功", CONFIGER_TYPE);
            ui->progressBar_upgradeProgress->setValue(3);
        }
    }

    // 4. DFU Requst
    if (0 != dfu_upgrade_request_check(u8DevNum))
    {
        test_browser_show_log_text(u8"step4:升级请求校验失败", CONFIGER_TYPE);
        return 4;
    }
    test_browser_show_log_text(u8"step4:升级请求校验成功", CONFIGER_TYPE);
    ui->progressBar_upgradeProgress->setValue(4);

    // 5. Erase Flash
    uint16_t u16NumOf256Bytes = 0;
    qDebug("localMxdBinInfo.binSize %d ", localMxdBinInfo.binSize);
    if (localMxdBinInfo.binSize <= 64 *1024)
    {
        u16NumOf256Bytes = 64 * 1024 / 256;
    }
    else if (localMxdBinInfo.binSize > 64 *1024 && localMxdBinInfo.binSize <= 128 *1024)
    {
        u16NumOf256Bytes = 128 * 1024 / 256;
    }
    else if (localMxdBinInfo.binSize > 128 * 1024 && localMxdBinInfo.binSize <= 160 * 1024)
    {
        u16NumOf256Bytes = 160 * 1024 / 256;
    }
    else if (localMxdBinInfo.binSize > 160 * 1024 && localMxdBinInfo.binSize <= 192 * 1024)
    {
        u16NumOf256Bytes = 192 * 1024 / 256;
    }
    else
    {
        test_browser_show_log_text(u8"step5:固件超过芯片所能存储的大小", CONFIGER_TYPE);
    }

    if (0 != dfu_send_erase_flash_cmd(u8DevNum, TARGET_CHIP_FW_UPGRADE_CODE_FLASH_ADDR, u16NumOf256Bytes))
    {
        test_browser_show_log_text(u8"step5:Flash 擦除失败", CONFIGER_TYPE);
        return 5;
    }
    ui->progressBar_upgradeProgress->setValue(5);
    test_browser_show_log_text(u8"step5:Flash 擦除完成", CONFIGER_TYPE);

    // 6.Loop Send Firmware Data
    uint16_t upgradeDataSize = upgradeRspInfo.upgradeMaxPackageLength;
    uint16_t loop_times = localMxdBinInfo.binSize / upgradeDataSize;

    qDebug("upgradeDataSize is: %d", upgradeDataSize);
    g_u32WriteAddr = TARGET_CHIP_FW_UPGRADE_CODE_FLASH_ADDR;

    uint8_t upgradProgressStep      = loop_times / 94;
    uint8_t upgradProgressRemainder = loop_times % 94;

    for (uint16_t i = 0; i < loop_times; ++i)
    {
        qDebug("loopTimes %d ", i);
        qDebug("The g_u32WriteAddr is 0x%x ", g_u32WriteAddr);

        if (0 != dfu_send_firmware_data_check(u8DevNum, i, upgradeDataSize, g_u32WriteAddr, 0))
        {
            test_browser_show_log_text(u8"step6:升级数据写入失败", CONFIGER_TYPE);
            return 6;
        }

        g_u32WriteAddr += upgradeDataSize;

        if(i / (upgradProgressStep + 1) < upgradProgressRemainder)
        {
            ui->progressBar_upgradeProgress->setValue(3 + i / (upgradProgressStep + 1));
        }
        else
        {
            uint16_t tempCnt = i - upgradProgressRemainder * (upgradProgressStep + 1);
            ui->progressBar_upgradeProgress->setValue(3 + upgradProgressRemainder + (tempCnt / upgradProgressStep));
        }
    }

    uint32_t write_index = loop_times * upgradeDataSize;
    qDebug("the loop times is:%d, the upgradeDataSize is:%d, the write index is:%d",loop_times, upgradeDataSize, write_index);

    if (localMxdBinInfo.binSize % upgradeDataSize)
    {
        if (0 != dfu_send_firmware_data_check(u8DevNum, write_index , (localMxdBinInfo.binSize % upgradeDataSize), g_u32WriteAddr, 1))
        {
            test_browser_show_log_text(u8"step6:升级数据写入失败", CONFIGER_TYPE);
            return 7;
        }
    }

    test_browser_show_log_text(u8"step6:升级数据写入通过",CONFIGER_TYPE);
    close_mxd_bin_file(localUpgradeFrimwareFileName);

    // 7. Send Firmware Check Cmd
    uint8_t ret = dfu_send_firmware_finish_check(u8DevNum, TARGET_CHIP_FW_UPGRADE_CODE_FLASH_ADDR, localMxdBinInfo.binSize, 0xFFFFFFFF);
    qDebug("ret %d ", ret);
    if (0 != ret)
    {
        test_browser_show_log_text(u8"step7:数据校验失败", CONFIGER_TYPE);
        return 8;
    }
    test_browser_show_log_text(u8"step7:数据校验成功",CONFIGER_TYPE);
    ui->progressBar_upgradeProgress->setValue(99);

    // 8. Send Firmware Reset
    if (0 != dfu_send_restart_check(u8DevNum))
    {
        test_browser_show_log_text(u8"step8:升级重启失败",CONFIGER_TYPE);
        return 9;
    }

    test_browser_show_log_text(u8"step8:升级重启成功",CONFIGER_TYPE);
    ui->progressBar_upgradeProgress->setValue(100);

    return 0;
}


void MainWindow::on_pushButton_startUpgrade_clicked()
{
    uint8_t u8DevNum = ui->lineEdit_localDevNum->text().toInt(nullptr, 16);;
    dfu_state_machine(u8DevNum);
}

void MainWindow::on_pushButton_startUpgradeAll_clicked()
{
    for (u8ChipIndex= u8StartChipID; u8ChipIndex <= u8TotalChipNum; u8ChipIndex++)
    {
        dfu_state_machine(u8ChipIndex);
        ui->progressBar_upgradeProgressAll->setValue(u8ChipIndex * 100 / u8TotalChipNum);
    }
}


void MainWindow::on_pushButton_stopUpgrade_clicked()
{
    u8ChipIndex = u8TotalChipNum;
}

