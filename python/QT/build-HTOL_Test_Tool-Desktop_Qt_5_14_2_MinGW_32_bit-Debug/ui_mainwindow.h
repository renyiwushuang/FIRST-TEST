/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.14.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStackedWidget>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include "device_processing/qt_custom_combobox_net.h"
#include "device_processing/qt_custom_combobox_uart.h"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionstart;
    QAction *actionstop;
    QAction *actionsoft_Version;
    QAction *actionHelp_Guid;
    QAction *actionpause;
    QAction *test_config;
    QAction *test_manager;
    QAction *actionc;
    QAction *actionce;
    QAction *sys_error_configer;
    QAction *dfu_setting;
    QWidget *centralwidget;
    QGridLayout *gridLayout_24;
    QStackedWidget *stackedWidget;
    QWidget *page1;
    QGridLayout *gridLayout_8;
    QGridLayout *gridLayout_5;
    QGroupBox *groupBox_2;
    QGridLayout *gridLayout_14;
    QComboBox *UartBoartComboBox;
    QLineEdit *testIdLineEdit;
    QToolButton *configerUartToolButton;
    QSpacerItem *horizontalSpacer_3;
    QSpacerItem *horizontalSpacer_2;
    QSpacerItem *horizontalSpacer;
    QToolButton *toolButton_Write_Addr;
    QLabel *label_8;
    QLabel *label;
    QSpacerItem *horizontalSpacer_32;
    QSpacerItem *horizontalSpacer_19;
    QSpacerItem *horizontalSpacer_31;
    QLabel *label_2;
    Qt_custom_combobox_uart *UartComboBox;
    QGroupBox *groupBox_4;
    QGridLayout *gridLayout_4;
    QRadioButton *radioButtonTrxTest;
    QRadioButton *radioButtonFlashTest;
    QRadioButton *radioButtonCanTest;
    QSpacerItem *horizontalSpacer_4;
    QLabel *label_9;
    QRadioButton *radioButtonRfTxTest;
    QToolButton *pushButton_TestInfoWrite;
    QLabel *label_10;
    QRadioButton *radioButtonI2cTest;
    QRadioButton *radioButtonGpioTest;
    QRadioButton *radioButton_AllTest;
    QRadioButton *radioButtonRfRxTest;
    QLabel *label_120;
    QSpacerItem *horizontalSpacer_23;
    QRadioButton *radioButtonSpiTest;
    QCheckBox *checkBox_AllID;
    QLineEdit *lineEdit_TestID;
    QComboBox *comboBox_TestExceptionHandle;
    QSpacerItem *horizontalSpacer_5;
    QGroupBox *groupBox_5;
    QGridLayout *gridLayout_16;
    QSpacerItem *horizontalSpacer_24;
    QLabel *label_4;
    QLineEdit *lineEdit_DataSavePath;
    QToolButton *pushButton_DataSavePathBrowse;
    QGroupBox *groupBox_12;
    QGridLayout *gridLayout_7;
    QLineEdit *lineEdit_CfgFilePath;
    QSpacerItem *horizontalSpacer_7;
    QComboBox *comboBox_SystemExceptionHandle;
    QLabel *label_12;
    QSpacerItem *horizontalSpacer_8;
    QToolButton *pushButton_SystemExcepWrite;
    QLabel *label_13;
    QToolButton *pushButton_SaveCfgFile;
    QGroupBox *groupBox_3;
    QGridLayout *gridLayout;
    QToolButton *FreqSpecButton;
    QLineEdit *FreqSpecAddrLineEdit;
    QLabel *label_98;
    QToolButton *FreqCalibrateButton;
    QProgressBar *progressBar;
    QLineEdit *FreqSpecPortlineEdit;
    QGridLayout *gridLayout_9;
    QGroupBox *groupBox;
    QGridLayout *gridLayout_3;
    QSpacerItem *horizontalSpacer_25;
    QLabel *label_95;
    QLineEdit *lineEdit_sendEmilName;
    QSpacerItem *horizontalSpacer_28;
    QSpacerItem *horizontalSpacer_26;
    QLabel *label_97;
    QLineEdit *lineEdit_sendEmilPassword;
    QSpacerItem *horizontalSpacer_29;
    QSpacerItem *horizontalSpacer_27;
    QLabel *label_96;
    QLineEdit *lineEdit_ReciveEmilName;
    QSpacerItem *horizontalSpacer_30;
    QGroupBox *groupBox_6;
    QGridLayout *gridLayout_2;
    QTextBrowser *testLogTextBrowser;
    QWidget *page2;
    QGridLayout *gridLayout_6;
    QGroupBox *groupBox_11;
    QGridLayout *gridLayout_13;
    QLabel *label_73;
    QLabel *label_68;
    QLabel *label_37;
    QLabel *label_58;
    QLabel *label_45;
    QLabel *label_35;
    QLabel *label_81;
    QLabel *label_76;
    QLabel *label_17;
    QLabel *label_50;
    QLabel *label_46;
    QLabel *label_78;
    QLabel *label_16;
    QLabel *label_74;
    QLabel *label_85;
    QLabel *label_60;
    QLabel *label_20;
    QLabel *label_59;
    QLabel *label_49;
    QLabel *label_54;
    QLabel *label_55;
    QLabel *label_84;
    QLabel *label_27;
    QLabel *label_38;
    QLabel *label_19;
    QLabel *label_47;
    QLabel *label_44;
    QLabel *label_69;
    QLabel *label_31;
    QLabel *label_86;
    QLabel *label_23;
    QLabel *label_24;
    QLabel *label_18;
    QLabel *label_40;
    QLabel *label_34;
    QLabel *label_48;
    QLabel *label_83;
    QLabel *label_52;
    QLabel *label_51;
    QLabel *label_82;
    QLabel *label_29;
    QLabel *label_75;
    QLabel *label_22;
    QLabel *label_32;
    QLabel *label_77;
    QLabel *label_53;
    QLabel *label_63;
    QLabel *label_65;
    QLabel *label_62;
    QLabel *label_66;
    QLabel *label_64;
    QLabel *label_57;
    QLabel *label_28;
    QLabel *label_72;
    QLabel *label_61;
    QLabel *label_25;
    QLabel *label_15;
    QLabel *label_71;
    QLabel *label_67;
    QLabel *label_43;
    QLabel *label_79;
    QLabel *label_41;
    QLabel *label_42;
    QLabel *label_56;
    QLabel *label_70;
    QLabel *label_21;
    QLabel *label_26;
    QLabel *label_39;
    QLabel *label_30;
    QLabel *label_33;
    QLabel *label_36;
    QLabel *label_87;
    QLabel *label_88;
    QLabel *label_89;
    QLabel *label_90;
    QLabel *label_91;
    QLabel *label_92;
    QLabel *label_93;
    QLabel *label_94;
    QLabel *label_80;
    QLabel *label_110;
    QVBoxLayout *verticalLayout_3;
    QGroupBox *groupBox_8;
    QGridLayout *gridLayout_10;
    QSpacerItem *horizontalSpacer_9;
    QSpacerItem *horizontalSpacer_18;
    QLabel *label_14;
    QSpacerItem *horizontalSpacer_6;
    QComboBox *runUartBaudRateComboBox;
    QLabel *label_11;
    Qt_custom_combobox_uart *runUartComboBox;
    QToolButton *runUarttoolButton;
    QSpacerItem *horizontalSpacer_33;
    QGroupBox *groupBox_10;
    QGridLayout *gridLayout_11;
    QLineEdit *digtaVoltagePortlineEdit;
    QToolButton *digtalPowerToolButton;
    QSpacerItem *horizontalSpacer_12;
    QSpacerItem *horizontalSpacer_13;
    QLineEdit *digtaVoltagelineEdit;
    QSpacerItem *horizontalSpacer_11;
    QLineEdit *digtalPowerPortlineEdit;
    QLabel *label_6;
    QLineEdit *digtalPowerLineEdit;
    QLabel *label_7;
    QLabel *label_5;
    QToolButton *digtaVoltageToolButton;
    QLineEdit *digtaElectricityPortlineEdit;
    QSpacerItem *horizontalSpacer_14;
    QToolButton *digtaElectricityToolButton;
    QLineEdit *digtaElectricityllineEdit;
    QGroupBox *groupBox_9;
    QGridLayout *gridLayout_12;
    QRadioButton *scripTestRadioButton;
    QToolButton *scriptToolButton;
    QSpacerItem *horizontalSpacer_17;
    QLineEdit *scriptPortlineEdit;
    QSpacerItem *horizontalSpacer_15;
    QToolButton *autoTestToolButton;
    QSpacerItem *horizontalSpacer_16;
    QLineEdit *scriptPatchlineEdit;
    QLabel *label_3;
    QRadioButton *autoTestRadioButton;
    QToolButton *scriptTestToolButton;
    Qt_custom_combobox_net *scriptNetcomboBox;
    QToolButton *ScriptSelectToolButton;
    QWidget *page3;
    QGridLayout *gridLayout_19;
    QVBoxLayout *verticalLayout;
    QGroupBox *groupBox_7;
    QGridLayout *gridLayout_15;
    QProgressBar *progressBar_upgradeProgress;
    QProgressBar *progressBar_upgradeProgressAll;
    QTextBrowser *textBrowser_firmwareUpgradeLog;
    QVBoxLayout *verticalLayout_5;
    QGroupBox *groupBox_16;
    QGridLayout *gridLayout_23;
    QHBoxLayout *horizontalLayout_6;
    QLabel *label_100;
    QLineEdit *lineEdit_firmwarePath;
    QHBoxLayout *horizontalLayout_3;
    QPushButton *chipInfo_recognize;
    QSpacerItem *horizontalSpacer_21;
    QPushButton *firmware_recognize;
    QSpacerItem *horizontalSpacer_22;
    QPushButton *firmwareLoad;
    QGroupBox *groupBox_17;
    QGridLayout *gridLayout_22;
    QGridLayout *gridLayout_18;
    QPushButton *pushButton_startUpgrade;
    QLabel *label_101;
    QPushButton *pushButton_startUpgradeAll;
    QComboBox *comboBox_upgradeMode;
    QPushButton *pushButton_stopUpgrade;
    QGridLayout *gridLayout_17;
    QLineEdit *lineEdit_6;
    QLabel *label_106;
    QLabel *label_107;
    QLineEdit *lineEdit_4;
    QLineEdit *lineEdit_5;
    QLabel *label_109;
    QLabel *label_108;
    QLineEdit *lineEdit_shakeData;
    QLabel *label_105;
    QGridLayout *gridLayout_20;
    QGroupBox *groupBox_21;
    QGridLayout *gridLayout_21;
    QLineEdit *lineEdit_localDevNum;
    QLineEdit *lineEdit_localChipInfo;
    QLineEdit *lineEdit_localAppVersion;
    QLineEdit *lineEdit_localBoot2Version;
    QLineEdit *lineEdit_localromVersion;
    QLabel *label_112;
    QLabel *label_113;
    QLabel *label_114;
    QLabel *label_115;
    QLabel *label_116;
    QGroupBox *groupBox_22;
    QGridLayout *gridLayout_25;
    QLineEdit *lineEdit_upgradeBinSize;
    QLineEdit *lineEdit_upgradeAppVersion;
    QLineEdit *lineEdit_upgradeChipInfo;
    QLineEdit *lineEdit_upgradeBoot2Version;
    QLineEdit *lineEdit_upgradeRomVersion;
    QLabel *label_99;
    QLabel *label_102;
    QLabel *label_103;
    QLabel *label_104;
    QLabel *label_111;
    QMenuBar *menubar;
    QMenu *menu_T;
    QMenu *menu_H;
    QMenu *menu_R;
    QMenu *menu_F;
    QStatusBar *statusbar;
    QToolBar *toolBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->setWindowModality(Qt::ApplicationModal);
        MainWindow->resize(1019, 715);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        QFont font;
        font.setFamily(QString::fromUtf8("Microsoft YaHei UI"));
        MainWindow->setFont(font);
        MainWindow->setMouseTracking(false);
        MainWindow->setTabletTracking(false);
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/new/prefix1/mxdico.ico"), QSize(), QIcon::Normal, QIcon::Off);
        MainWindow->setWindowIcon(icon);
        MainWindow->setToolTipDuration(3);
        MainWindow->setAutoFillBackground(true);
        MainWindow->setToolButtonStyle(Qt::ToolButtonIconOnly);
        MainWindow->setTabShape(QTabWidget::Rounded);
        MainWindow->setDockNestingEnabled(true);
        actionstart = new QAction(MainWindow);
        actionstart->setObjectName(QString::fromUtf8("actionstart"));
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/new/prefix4/run_start.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionstart->setIcon(icon1);
        actionstop = new QAction(MainWindow);
        actionstop->setObjectName(QString::fromUtf8("actionstop"));
        QIcon icon2;
        icon2.addFile(QString::fromUtf8(":/new/prefix4/run_stop.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionstop->setIcon(icon2);
        actionsoft_Version = new QAction(MainWindow);
        actionsoft_Version->setObjectName(QString::fromUtf8("actionsoft_Version"));
        QIcon icon3;
        icon3.addFile(QString::fromUtf8(":/new/prefix5/help-about.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionsoft_Version->setIcon(icon3);
        actionHelp_Guid = new QAction(MainWindow);
        actionHelp_Guid->setObjectName(QString::fromUtf8("actionHelp_Guid"));
        QIcon icon4;
        icon4.addFile(QString::fromUtf8(":/new/prefix5/help_guide.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionHelp_Guid->setIcon(icon4);
        actionpause = new QAction(MainWindow);
        actionpause->setObjectName(QString::fromUtf8("actionpause"));
        QIcon icon5;
        icon5.addFile(QString::fromUtf8(":/new/prefix4/run_pause.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionpause->setIcon(icon5);
        test_config = new QAction(MainWindow);
        test_config->setObjectName(QString::fromUtf8("test_config"));
        QIcon icon6;
        icon6.addFile(QString::fromUtf8(":/new/prefix6/test_cofiger.png"), QSize(), QIcon::Normal, QIcon::Off);
        test_config->setIcon(icon6);
        test_config->setFont(font);
        test_manager = new QAction(MainWindow);
        test_manager->setObjectName(QString::fromUtf8("test_manager"));
        QIcon icon7;
        icon7.addFile(QString::fromUtf8(":/new/prefix6/test_manager.png"), QSize(), QIcon::Normal, QIcon::Off);
        test_manager->setIcon(icon7);
        test_manager->setFont(font);
        actionc = new QAction(MainWindow);
        actionc->setObjectName(QString::fromUtf8("actionc"));
        actionce = new QAction(MainWindow);
        actionce->setObjectName(QString::fromUtf8("actionce"));
        sys_error_configer = new QAction(MainWindow);
        sys_error_configer->setObjectName(QString::fromUtf8("sys_error_configer"));
        dfu_setting = new QAction(MainWindow);
        dfu_setting->setObjectName(QString::fromUtf8("dfu_setting"));
        QIcon icon8;
        icon8.addFile(QString::fromUtf8(":/new/prefix2/fileopen.png"), QSize(), QIcon::Normal, QIcon::Off);
        dfu_setting->setIcon(icon8);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        gridLayout_24 = new QGridLayout(centralwidget);
        gridLayout_24->setObjectName(QString::fromUtf8("gridLayout_24"));
        stackedWidget = new QStackedWidget(centralwidget);
        stackedWidget->setObjectName(QString::fromUtf8("stackedWidget"));
        stackedWidget->setFont(font);
        page1 = new QWidget();
        page1->setObjectName(QString::fromUtf8("page1"));
        gridLayout_8 = new QGridLayout(page1);
        gridLayout_8->setObjectName(QString::fromUtf8("gridLayout_8"));
        gridLayout_5 = new QGridLayout();
        gridLayout_5->setObjectName(QString::fromUtf8("gridLayout_5"));
        groupBox_2 = new QGroupBox(page1);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        QFont font1;
        font1.setFamily(QString::fromUtf8("Microsoft YaHei"));
        groupBox_2->setFont(font1);
        gridLayout_14 = new QGridLayout(groupBox_2);
        gridLayout_14->setObjectName(QString::fromUtf8("gridLayout_14"));
        UartBoartComboBox = new QComboBox(groupBox_2);
        UartBoartComboBox->addItem(QString());
        UartBoartComboBox->addItem(QString());
        UartBoartComboBox->addItem(QString());
        UartBoartComboBox->addItem(QString());
        UartBoartComboBox->setObjectName(QString::fromUtf8("UartBoartComboBox"));

        gridLayout_14->addWidget(UartBoartComboBox, 1, 2, 1, 1);

        testIdLineEdit = new QLineEdit(groupBox_2);
        testIdLineEdit->setObjectName(QString::fromUtf8("testIdLineEdit"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(testIdLineEdit->sizePolicy().hasHeightForWidth());
        testIdLineEdit->setSizePolicy(sizePolicy1);

        gridLayout_14->addWidget(testIdLineEdit, 2, 2, 1, 1);

        configerUartToolButton = new QToolButton(groupBox_2);
        configerUartToolButton->setObjectName(QString::fromUtf8("configerUartToolButton"));
        configerUartToolButton->setMaximumSize(QSize(100, 100));

        gridLayout_14->addWidget(configerUartToolButton, 1, 3, 1, 1);

        horizontalSpacer_3 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_14->addItem(horizontalSpacer_3, 2, 0, 1, 1);

        horizontalSpacer_2 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_14->addItem(horizontalSpacer_2, 1, 0, 1, 1);

        horizontalSpacer = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_14->addItem(horizontalSpacer, 0, 0, 1, 1);

        toolButton_Write_Addr = new QToolButton(groupBox_2);
        toolButton_Write_Addr->setObjectName(QString::fromUtf8("toolButton_Write_Addr"));
        toolButton_Write_Addr->setMaximumSize(QSize(80, 100));

        gridLayout_14->addWidget(toolButton_Write_Addr, 2, 3, 1, 1);

        label_8 = new QLabel(groupBox_2);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        QSizePolicy sizePolicy2(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(label_8->sizePolicy().hasHeightForWidth());
        label_8->setSizePolicy(sizePolicy2);
        label_8->setMaximumSize(QSize(80, 40));

        gridLayout_14->addWidget(label_8, 1, 1, 1, 1);

        label = new QLabel(groupBox_2);
        label->setObjectName(QString::fromUtf8("label"));
        sizePolicy2.setHeightForWidth(label->sizePolicy().hasHeightForWidth());
        label->setSizePolicy(sizePolicy2);
        label->setMaximumSize(QSize(80, 40));

        gridLayout_14->addWidget(label, 0, 1, 1, 1);

        horizontalSpacer_32 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        gridLayout_14->addItem(horizontalSpacer_32, 0, 3, 1, 2);

        horizontalSpacer_19 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_14->addItem(horizontalSpacer_19, 1, 4, 1, 1);

        horizontalSpacer_31 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_14->addItem(horizontalSpacer_31, 2, 4, 1, 1);

        label_2 = new QLabel(groupBox_2);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        sizePolicy2.setHeightForWidth(label_2->sizePolicy().hasHeightForWidth());
        label_2->setSizePolicy(sizePolicy2);
        label_2->setMaximumSize(QSize(80, 40));

        gridLayout_14->addWidget(label_2, 2, 1, 1, 1);

        UartComboBox = new Qt_custom_combobox_uart(groupBox_2);
        UartComboBox->setObjectName(QString::fromUtf8("UartComboBox"));

        gridLayout_14->addWidget(UartComboBox, 0, 2, 1, 1);


        gridLayout_5->addWidget(groupBox_2, 0, 0, 1, 1);

        groupBox_4 = new QGroupBox(page1);
        groupBox_4->setObjectName(QString::fromUtf8("groupBox_4"));
        groupBox_4->setFont(font);
        gridLayout_4 = new QGridLayout(groupBox_4);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        radioButtonTrxTest = new QRadioButton(groupBox_4);
        radioButtonTrxTest->setObjectName(QString::fromUtf8("radioButtonTrxTest"));

        gridLayout_4->addWidget(radioButtonTrxTest, 1, 4, 1, 1);

        radioButtonFlashTest = new QRadioButton(groupBox_4);
        radioButtonFlashTest->setObjectName(QString::fromUtf8("radioButtonFlashTest"));
        radioButtonFlashTest->setChecked(false);

        gridLayout_4->addWidget(radioButtonFlashTest, 1, 3, 1, 1);

        radioButtonCanTest = new QRadioButton(groupBox_4);
        radioButtonCanTest->setObjectName(QString::fromUtf8("radioButtonCanTest"));

        gridLayout_4->addWidget(radioButtonCanTest, 2, 4, 1, 1);

        horizontalSpacer_4 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_4->addItem(horizontalSpacer_4, 0, 0, 1, 1);

        label_9 = new QLabel(groupBox_4);
        label_9->setObjectName(QString::fromUtf8("label_9"));
        sizePolicy2.setHeightForWidth(label_9->sizePolicy().hasHeightForWidth());
        label_9->setSizePolicy(sizePolicy2);
        label_9->setMaximumSize(QSize(80, 40));

        gridLayout_4->addWidget(label_9, 4, 1, 1, 1);

        radioButtonRfTxTest = new QRadioButton(groupBox_4);
        radioButtonRfTxTest->setObjectName(QString::fromUtf8("radioButtonRfTxTest"));

        gridLayout_4->addWidget(radioButtonRfTxTest, 3, 3, 1, 1);

        pushButton_TestInfoWrite = new QToolButton(groupBox_4);
        pushButton_TestInfoWrite->setObjectName(QString::fromUtf8("pushButton_TestInfoWrite"));
        pushButton_TestInfoWrite->setMaximumSize(QSize(80, 100));

        gridLayout_4->addWidget(pushButton_TestInfoWrite, 4, 4, 1, 1);

        label_10 = new QLabel(groupBox_4);
        label_10->setObjectName(QString::fromUtf8("label_10"));
        sizePolicy2.setHeightForWidth(label_10->sizePolicy().hasHeightForWidth());
        label_10->setSizePolicy(sizePolicy2);
        label_10->setMaximumSize(QSize(80, 40));

        gridLayout_4->addWidget(label_10, 0, 1, 1, 1);

        radioButtonI2cTest = new QRadioButton(groupBox_4);
        radioButtonI2cTest->setObjectName(QString::fromUtf8("radioButtonI2cTest"));

        gridLayout_4->addWidget(radioButtonI2cTest, 2, 2, 1, 1);

        radioButtonGpioTest = new QRadioButton(groupBox_4);
        radioButtonGpioTest->setObjectName(QString::fromUtf8("radioButtonGpioTest"));
        radioButtonGpioTest->setChecked(false);

        gridLayout_4->addWidget(radioButtonGpioTest, 1, 2, 1, 1);

        radioButton_AllTest = new QRadioButton(groupBox_4);
        radioButton_AllTest->setObjectName(QString::fromUtf8("radioButton_AllTest"));
        radioButton_AllTest->setChecked(true);

        gridLayout_4->addWidget(radioButton_AllTest, 3, 4, 1, 1);

        radioButtonRfRxTest = new QRadioButton(groupBox_4);
        radioButtonRfRxTest->setObjectName(QString::fromUtf8("radioButtonRfRxTest"));

        gridLayout_4->addWidget(radioButtonRfRxTest, 3, 2, 1, 1);

        label_120 = new QLabel(groupBox_4);
        label_120->setObjectName(QString::fromUtf8("label_120"));
        sizePolicy2.setHeightForWidth(label_120->sizePolicy().hasHeightForWidth());
        label_120->setSizePolicy(sizePolicy2);
        label_120->setMaximumSize(QSize(80, 20));

        gridLayout_4->addWidget(label_120, 1, 1, 1, 1);

        horizontalSpacer_23 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_4->addItem(horizontalSpacer_23, 1, 0, 1, 1);

        radioButtonSpiTest = new QRadioButton(groupBox_4);
        radioButtonSpiTest->setObjectName(QString::fromUtf8("radioButtonSpiTest"));

        gridLayout_4->addWidget(radioButtonSpiTest, 2, 3, 1, 1);

        checkBox_AllID = new QCheckBox(groupBox_4);
        checkBox_AllID->setObjectName(QString::fromUtf8("checkBox_AllID"));
        checkBox_AllID->setChecked(true);

        gridLayout_4->addWidget(checkBox_AllID, 0, 4, 1, 1);

        lineEdit_TestID = new QLineEdit(groupBox_4);
        lineEdit_TestID->setObjectName(QString::fromUtf8("lineEdit_TestID"));
        sizePolicy1.setHeightForWidth(lineEdit_TestID->sizePolicy().hasHeightForWidth());
        lineEdit_TestID->setSizePolicy(sizePolicy1);

        gridLayout_4->addWidget(lineEdit_TestID, 0, 2, 1, 2);

        comboBox_TestExceptionHandle = new QComboBox(groupBox_4);
        comboBox_TestExceptionHandle->addItem(QString());
        comboBox_TestExceptionHandle->addItem(QString());
        comboBox_TestExceptionHandle->addItem(QString());
        comboBox_TestExceptionHandle->addItem(QString());
        comboBox_TestExceptionHandle->setObjectName(QString::fromUtf8("comboBox_TestExceptionHandle"));

        gridLayout_4->addWidget(comboBox_TestExceptionHandle, 4, 2, 1, 2);

        horizontalSpacer_5 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_4->addItem(horizontalSpacer_5, 4, 0, 1, 1);


        gridLayout_5->addWidget(groupBox_4, 1, 0, 1, 1);

        groupBox_5 = new QGroupBox(page1);
        groupBox_5->setObjectName(QString::fromUtf8("groupBox_5"));
        gridLayout_16 = new QGridLayout(groupBox_5);
        gridLayout_16->setObjectName(QString::fromUtf8("gridLayout_16"));
        horizontalSpacer_24 = new QSpacerItem(13, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_16->addItem(horizontalSpacer_24, 0, 0, 1, 1);

        label_4 = new QLabel(groupBox_5);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        sizePolicy2.setHeightForWidth(label_4->sizePolicy().hasHeightForWidth());
        label_4->setSizePolicy(sizePolicy2);
        label_4->setMaximumSize(QSize(80, 40));

        gridLayout_16->addWidget(label_4, 0, 1, 1, 1);

        lineEdit_DataSavePath = new QLineEdit(groupBox_5);
        lineEdit_DataSavePath->setObjectName(QString::fromUtf8("lineEdit_DataSavePath"));
        sizePolicy1.setHeightForWidth(lineEdit_DataSavePath->sizePolicy().hasHeightForWidth());
        lineEdit_DataSavePath->setSizePolicy(sizePolicy1);

        gridLayout_16->addWidget(lineEdit_DataSavePath, 0, 2, 1, 1);

        pushButton_DataSavePathBrowse = new QToolButton(groupBox_5);
        pushButton_DataSavePathBrowse->setObjectName(QString::fromUtf8("pushButton_DataSavePathBrowse"));
        pushButton_DataSavePathBrowse->setMaximumSize(QSize(100, 16777215));

        gridLayout_16->addWidget(pushButton_DataSavePathBrowse, 0, 3, 1, 1);


        gridLayout_5->addWidget(groupBox_5, 2, 0, 1, 1);

        groupBox_12 = new QGroupBox(page1);
        groupBox_12->setObjectName(QString::fromUtf8("groupBox_12"));
        gridLayout_7 = new QGridLayout(groupBox_12);
        gridLayout_7->setObjectName(QString::fromUtf8("gridLayout_7"));
        lineEdit_CfgFilePath = new QLineEdit(groupBox_12);
        lineEdit_CfgFilePath->setObjectName(QString::fromUtf8("lineEdit_CfgFilePath"));
        sizePolicy1.setHeightForWidth(lineEdit_CfgFilePath->sizePolicy().hasHeightForWidth());
        lineEdit_CfgFilePath->setSizePolicy(sizePolicy1);

        gridLayout_7->addWidget(lineEdit_CfgFilePath, 1, 3, 1, 3);

        horizontalSpacer_7 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_7->addItem(horizontalSpacer_7, 1, 0, 1, 1);

        comboBox_SystemExceptionHandle = new QComboBox(groupBox_12);
        comboBox_SystemExceptionHandle->addItem(QString());
        comboBox_SystemExceptionHandle->addItem(QString());
        comboBox_SystemExceptionHandle->addItem(QString());
        comboBox_SystemExceptionHandle->setObjectName(QString::fromUtf8("comboBox_SystemExceptionHandle"));

        gridLayout_7->addWidget(comboBox_SystemExceptionHandle, 0, 3, 1, 3);

        label_12 = new QLabel(groupBox_12);
        label_12->setObjectName(QString::fromUtf8("label_12"));
        sizePolicy2.setHeightForWidth(label_12->sizePolicy().hasHeightForWidth());
        label_12->setSizePolicy(sizePolicy2);
        label_12->setMaximumSize(QSize(80, 40));

        gridLayout_7->addWidget(label_12, 0, 2, 1, 1);

        horizontalSpacer_8 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_7->addItem(horizontalSpacer_8, 0, 0, 1, 1);

        pushButton_SystemExcepWrite = new QToolButton(groupBox_12);
        pushButton_SystemExcepWrite->setObjectName(QString::fromUtf8("pushButton_SystemExcepWrite"));
        pushButton_SystemExcepWrite->setMaximumSize(QSize(100, 100));

        gridLayout_7->addWidget(pushButton_SystemExcepWrite, 0, 6, 1, 1);

        label_13 = new QLabel(groupBox_12);
        label_13->setObjectName(QString::fromUtf8("label_13"));
        sizePolicy2.setHeightForWidth(label_13->sizePolicy().hasHeightForWidth());
        label_13->setSizePolicy(sizePolicy2);
        label_13->setMaximumSize(QSize(80, 40));
        label_13->setFont(font);

        gridLayout_7->addWidget(label_13, 1, 2, 1, 1);

        pushButton_SaveCfgFile = new QToolButton(groupBox_12);
        pushButton_SaveCfgFile->setObjectName(QString::fromUtf8("pushButton_SaveCfgFile"));
        pushButton_SaveCfgFile->setMaximumSize(QSize(100, 25));
        pushButton_SaveCfgFile->setFont(font);

        gridLayout_7->addWidget(pushButton_SaveCfgFile, 1, 6, 1, 1);


        gridLayout_5->addWidget(groupBox_12, 3, 0, 1, 1);

        groupBox_3 = new QGroupBox(page1);
        groupBox_3->setObjectName(QString::fromUtf8("groupBox_3"));
        gridLayout = new QGridLayout(groupBox_3);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        FreqSpecButton = new QToolButton(groupBox_3);
        FreqSpecButton->setObjectName(QString::fromUtf8("FreqSpecButton"));
        FreqSpecButton->setMaximumSize(QSize(100, 25));
        FreqSpecButton->setFont(font);

        gridLayout->addWidget(FreqSpecButton, 0, 4, 1, 1);

        FreqSpecAddrLineEdit = new QLineEdit(groupBox_3);
        FreqSpecAddrLineEdit->setObjectName(QString::fromUtf8("FreqSpecAddrLineEdit"));
        sizePolicy1.setHeightForWidth(FreqSpecAddrLineEdit->sizePolicy().hasHeightForWidth());
        FreqSpecAddrLineEdit->setSizePolicy(sizePolicy1);
        FreqSpecAddrLineEdit->setFont(font);

        gridLayout->addWidget(FreqSpecAddrLineEdit, 0, 1, 1, 2);

        label_98 = new QLabel(groupBox_3);
        label_98->setObjectName(QString::fromUtf8("label_98"));
        sizePolicy2.setHeightForWidth(label_98->sizePolicy().hasHeightForWidth());
        label_98->setSizePolicy(sizePolicy2);
        label_98->setMaximumSize(QSize(80, 25));
        label_98->setFont(font);

        gridLayout->addWidget(label_98, 0, 0, 1, 1);

        FreqCalibrateButton = new QToolButton(groupBox_3);
        FreqCalibrateButton->setObjectName(QString::fromUtf8("FreqCalibrateButton"));
        FreqCalibrateButton->setMaximumSize(QSize(100, 25));
        FreqCalibrateButton->setFont(font);

        gridLayout->addWidget(FreqCalibrateButton, 1, 4, 1, 1);

        progressBar = new QProgressBar(groupBox_3);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setValue(24);
        progressBar->setTextVisible(false);

        gridLayout->addWidget(progressBar, 1, 0, 1, 4);

        FreqSpecPortlineEdit = new QLineEdit(groupBox_3);
        FreqSpecPortlineEdit->setObjectName(QString::fromUtf8("FreqSpecPortlineEdit"));
        sizePolicy2.setHeightForWidth(FreqSpecPortlineEdit->sizePolicy().hasHeightForWidth());
        FreqSpecPortlineEdit->setSizePolicy(sizePolicy2);
        FreqSpecPortlineEdit->setMaximumSize(QSize(40, 16777215));
        FreqSpecPortlineEdit->setFont(font);

        gridLayout->addWidget(FreqSpecPortlineEdit, 0, 3, 1, 1);


        gridLayout_5->addWidget(groupBox_3, 4, 0, 1, 1);


        gridLayout_8->addLayout(gridLayout_5, 0, 0, 1, 1);

        gridLayout_9 = new QGridLayout();
        gridLayout_9->setObjectName(QString::fromUtf8("gridLayout_9"));
        groupBox = new QGroupBox(page1);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        gridLayout_3 = new QGridLayout(groupBox);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        horizontalSpacer_25 = new QSpacerItem(13, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_25, 0, 0, 1, 1);

        label_95 = new QLabel(groupBox);
        label_95->setObjectName(QString::fromUtf8("label_95"));
        sizePolicy2.setHeightForWidth(label_95->sizePolicy().hasHeightForWidth());
        label_95->setSizePolicy(sizePolicy2);
        label_95->setMaximumSize(QSize(80, 40));

        gridLayout_3->addWidget(label_95, 0, 1, 1, 1);

        lineEdit_sendEmilName = new QLineEdit(groupBox);
        lineEdit_sendEmilName->setObjectName(QString::fromUtf8("lineEdit_sendEmilName"));
        sizePolicy1.setHeightForWidth(lineEdit_sendEmilName->sizePolicy().hasHeightForWidth());
        lineEdit_sendEmilName->setSizePolicy(sizePolicy1);

        gridLayout_3->addWidget(lineEdit_sendEmilName, 0, 2, 1, 1);

        horizontalSpacer_28 = new QSpacerItem(40, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_28, 0, 3, 1, 1);

        horizontalSpacer_26 = new QSpacerItem(13, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_26, 1, 0, 1, 1);

        label_97 = new QLabel(groupBox);
        label_97->setObjectName(QString::fromUtf8("label_97"));
        sizePolicy2.setHeightForWidth(label_97->sizePolicy().hasHeightForWidth());
        label_97->setSizePolicy(sizePolicy2);
        label_97->setMaximumSize(QSize(80, 40));

        gridLayout_3->addWidget(label_97, 1, 1, 1, 1);

        lineEdit_sendEmilPassword = new QLineEdit(groupBox);
        lineEdit_sendEmilPassword->setObjectName(QString::fromUtf8("lineEdit_sendEmilPassword"));
        sizePolicy1.setHeightForWidth(lineEdit_sendEmilPassword->sizePolicy().hasHeightForWidth());
        lineEdit_sendEmilPassword->setSizePolicy(sizePolicy1);

        gridLayout_3->addWidget(lineEdit_sendEmilPassword, 1, 2, 1, 1);

        horizontalSpacer_29 = new QSpacerItem(40, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_29, 1, 3, 1, 1);

        horizontalSpacer_27 = new QSpacerItem(13, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_27, 2, 0, 1, 1);

        label_96 = new QLabel(groupBox);
        label_96->setObjectName(QString::fromUtf8("label_96"));
        sizePolicy2.setHeightForWidth(label_96->sizePolicy().hasHeightForWidth());
        label_96->setSizePolicy(sizePolicy2);
        label_96->setMaximumSize(QSize(80, 40));

        gridLayout_3->addWidget(label_96, 2, 1, 1, 1);

        lineEdit_ReciveEmilName = new QLineEdit(groupBox);
        lineEdit_ReciveEmilName->setObjectName(QString::fromUtf8("lineEdit_ReciveEmilName"));
        sizePolicy1.setHeightForWidth(lineEdit_ReciveEmilName->sizePolicy().hasHeightForWidth());
        lineEdit_ReciveEmilName->setSizePolicy(sizePolicy1);

        gridLayout_3->addWidget(lineEdit_ReciveEmilName, 2, 2, 1, 1);

        horizontalSpacer_30 = new QSpacerItem(40, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_3->addItem(horizontalSpacer_30, 2, 3, 1, 1);


        gridLayout_9->addWidget(groupBox, 0, 0, 1, 1);

        groupBox_6 = new QGroupBox(page1);
        groupBox_6->setObjectName(QString::fromUtf8("groupBox_6"));
        groupBox_6->setFont(font);
        gridLayout_2 = new QGridLayout(groupBox_6);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        testLogTextBrowser = new QTextBrowser(groupBox_6);
        testLogTextBrowser->setObjectName(QString::fromUtf8("testLogTextBrowser"));

        gridLayout_2->addWidget(testLogTextBrowser, 0, 0, 1, 1);


        gridLayout_9->addWidget(groupBox_6, 1, 0, 1, 1);


        gridLayout_8->addLayout(gridLayout_9, 0, 1, 1, 1);

        stackedWidget->addWidget(page1);
        page2 = new QWidget();
        page2->setObjectName(QString::fromUtf8("page2"));
        gridLayout_6 = new QGridLayout(page2);
        gridLayout_6->setObjectName(QString::fromUtf8("gridLayout_6"));
        groupBox_11 = new QGroupBox(page2);
        groupBox_11->setObjectName(QString::fromUtf8("groupBox_11"));
        groupBox_11->setFont(font);
        gridLayout_13 = new QGridLayout(groupBox_11);
        gridLayout_13->setObjectName(QString::fromUtf8("gridLayout_13"));
        label_73 = new QLabel(groupBox_11);
        label_73->setObjectName(QString::fromUtf8("label_73"));
        label_73->setFont(font);

        gridLayout_13->addWidget(label_73, 8, 6, 1, 1);

        label_68 = new QLabel(groupBox_11);
        label_68->setObjectName(QString::fromUtf8("label_68"));
        label_68->setFont(font);

        gridLayout_13->addWidget(label_68, 7, 11, 1, 1);

        label_37 = new QLabel(groupBox_11);
        label_37->setObjectName(QString::fromUtf8("label_37"));
        label_37->setFont(font);

        gridLayout_13->addWidget(label_37, 3, 12, 1, 1);

        label_58 = new QLabel(groupBox_11);
        label_58->setObjectName(QString::fromUtf8("label_58"));
        label_58->setFont(font);

        gridLayout_13->addWidget(label_58, 6, 9, 1, 1);

        label_45 = new QLabel(groupBox_11);
        label_45->setObjectName(QString::fromUtf8("label_45"));
        label_45->setFont(font);

        gridLayout_13->addWidget(label_45, 4, 12, 1, 1);

        label_35 = new QLabel(groupBox_11);
        label_35->setObjectName(QString::fromUtf8("label_35"));
        label_35->setFont(font);

        gridLayout_13->addWidget(label_35, 3, 10, 1, 1);

        label_81 = new QLabel(groupBox_11);
        label_81->setObjectName(QString::fromUtf8("label_81"));
        label_81->setFont(font);

        gridLayout_13->addWidget(label_81, 9, 6, 1, 1);

        label_76 = new QLabel(groupBox_11);
        label_76->setObjectName(QString::fromUtf8("label_76"));
        label_76->setFont(font);

        gridLayout_13->addWidget(label_76, 8, 11, 1, 1);

        label_17 = new QLabel(groupBox_11);
        label_17->setObjectName(QString::fromUtf8("label_17"));
        label_17->setFont(font);

        gridLayout_13->addWidget(label_17, 1, 6, 1, 1);

        label_50 = new QLabel(groupBox_11);
        label_50->setObjectName(QString::fromUtf8("label_50"));
        label_50->setFont(font);

        gridLayout_13->addWidget(label_50, 5, 9, 1, 1);

        label_46 = new QLabel(groupBox_11);
        label_46->setObjectName(QString::fromUtf8("label_46"));
        label_46->setFont(font);

        gridLayout_13->addWidget(label_46, 4, 13, 1, 1);

        label_78 = new QLabel(groupBox_11);
        label_78->setObjectName(QString::fromUtf8("label_78"));
        label_78->setFont(font);

        gridLayout_13->addWidget(label_78, 8, 13, 1, 1);

        label_16 = new QLabel(groupBox_11);
        label_16->setObjectName(QString::fromUtf8("label_16"));
        label_16->setFont(font);

        gridLayout_13->addWidget(label_16, 1, 4, 1, 1);

        label_74 = new QLabel(groupBox_11);
        label_74->setObjectName(QString::fromUtf8("label_74"));
        label_74->setFont(font);

        gridLayout_13->addWidget(label_74, 8, 9, 1, 1);

        label_85 = new QLabel(groupBox_11);
        label_85->setObjectName(QString::fromUtf8("label_85"));
        label_85->setFont(font);

        gridLayout_13->addWidget(label_85, 9, 12, 1, 1);

        label_60 = new QLabel(groupBox_11);
        label_60->setObjectName(QString::fromUtf8("label_60"));
        label_60->setFont(font);

        gridLayout_13->addWidget(label_60, 6, 11, 1, 1);

        label_20 = new QLabel(groupBox_11);
        label_20->setObjectName(QString::fromUtf8("label_20"));
        label_20->setFont(font);

        gridLayout_13->addWidget(label_20, 1, 11, 1, 1);

        label_59 = new QLabel(groupBox_11);
        label_59->setObjectName(QString::fromUtf8("label_59"));
        label_59->setFont(font);

        gridLayout_13->addWidget(label_59, 6, 10, 1, 1);

        label_49 = new QLabel(groupBox_11);
        label_49->setObjectName(QString::fromUtf8("label_49"));
        label_49->setFont(font);

        gridLayout_13->addWidget(label_49, 5, 6, 1, 1);

        label_54 = new QLabel(groupBox_11);
        label_54->setObjectName(QString::fromUtf8("label_54"));
        label_54->setFont(font);

        gridLayout_13->addWidget(label_54, 5, 13, 1, 1);

        label_55 = new QLabel(groupBox_11);
        label_55->setObjectName(QString::fromUtf8("label_55"));
        label_55->setFont(font);

        gridLayout_13->addWidget(label_55, 6, 3, 1, 1);

        label_84 = new QLabel(groupBox_11);
        label_84->setObjectName(QString::fromUtf8("label_84"));
        label_84->setFont(font);

        gridLayout_13->addWidget(label_84, 9, 11, 1, 1);

        label_27 = new QLabel(groupBox_11);
        label_27->setObjectName(QString::fromUtf8("label_27"));
        label_27->setFont(font);

        gridLayout_13->addWidget(label_27, 2, 10, 1, 1);

        label_38 = new QLabel(groupBox_11);
        label_38->setObjectName(QString::fromUtf8("label_38"));
        label_38->setFont(font);

        gridLayout_13->addWidget(label_38, 3, 13, 1, 1);

        label_19 = new QLabel(groupBox_11);
        label_19->setObjectName(QString::fromUtf8("label_19"));
        label_19->setFont(font);

        gridLayout_13->addWidget(label_19, 1, 10, 1, 1);

        label_47 = new QLabel(groupBox_11);
        label_47->setObjectName(QString::fromUtf8("label_47"));
        label_47->setFont(font);

        gridLayout_13->addWidget(label_47, 5, 3, 1, 1);

        label_44 = new QLabel(groupBox_11);
        label_44->setObjectName(QString::fromUtf8("label_44"));
        label_44->setFont(font);

        gridLayout_13->addWidget(label_44, 4, 11, 1, 1);

        label_69 = new QLabel(groupBox_11);
        label_69->setObjectName(QString::fromUtf8("label_69"));
        label_69->setFont(font);

        gridLayout_13->addWidget(label_69, 7, 12, 1, 1);

        label_31 = new QLabel(groupBox_11);
        label_31->setObjectName(QString::fromUtf8("label_31"));
        label_31->setFont(font);

        gridLayout_13->addWidget(label_31, 3, 3, 1, 1);

        label_86 = new QLabel(groupBox_11);
        label_86->setObjectName(QString::fromUtf8("label_86"));
        label_86->setFont(font);

        gridLayout_13->addWidget(label_86, 9, 13, 1, 1);

        label_23 = new QLabel(groupBox_11);
        label_23->setObjectName(QString::fromUtf8("label_23"));
        label_23->setFont(font);

        gridLayout_13->addWidget(label_23, 2, 3, 1, 1);

        label_24 = new QLabel(groupBox_11);
        label_24->setObjectName(QString::fromUtf8("label_24"));
        label_24->setFont(font);

        gridLayout_13->addWidget(label_24, 2, 4, 1, 1);

        label_18 = new QLabel(groupBox_11);
        label_18->setObjectName(QString::fromUtf8("label_18"));
        label_18->setFont(font);

        gridLayout_13->addWidget(label_18, 1, 9, 1, 1);

        label_40 = new QLabel(groupBox_11);
        label_40->setObjectName(QString::fromUtf8("label_40"));
        label_40->setFont(font);

        gridLayout_13->addWidget(label_40, 4, 4, 1, 1);

        label_34 = new QLabel(groupBox_11);
        label_34->setObjectName(QString::fromUtf8("label_34"));
        label_34->setFont(font);

        gridLayout_13->addWidget(label_34, 3, 9, 1, 1);

        label_48 = new QLabel(groupBox_11);
        label_48->setObjectName(QString::fromUtf8("label_48"));
        label_48->setFont(font);

        gridLayout_13->addWidget(label_48, 5, 4, 1, 1);

        label_83 = new QLabel(groupBox_11);
        label_83->setObjectName(QString::fromUtf8("label_83"));
        label_83->setFont(font);

        gridLayout_13->addWidget(label_83, 9, 10, 1, 1);

        label_52 = new QLabel(groupBox_11);
        label_52->setObjectName(QString::fromUtf8("label_52"));
        label_52->setFont(font);

        gridLayout_13->addWidget(label_52, 5, 11, 1, 1);

        label_51 = new QLabel(groupBox_11);
        label_51->setObjectName(QString::fromUtf8("label_51"));
        label_51->setFont(font);

        gridLayout_13->addWidget(label_51, 5, 10, 1, 1);

        label_82 = new QLabel(groupBox_11);
        label_82->setObjectName(QString::fromUtf8("label_82"));
        label_82->setFont(font);

        gridLayout_13->addWidget(label_82, 9, 9, 1, 1);

        label_29 = new QLabel(groupBox_11);
        label_29->setObjectName(QString::fromUtf8("label_29"));
        label_29->setFont(font);

        gridLayout_13->addWidget(label_29, 2, 12, 1, 1);

        label_75 = new QLabel(groupBox_11);
        label_75->setObjectName(QString::fromUtf8("label_75"));
        label_75->setFont(font);

        gridLayout_13->addWidget(label_75, 8, 10, 1, 1);

        label_22 = new QLabel(groupBox_11);
        label_22->setObjectName(QString::fromUtf8("label_22"));
        label_22->setFont(font);

        gridLayout_13->addWidget(label_22, 1, 13, 1, 1);

        label_32 = new QLabel(groupBox_11);
        label_32->setObjectName(QString::fromUtf8("label_32"));
        label_32->setFont(font);

        gridLayout_13->addWidget(label_32, 3, 4, 1, 1);

        label_77 = new QLabel(groupBox_11);
        label_77->setObjectName(QString::fromUtf8("label_77"));
        label_77->setFont(font);

        gridLayout_13->addWidget(label_77, 8, 12, 1, 1);

        label_53 = new QLabel(groupBox_11);
        label_53->setObjectName(QString::fromUtf8("label_53"));
        label_53->setFont(font);

        gridLayout_13->addWidget(label_53, 5, 12, 1, 1);

        label_63 = new QLabel(groupBox_11);
        label_63->setObjectName(QString::fromUtf8("label_63"));
        label_63->setFont(font);

        gridLayout_13->addWidget(label_63, 7, 3, 1, 1);

        label_65 = new QLabel(groupBox_11);
        label_65->setObjectName(QString::fromUtf8("label_65"));
        label_65->setFont(font);

        gridLayout_13->addWidget(label_65, 7, 6, 1, 1);

        label_62 = new QLabel(groupBox_11);
        label_62->setObjectName(QString::fromUtf8("label_62"));
        label_62->setFont(font);

        gridLayout_13->addWidget(label_62, 6, 13, 1, 1);

        label_66 = new QLabel(groupBox_11);
        label_66->setObjectName(QString::fromUtf8("label_66"));
        label_66->setFont(font);

        gridLayout_13->addWidget(label_66, 7, 9, 1, 1);

        label_64 = new QLabel(groupBox_11);
        label_64->setObjectName(QString::fromUtf8("label_64"));
        label_64->setFont(font);

        gridLayout_13->addWidget(label_64, 7, 4, 1, 1);

        label_57 = new QLabel(groupBox_11);
        label_57->setObjectName(QString::fromUtf8("label_57"));
        label_57->setFont(font);

        gridLayout_13->addWidget(label_57, 6, 6, 1, 1);

        label_28 = new QLabel(groupBox_11);
        label_28->setObjectName(QString::fromUtf8("label_28"));
        label_28->setFont(font);

        gridLayout_13->addWidget(label_28, 2, 11, 1, 1);

        label_72 = new QLabel(groupBox_11);
        label_72->setObjectName(QString::fromUtf8("label_72"));
        label_72->setFont(font);

        gridLayout_13->addWidget(label_72, 8, 4, 1, 1);

        label_61 = new QLabel(groupBox_11);
        label_61->setObjectName(QString::fromUtf8("label_61"));
        label_61->setFont(font);

        gridLayout_13->addWidget(label_61, 6, 12, 1, 1);

        label_25 = new QLabel(groupBox_11);
        label_25->setObjectName(QString::fromUtf8("label_25"));
        label_25->setFont(font);

        gridLayout_13->addWidget(label_25, 2, 6, 1, 1);

        label_15 = new QLabel(groupBox_11);
        label_15->setObjectName(QString::fromUtf8("label_15"));
        label_15->setFont(font);

        gridLayout_13->addWidget(label_15, 1, 3, 1, 1);

        label_71 = new QLabel(groupBox_11);
        label_71->setObjectName(QString::fromUtf8("label_71"));
        label_71->setFont(font);

        gridLayout_13->addWidget(label_71, 8, 3, 1, 1);

        label_67 = new QLabel(groupBox_11);
        label_67->setObjectName(QString::fromUtf8("label_67"));
        label_67->setFont(font);

        gridLayout_13->addWidget(label_67, 7, 10, 1, 1);

        label_43 = new QLabel(groupBox_11);
        label_43->setObjectName(QString::fromUtf8("label_43"));
        label_43->setFont(font);

        gridLayout_13->addWidget(label_43, 4, 10, 1, 1);

        label_79 = new QLabel(groupBox_11);
        label_79->setObjectName(QString::fromUtf8("label_79"));
        label_79->setFont(font);

        gridLayout_13->addWidget(label_79, 9, 3, 1, 1);

        label_41 = new QLabel(groupBox_11);
        label_41->setObjectName(QString::fromUtf8("label_41"));
        label_41->setFont(font);

        gridLayout_13->addWidget(label_41, 4, 6, 1, 1);

        label_42 = new QLabel(groupBox_11);
        label_42->setObjectName(QString::fromUtf8("label_42"));
        label_42->setFont(font);

        gridLayout_13->addWidget(label_42, 4, 9, 1, 1);

        label_56 = new QLabel(groupBox_11);
        label_56->setObjectName(QString::fromUtf8("label_56"));
        label_56->setFont(font);

        gridLayout_13->addWidget(label_56, 6, 4, 1, 1);

        label_70 = new QLabel(groupBox_11);
        label_70->setObjectName(QString::fromUtf8("label_70"));
        label_70->setFont(font);

        gridLayout_13->addWidget(label_70, 7, 13, 1, 1);

        label_21 = new QLabel(groupBox_11);
        label_21->setObjectName(QString::fromUtf8("label_21"));
        label_21->setFont(font);

        gridLayout_13->addWidget(label_21, 1, 12, 1, 1);

        label_26 = new QLabel(groupBox_11);
        label_26->setObjectName(QString::fromUtf8("label_26"));
        label_26->setFont(font);

        gridLayout_13->addWidget(label_26, 2, 9, 1, 1);

        label_39 = new QLabel(groupBox_11);
        label_39->setObjectName(QString::fromUtf8("label_39"));
        label_39->setFont(font);

        gridLayout_13->addWidget(label_39, 4, 3, 1, 1);

        label_30 = new QLabel(groupBox_11);
        label_30->setObjectName(QString::fromUtf8("label_30"));
        label_30->setFont(font);

        gridLayout_13->addWidget(label_30, 2, 13, 1, 1);

        label_33 = new QLabel(groupBox_11);
        label_33->setObjectName(QString::fromUtf8("label_33"));
        label_33->setFont(font);

        gridLayout_13->addWidget(label_33, 3, 6, 1, 1);

        label_36 = new QLabel(groupBox_11);
        label_36->setObjectName(QString::fromUtf8("label_36"));
        label_36->setFont(font);

        gridLayout_13->addWidget(label_36, 3, 11, 1, 1);

        label_87 = new QLabel(groupBox_11);
        label_87->setObjectName(QString::fromUtf8("label_87"));
        label_87->setFont(font);

        gridLayout_13->addWidget(label_87, 10, 3, 1, 1);

        label_88 = new QLabel(groupBox_11);
        label_88->setObjectName(QString::fromUtf8("label_88"));
        label_88->setFont(font);

        gridLayout_13->addWidget(label_88, 10, 4, 1, 1);

        label_89 = new QLabel(groupBox_11);
        label_89->setObjectName(QString::fromUtf8("label_89"));
        label_89->setFont(font);

        gridLayout_13->addWidget(label_89, 10, 6, 1, 1);

        label_90 = new QLabel(groupBox_11);
        label_90->setObjectName(QString::fromUtf8("label_90"));
        label_90->setFont(font);

        gridLayout_13->addWidget(label_90, 10, 9, 1, 1);

        label_91 = new QLabel(groupBox_11);
        label_91->setObjectName(QString::fromUtf8("label_91"));
        label_91->setFont(font);

        gridLayout_13->addWidget(label_91, 10, 10, 1, 1);

        label_92 = new QLabel(groupBox_11);
        label_92->setObjectName(QString::fromUtf8("label_92"));
        label_92->setFont(font);

        gridLayout_13->addWidget(label_92, 10, 11, 1, 1);

        label_93 = new QLabel(groupBox_11);
        label_93->setObjectName(QString::fromUtf8("label_93"));
        label_93->setFont(font);

        gridLayout_13->addWidget(label_93, 10, 12, 1, 1);

        label_94 = new QLabel(groupBox_11);
        label_94->setObjectName(QString::fromUtf8("label_94"));
        label_94->setFont(font);

        gridLayout_13->addWidget(label_94, 10, 13, 1, 1);

        label_80 = new QLabel(groupBox_11);
        label_80->setObjectName(QString::fromUtf8("label_80"));
        label_80->setFont(font);

        gridLayout_13->addWidget(label_80, 9, 4, 1, 1);

        label_110 = new QLabel(groupBox_11);
        label_110->setObjectName(QString::fromUtf8("label_110"));
        sizePolicy2.setHeightForWidth(label_110->sizePolicy().hasHeightForWidth());
        label_110->setSizePolicy(sizePolicy2);
        label_110->setMaximumSize(QSize(60, 12));
        QFont font2;
        font2.setFamily(QString::fromUtf8("Microsoft YaHei UI"));
        font2.setBold(false);
        font2.setWeight(50);
        label_110->setFont(font2);
        label_110->setStyleSheet(QString::fromUtf8("color: rgb(0, 85, 255);\n"
"color: rgb(255, 0, 0);"));

        gridLayout_13->addWidget(label_110, 11, 13, 1, 1);


        gridLayout_6->addWidget(groupBox_11, 0, 0, 1, 1);

        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        groupBox_8 = new QGroupBox(page2);
        groupBox_8->setObjectName(QString::fromUtf8("groupBox_8"));
        groupBox_8->setFont(font);
        gridLayout_10 = new QGridLayout(groupBox_8);
        gridLayout_10->setObjectName(QString::fromUtf8("gridLayout_10"));
        horizontalSpacer_9 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_10->addItem(horizontalSpacer_9, 1, 0, 1, 1);

        horizontalSpacer_18 = new QSpacerItem(20, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_10->addItem(horizontalSpacer_18, 1, 5, 1, 1);

        label_14 = new QLabel(groupBox_8);
        label_14->setObjectName(QString::fromUtf8("label_14"));
        sizePolicy2.setHeightForWidth(label_14->sizePolicy().hasHeightForWidth());
        label_14->setSizePolicy(sizePolicy2);
        label_14->setMaximumSize(QSize(60, 25));
        label_14->setFont(font);

        gridLayout_10->addWidget(label_14, 1, 1, 1, 1);

        horizontalSpacer_6 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_10->addItem(horizontalSpacer_6, 0, 0, 1, 1);

        runUartBaudRateComboBox = new QComboBox(groupBox_8);
        runUartBaudRateComboBox->addItem(QString());
        runUartBaudRateComboBox->addItem(QString());
        runUartBaudRateComboBox->addItem(QString());
        runUartBaudRateComboBox->addItem(QString());
        runUartBaudRateComboBox->setObjectName(QString::fromUtf8("runUartBaudRateComboBox"));
        sizePolicy1.setHeightForWidth(runUartBaudRateComboBox->sizePolicy().hasHeightForWidth());
        runUartBaudRateComboBox->setSizePolicy(sizePolicy1);
        runUartBaudRateComboBox->setMaximumSize(QSize(150, 25));
        runUartBaudRateComboBox->setFont(font);

        gridLayout_10->addWidget(runUartBaudRateComboBox, 1, 2, 1, 1);

        label_11 = new QLabel(groupBox_8);
        label_11->setObjectName(QString::fromUtf8("label_11"));
        sizePolicy2.setHeightForWidth(label_11->sizePolicy().hasHeightForWidth());
        label_11->setSizePolicy(sizePolicy2);
        label_11->setMaximumSize(QSize(80, 25));
        label_11->setFont(font);

        gridLayout_10->addWidget(label_11, 0, 1, 1, 1);

        runUartComboBox = new Qt_custom_combobox_uart(groupBox_8);
        runUartComboBox->setObjectName(QString::fromUtf8("runUartComboBox"));
        sizePolicy1.setHeightForWidth(runUartComboBox->sizePolicy().hasHeightForWidth());
        runUartComboBox->setSizePolicy(sizePolicy1);
        runUartComboBox->setMaximumSize(QSize(150, 25));
        runUartComboBox->setFont(font);

        gridLayout_10->addWidget(runUartComboBox, 0, 2, 1, 1);

        runUarttoolButton = new QToolButton(groupBox_8);
        runUarttoolButton->setObjectName(QString::fromUtf8("runUarttoolButton"));
        runUarttoolButton->setMaximumSize(QSize(100, 25));
        runUarttoolButton->setFont(font);

        gridLayout_10->addWidget(runUarttoolButton, 1, 4, 1, 1);

        horizontalSpacer_33 = new QSpacerItem(10, 20, QSizePolicy::Preferred, QSizePolicy::Minimum);

        gridLayout_10->addItem(horizontalSpacer_33, 0, 4, 1, 2);


        verticalLayout_3->addWidget(groupBox_8);

        groupBox_10 = new QGroupBox(page2);
        groupBox_10->setObjectName(QString::fromUtf8("groupBox_10"));
        groupBox_10->setFont(font);
        gridLayout_11 = new QGridLayout(groupBox_10);
        gridLayout_11->setObjectName(QString::fromUtf8("gridLayout_11"));
        digtaVoltagePortlineEdit = new QLineEdit(groupBox_10);
        digtaVoltagePortlineEdit->setObjectName(QString::fromUtf8("digtaVoltagePortlineEdit"));
        sizePolicy2.setHeightForWidth(digtaVoltagePortlineEdit->sizePolicy().hasHeightForWidth());
        digtaVoltagePortlineEdit->setSizePolicy(sizePolicy2);
        digtaVoltagePortlineEdit->setMaximumSize(QSize(40, 16777215));
        digtaVoltagePortlineEdit->setFont(font);

        gridLayout_11->addWidget(digtaVoltagePortlineEdit, 3, 4, 1, 1);

        digtalPowerToolButton = new QToolButton(groupBox_10);
        digtalPowerToolButton->setObjectName(QString::fromUtf8("digtalPowerToolButton"));
        digtalPowerToolButton->setMaximumSize(QSize(100, 25));
        digtalPowerToolButton->setFont(font);

        gridLayout_11->addWidget(digtalPowerToolButton, 0, 5, 1, 1);

        horizontalSpacer_12 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_11->addItem(horizontalSpacer_12, 1, 1, 1, 1);

        horizontalSpacer_13 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_11->addItem(horizontalSpacer_13, 3, 1, 1, 1);

        digtaVoltagelineEdit = new QLineEdit(groupBox_10);
        digtaVoltagelineEdit->setObjectName(QString::fromUtf8("digtaVoltagelineEdit"));
        sizePolicy1.setHeightForWidth(digtaVoltagelineEdit->sizePolicy().hasHeightForWidth());
        digtaVoltagelineEdit->setSizePolicy(sizePolicy1);
        digtaVoltagelineEdit->setFont(font);

        gridLayout_11->addWidget(digtaVoltagelineEdit, 3, 3, 1, 1);

        horizontalSpacer_11 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_11->addItem(horizontalSpacer_11, 0, 1, 1, 1);

        digtalPowerPortlineEdit = new QLineEdit(groupBox_10);
        digtalPowerPortlineEdit->setObjectName(QString::fromUtf8("digtalPowerPortlineEdit"));
        sizePolicy2.setHeightForWidth(digtalPowerPortlineEdit->sizePolicy().hasHeightForWidth());
        digtalPowerPortlineEdit->setSizePolicy(sizePolicy2);
        digtalPowerPortlineEdit->setMaximumSize(QSize(40, 16777215));
        digtalPowerPortlineEdit->setFont(font);

        gridLayout_11->addWidget(digtalPowerPortlineEdit, 0, 4, 1, 1);

        label_6 = new QLabel(groupBox_10);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setMaximumSize(QSize(80, 25));
        label_6->setFont(font);

        gridLayout_11->addWidget(label_6, 1, 2, 1, 1);

        digtalPowerLineEdit = new QLineEdit(groupBox_10);
        digtalPowerLineEdit->setObjectName(QString::fromUtf8("digtalPowerLineEdit"));
        sizePolicy1.setHeightForWidth(digtalPowerLineEdit->sizePolicy().hasHeightForWidth());
        digtalPowerLineEdit->setSizePolicy(sizePolicy1);
        digtalPowerLineEdit->setFont(font);

        gridLayout_11->addWidget(digtalPowerLineEdit, 0, 3, 1, 1);

        label_7 = new QLabel(groupBox_10);
        label_7->setObjectName(QString::fromUtf8("label_7"));
        label_7->setMaximumSize(QSize(80, 25));
        label_7->setFont(font);

        gridLayout_11->addWidget(label_7, 3, 2, 1, 1);

        label_5 = new QLabel(groupBox_10);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        sizePolicy2.setHeightForWidth(label_5->sizePolicy().hasHeightForWidth());
        label_5->setSizePolicy(sizePolicy2);
        label_5->setMaximumSize(QSize(80, 25));
        label_5->setFont(font);

        gridLayout_11->addWidget(label_5, 0, 2, 1, 1);

        digtaVoltageToolButton = new QToolButton(groupBox_10);
        digtaVoltageToolButton->setObjectName(QString::fromUtf8("digtaVoltageToolButton"));
        digtaVoltageToolButton->setMaximumSize(QSize(100, 25));
        digtaVoltageToolButton->setFont(font);

        gridLayout_11->addWidget(digtaVoltageToolButton, 3, 5, 1, 1);

        digtaElectricityPortlineEdit = new QLineEdit(groupBox_10);
        digtaElectricityPortlineEdit->setObjectName(QString::fromUtf8("digtaElectricityPortlineEdit"));
        sizePolicy2.setHeightForWidth(digtaElectricityPortlineEdit->sizePolicy().hasHeightForWidth());
        digtaElectricityPortlineEdit->setSizePolicy(sizePolicy2);
        digtaElectricityPortlineEdit->setMaximumSize(QSize(40, 16777215));
        digtaElectricityPortlineEdit->setFont(font);

        gridLayout_11->addWidget(digtaElectricityPortlineEdit, 1, 4, 1, 1);

        horizontalSpacer_14 = new QSpacerItem(20, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_11->addItem(horizontalSpacer_14, 1, 6, 1, 1);

        digtaElectricityToolButton = new QToolButton(groupBox_10);
        digtaElectricityToolButton->setObjectName(QString::fromUtf8("digtaElectricityToolButton"));
        digtaElectricityToolButton->setMaximumSize(QSize(100, 25));
        digtaElectricityToolButton->setFont(font);

        gridLayout_11->addWidget(digtaElectricityToolButton, 1, 5, 1, 1);

        digtaElectricityllineEdit = new QLineEdit(groupBox_10);
        digtaElectricityllineEdit->setObjectName(QString::fromUtf8("digtaElectricityllineEdit"));
        sizePolicy1.setHeightForWidth(digtaElectricityllineEdit->sizePolicy().hasHeightForWidth());
        digtaElectricityllineEdit->setSizePolicy(sizePolicy1);
        digtaElectricityllineEdit->setFont(font);

        gridLayout_11->addWidget(digtaElectricityllineEdit, 1, 3, 1, 1);


        verticalLayout_3->addWidget(groupBox_10);

        groupBox_9 = new QGroupBox(page2);
        groupBox_9->setObjectName(QString::fromUtf8("groupBox_9"));
        groupBox_9->setFont(font);
        gridLayout_12 = new QGridLayout(groupBox_9);
        gridLayout_12->setObjectName(QString::fromUtf8("gridLayout_12"));
        scripTestRadioButton = new QRadioButton(groupBox_9);
        scripTestRadioButton->setObjectName(QString::fromUtf8("scripTestRadioButton"));
        scripTestRadioButton->setFont(font);
        scripTestRadioButton->setCheckable(true);

        gridLayout_12->addWidget(scripTestRadioButton, 1, 1, 1, 1);

        scriptToolButton = new QToolButton(groupBox_9);
        scriptToolButton->setObjectName(QString::fromUtf8("scriptToolButton"));
        scriptToolButton->setMaximumSize(QSize(100, 25));
        scriptToolButton->setFont(font);
        scriptToolButton->setCheckable(false);

        gridLayout_12->addWidget(scriptToolButton, 2, 6, 1, 1);

        horizontalSpacer_17 = new QSpacerItem(20, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_12->addItem(horizontalSpacer_17, 1, 7, 1, 1);

        scriptPortlineEdit = new QLineEdit(groupBox_9);
        scriptPortlineEdit->setObjectName(QString::fromUtf8("scriptPortlineEdit"));
        sizePolicy2.setHeightForWidth(scriptPortlineEdit->sizePolicy().hasHeightForWidth());
        scriptPortlineEdit->setSizePolicy(sizePolicy2);
        scriptPortlineEdit->setMaximumSize(QSize(40, 16777215));
        scriptPortlineEdit->setFont(font);

        gridLayout_12->addWidget(scriptPortlineEdit, 2, 5, 1, 1);

        horizontalSpacer_15 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_12->addItem(horizontalSpacer_15, 1, 0, 1, 1);

        autoTestToolButton = new QToolButton(groupBox_9);
        autoTestToolButton->setObjectName(QString::fromUtf8("autoTestToolButton"));
        autoTestToolButton->setMaximumSize(QSize(100, 25));
        autoTestToolButton->setFont(font);

        gridLayout_12->addWidget(autoTestToolButton, 0, 6, 1, 1);

        horizontalSpacer_16 = new QSpacerItem(10, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

        gridLayout_12->addItem(horizontalSpacer_16, 0, 0, 1, 1);

        scriptPatchlineEdit = new QLineEdit(groupBox_9);
        scriptPatchlineEdit->setObjectName(QString::fromUtf8("scriptPatchlineEdit"));
        sizePolicy1.setHeightForWidth(scriptPatchlineEdit->sizePolicy().hasHeightForWidth());
        scriptPatchlineEdit->setSizePolicy(sizePolicy1);
        scriptPatchlineEdit->setFont(font);

        gridLayout_12->addWidget(scriptPatchlineEdit, 3, 3, 1, 3);

        label_3 = new QLabel(groupBox_9);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        sizePolicy2.setHeightForWidth(label_3->sizePolicy().hasHeightForWidth());
        label_3->setSizePolicy(sizePolicy2);
        label_3->setMaximumSize(QSize(80, 25));
        label_3->setFont(font);

        gridLayout_12->addWidget(label_3, 2, 1, 1, 1);

        autoTestRadioButton = new QRadioButton(groupBox_9);
        autoTestRadioButton->setObjectName(QString::fromUtf8("autoTestRadioButton"));
        autoTestRadioButton->setFont(font);
        autoTestRadioButton->setChecked(true);

        gridLayout_12->addWidget(autoTestRadioButton, 0, 1, 1, 1);

        scriptTestToolButton = new QToolButton(groupBox_9);
        scriptTestToolButton->setObjectName(QString::fromUtf8("scriptTestToolButton"));
        scriptTestToolButton->setFont(font);
        scriptTestToolButton->setCheckable(false);

        gridLayout_12->addWidget(scriptTestToolButton, 3, 6, 1, 1);

        scriptNetcomboBox = new Qt_custom_combobox_net(groupBox_9);
        scriptNetcomboBox->setObjectName(QString::fromUtf8("scriptNetcomboBox"));
        scriptNetcomboBox->setMaximumSize(QSize(120, 16777215));
        scriptNetcomboBox->setFont(font);

        gridLayout_12->addWidget(scriptNetcomboBox, 2, 3, 1, 2);

        ScriptSelectToolButton = new QToolButton(groupBox_9);
        ScriptSelectToolButton->setObjectName(QString::fromUtf8("ScriptSelectToolButton"));
        ScriptSelectToolButton->setMaximumSize(QSize(80, 25));
        ScriptSelectToolButton->setFont(font);
        ScriptSelectToolButton->setCheckable(false);

        gridLayout_12->addWidget(ScriptSelectToolButton, 3, 1, 1, 1);


        verticalLayout_3->addWidget(groupBox_9);

        verticalLayout_3->setStretch(0, 2);
        verticalLayout_3->setStretch(1, 3);
        verticalLayout_3->setStretch(2, 4);

        gridLayout_6->addLayout(verticalLayout_3, 0, 1, 1, 1);

        gridLayout_6->setColumnStretch(0, 3);
        gridLayout_6->setColumnStretch(1, 2);
        gridLayout_6->setColumnMinimumWidth(0, 3);
        gridLayout_6->setColumnMinimumWidth(1, 2);
        stackedWidget->addWidget(page2);
        page3 = new QWidget();
        page3->setObjectName(QString::fromUtf8("page3"));
        gridLayout_19 = new QGridLayout(page3);
        gridLayout_19->setObjectName(QString::fromUtf8("gridLayout_19"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        groupBox_7 = new QGroupBox(page3);
        groupBox_7->setObjectName(QString::fromUtf8("groupBox_7"));
        gridLayout_15 = new QGridLayout(groupBox_7);
        gridLayout_15->setObjectName(QString::fromUtf8("gridLayout_15"));
        progressBar_upgradeProgress = new QProgressBar(groupBox_7);
        progressBar_upgradeProgress->setObjectName(QString::fromUtf8("progressBar_upgradeProgress"));
        progressBar_upgradeProgress->setValue(0);

        gridLayout_15->addWidget(progressBar_upgradeProgress, 1, 0, 1, 1);

        progressBar_upgradeProgressAll = new QProgressBar(groupBox_7);
        progressBar_upgradeProgressAll->setObjectName(QString::fromUtf8("progressBar_upgradeProgressAll"));
        progressBar_upgradeProgressAll->setValue(0);

        gridLayout_15->addWidget(progressBar_upgradeProgressAll, 2, 0, 1, 1);

        textBrowser_firmwareUpgradeLog = new QTextBrowser(groupBox_7);
        textBrowser_firmwareUpgradeLog->setObjectName(QString::fromUtf8("textBrowser_firmwareUpgradeLog"));

        gridLayout_15->addWidget(textBrowser_firmwareUpgradeLog, 0, 0, 1, 1);


        verticalLayout->addWidget(groupBox_7);


        gridLayout_19->addLayout(verticalLayout, 0, 1, 1, 1);

        verticalLayout_5 = new QVBoxLayout();
        verticalLayout_5->setObjectName(QString::fromUtf8("verticalLayout_5"));
        groupBox_16 = new QGroupBox(page3);
        groupBox_16->setObjectName(QString::fromUtf8("groupBox_16"));
        gridLayout_23 = new QGridLayout(groupBox_16);
        gridLayout_23->setObjectName(QString::fromUtf8("gridLayout_23"));
        horizontalLayout_6 = new QHBoxLayout();
        horizontalLayout_6->setObjectName(QString::fromUtf8("horizontalLayout_6"));
        label_100 = new QLabel(groupBox_16);
        label_100->setObjectName(QString::fromUtf8("label_100"));

        horizontalLayout_6->addWidget(label_100);

        lineEdit_firmwarePath = new QLineEdit(groupBox_16);
        lineEdit_firmwarePath->setObjectName(QString::fromUtf8("lineEdit_firmwarePath"));

        horizontalLayout_6->addWidget(lineEdit_firmwarePath);


        gridLayout_23->addLayout(horizontalLayout_6, 0, 0, 1, 1);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setObjectName(QString::fromUtf8("horizontalLayout_3"));
        chipInfo_recognize = new QPushButton(groupBox_16);
        chipInfo_recognize->setObjectName(QString::fromUtf8("chipInfo_recognize"));

        horizontalLayout_3->addWidget(chipInfo_recognize);

        horizontalSpacer_21 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_21);

        firmware_recognize = new QPushButton(groupBox_16);
        firmware_recognize->setObjectName(QString::fromUtf8("firmware_recognize"));

        horizontalLayout_3->addWidget(firmware_recognize);

        horizontalSpacer_22 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_3->addItem(horizontalSpacer_22);

        firmwareLoad = new QPushButton(groupBox_16);
        firmwareLoad->setObjectName(QString::fromUtf8("firmwareLoad"));

        horizontalLayout_3->addWidget(firmwareLoad);


        gridLayout_23->addLayout(horizontalLayout_3, 1, 0, 1, 1);

        groupBox_17 = new QGroupBox(groupBox_16);
        groupBox_17->setObjectName(QString::fromUtf8("groupBox_17"));
        gridLayout_22 = new QGridLayout(groupBox_17);
        gridLayout_22->setObjectName(QString::fromUtf8("gridLayout_22"));
        gridLayout_18 = new QGridLayout();
        gridLayout_18->setObjectName(QString::fromUtf8("gridLayout_18"));
        pushButton_startUpgrade = new QPushButton(groupBox_17);
        pushButton_startUpgrade->setObjectName(QString::fromUtf8("pushButton_startUpgrade"));

        gridLayout_18->addWidget(pushButton_startUpgrade, 0, 2, 1, 1);

        label_101 = new QLabel(groupBox_17);
        label_101->setObjectName(QString::fromUtf8("label_101"));

        gridLayout_18->addWidget(label_101, 0, 0, 1, 1);

        pushButton_startUpgradeAll = new QPushButton(groupBox_17);
        pushButton_startUpgradeAll->setObjectName(QString::fromUtf8("pushButton_startUpgradeAll"));

        gridLayout_18->addWidget(pushButton_startUpgradeAll, 0, 3, 1, 1);

        comboBox_upgradeMode = new QComboBox(groupBox_17);
        comboBox_upgradeMode->addItem(QString());
        comboBox_upgradeMode->addItem(QString());
        comboBox_upgradeMode->setObjectName(QString::fromUtf8("comboBox_upgradeMode"));

        gridLayout_18->addWidget(comboBox_upgradeMode, 0, 1, 1, 1);

        pushButton_stopUpgrade = new QPushButton(groupBox_17);
        pushButton_stopUpgrade->setObjectName(QString::fromUtf8("pushButton_stopUpgrade"));

        gridLayout_18->addWidget(pushButton_stopUpgrade, 0, 4, 1, 1);


        gridLayout_22->addLayout(gridLayout_18, 0, 0, 1, 2);

        gridLayout_17 = new QGridLayout();
        gridLayout_17->setObjectName(QString::fromUtf8("gridLayout_17"));
        lineEdit_6 = new QLineEdit(groupBox_17);
        lineEdit_6->setObjectName(QString::fromUtf8("lineEdit_6"));

        gridLayout_17->addWidget(lineEdit_6, 1, 3, 1, 1);

        label_106 = new QLabel(groupBox_17);
        label_106->setObjectName(QString::fromUtf8("label_106"));

        gridLayout_17->addWidget(label_106, 0, 0, 1, 1);

        label_107 = new QLabel(groupBox_17);
        label_107->setObjectName(QString::fromUtf8("label_107"));

        gridLayout_17->addWidget(label_107, 0, 2, 1, 1);

        lineEdit_4 = new QLineEdit(groupBox_17);
        lineEdit_4->setObjectName(QString::fromUtf8("lineEdit_4"));

        gridLayout_17->addWidget(lineEdit_4, 0, 3, 1, 1);

        lineEdit_5 = new QLineEdit(groupBox_17);
        lineEdit_5->setObjectName(QString::fromUtf8("lineEdit_5"));

        gridLayout_17->addWidget(lineEdit_5, 1, 1, 1, 1);

        label_109 = new QLabel(groupBox_17);
        label_109->setObjectName(QString::fromUtf8("label_109"));

        gridLayout_17->addWidget(label_109, 1, 2, 1, 1);

        label_108 = new QLabel(groupBox_17);
        label_108->setObjectName(QString::fromUtf8("label_108"));

        gridLayout_17->addWidget(label_108, 1, 0, 1, 1);

        lineEdit_shakeData = new QLineEdit(groupBox_17);
        lineEdit_shakeData->setObjectName(QString::fromUtf8("lineEdit_shakeData"));

        gridLayout_17->addWidget(lineEdit_shakeData, 0, 1, 1, 1);


        gridLayout_22->addLayout(gridLayout_17, 1, 0, 2, 2);

        label_105 = new QLabel(groupBox_17);
        label_105->setObjectName(QString::fromUtf8("label_105"));

        gridLayout_22->addWidget(label_105, 2, 1, 1, 1);


        gridLayout_23->addWidget(groupBox_17, 4, 0, 1, 1);

        gridLayout_20 = new QGridLayout();
        gridLayout_20->setObjectName(QString::fromUtf8("gridLayout_20"));
        groupBox_21 = new QGroupBox(groupBox_16);
        groupBox_21->setObjectName(QString::fromUtf8("groupBox_21"));
        gridLayout_21 = new QGridLayout(groupBox_21);
        gridLayout_21->setObjectName(QString::fromUtf8("gridLayout_21"));
        lineEdit_localDevNum = new QLineEdit(groupBox_21);
        lineEdit_localDevNum->setObjectName(QString::fromUtf8("lineEdit_localDevNum"));

        gridLayout_21->addWidget(lineEdit_localDevNum, 0, 1, 1, 1);

        lineEdit_localChipInfo = new QLineEdit(groupBox_21);
        lineEdit_localChipInfo->setObjectName(QString::fromUtf8("lineEdit_localChipInfo"));

        gridLayout_21->addWidget(lineEdit_localChipInfo, 1, 1, 1, 1);

        lineEdit_localAppVersion = new QLineEdit(groupBox_21);
        lineEdit_localAppVersion->setObjectName(QString::fromUtf8("lineEdit_localAppVersion"));

        gridLayout_21->addWidget(lineEdit_localAppVersion, 4, 1, 1, 1);

        lineEdit_localBoot2Version = new QLineEdit(groupBox_21);
        lineEdit_localBoot2Version->setObjectName(QString::fromUtf8("lineEdit_localBoot2Version"));

        gridLayout_21->addWidget(lineEdit_localBoot2Version, 3, 1, 1, 1);

        lineEdit_localromVersion = new QLineEdit(groupBox_21);
        lineEdit_localromVersion->setObjectName(QString::fromUtf8("lineEdit_localromVersion"));

        gridLayout_21->addWidget(lineEdit_localromVersion, 2, 1, 1, 1);

        label_112 = new QLabel(groupBox_21);
        label_112->setObjectName(QString::fromUtf8("label_112"));

        gridLayout_21->addWidget(label_112, 0, 0, 1, 1);

        label_113 = new QLabel(groupBox_21);
        label_113->setObjectName(QString::fromUtf8("label_113"));

        gridLayout_21->addWidget(label_113, 1, 0, 1, 1);

        label_114 = new QLabel(groupBox_21);
        label_114->setObjectName(QString::fromUtf8("label_114"));

        gridLayout_21->addWidget(label_114, 2, 0, 1, 1);

        label_115 = new QLabel(groupBox_21);
        label_115->setObjectName(QString::fromUtf8("label_115"));

        gridLayout_21->addWidget(label_115, 3, 0, 1, 1);

        label_116 = new QLabel(groupBox_21);
        label_116->setObjectName(QString::fromUtf8("label_116"));

        gridLayout_21->addWidget(label_116, 4, 0, 1, 1);


        gridLayout_20->addWidget(groupBox_21, 0, 0, 1, 1);

        groupBox_22 = new QGroupBox(groupBox_16);
        groupBox_22->setObjectName(QString::fromUtf8("groupBox_22"));
        gridLayout_25 = new QGridLayout(groupBox_22);
        gridLayout_25->setObjectName(QString::fromUtf8("gridLayout_25"));
        lineEdit_upgradeBinSize = new QLineEdit(groupBox_22);
        lineEdit_upgradeBinSize->setObjectName(QString::fromUtf8("lineEdit_upgradeBinSize"));

        gridLayout_25->addWidget(lineEdit_upgradeBinSize, 4, 1, 1, 1);

        lineEdit_upgradeAppVersion = new QLineEdit(groupBox_22);
        lineEdit_upgradeAppVersion->setObjectName(QString::fromUtf8("lineEdit_upgradeAppVersion"));

        gridLayout_25->addWidget(lineEdit_upgradeAppVersion, 3, 1, 1, 1);

        lineEdit_upgradeChipInfo = new QLineEdit(groupBox_22);
        lineEdit_upgradeChipInfo->setObjectName(QString::fromUtf8("lineEdit_upgradeChipInfo"));

        gridLayout_25->addWidget(lineEdit_upgradeChipInfo, 0, 1, 1, 1);

        lineEdit_upgradeBoot2Version = new QLineEdit(groupBox_22);
        lineEdit_upgradeBoot2Version->setObjectName(QString::fromUtf8("lineEdit_upgradeBoot2Version"));

        gridLayout_25->addWidget(lineEdit_upgradeBoot2Version, 2, 1, 1, 1);

        lineEdit_upgradeRomVersion = new QLineEdit(groupBox_22);
        lineEdit_upgradeRomVersion->setObjectName(QString::fromUtf8("lineEdit_upgradeRomVersion"));

        gridLayout_25->addWidget(lineEdit_upgradeRomVersion, 1, 1, 1, 1);

        label_99 = new QLabel(groupBox_22);
        label_99->setObjectName(QString::fromUtf8("label_99"));

        gridLayout_25->addWidget(label_99, 0, 0, 1, 1);

        label_102 = new QLabel(groupBox_22);
        label_102->setObjectName(QString::fromUtf8("label_102"));

        gridLayout_25->addWidget(label_102, 1, 0, 1, 1);

        label_103 = new QLabel(groupBox_22);
        label_103->setObjectName(QString::fromUtf8("label_103"));

        gridLayout_25->addWidget(label_103, 2, 0, 1, 1);

        label_104 = new QLabel(groupBox_22);
        label_104->setObjectName(QString::fromUtf8("label_104"));

        gridLayout_25->addWidget(label_104, 3, 0, 1, 1);

        label_111 = new QLabel(groupBox_22);
        label_111->setObjectName(QString::fromUtf8("label_111"));

        gridLayout_25->addWidget(label_111, 4, 0, 1, 1);


        gridLayout_20->addWidget(groupBox_22, 0, 1, 1, 1);


        gridLayout_23->addLayout(gridLayout_20, 2, 0, 2, 1);


        verticalLayout_5->addWidget(groupBox_16);


        gridLayout_19->addLayout(verticalLayout_5, 0, 0, 1, 1);

        stackedWidget->addWidget(page3);

        gridLayout_24->addWidget(stackedWidget, 0, 0, 1, 1);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 1019, 23));
        menu_T = new QMenu(menubar);
        menu_T->setObjectName(QString::fromUtf8("menu_T"));
        menu_H = new QMenu(menubar);
        menu_H->setObjectName(QString::fromUtf8("menu_H"));
        menu_R = new QMenu(menubar);
        menu_R->setObjectName(QString::fromUtf8("menu_R"));
        menu_F = new QMenu(menubar);
        menu_F->setObjectName(QString::fromUtf8("menu_F"));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);
        toolBar = new QToolBar(MainWindow);
        toolBar->setObjectName(QString::fromUtf8("toolBar"));
        toolBar->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
        MainWindow->addToolBar(Qt::TopToolBarArea, toolBar);

        menubar->addAction(menu_F->menuAction());
        menubar->addAction(menu_T->menuAction());
        menubar->addAction(menu_R->menuAction());
        menubar->addAction(menu_H->menuAction());
        menu_T->addAction(actionc);
        menu_T->addAction(actionce);
        menu_T->addAction(sys_error_configer);
        menu_H->addAction(actionHelp_Guid);
        menu_H->addAction(actionsoft_Version);
        menu_R->addAction(actionstart);
        menu_R->addAction(actionpause);
        menu_R->addAction(actionstop);
        toolBar->addAction(test_config);
        toolBar->addAction(test_manager);
        toolBar->addAction(dfu_setting);

        retranslateUi(MainWindow);

        stackedWidget->setCurrentIndex(0);
        UartBoartComboBox->setCurrentIndex(0);
        runUartBaudRateComboBox->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "HTOL_Test_Tool", nullptr));
#if QT_CONFIG(tooltip)
        MainWindow->setToolTip(QString());
#endif // QT_CONFIG(tooltip)
        actionstart->setText(QCoreApplication::translate("MainWindow", "\345\274\200\345\247\213(S)", nullptr));
        actionstop->setText(QCoreApplication::translate("MainWindow", "\345\201\234\346\255\242(S)", nullptr));
        actionsoft_Version->setText(QCoreApplication::translate("MainWindow", "\345\205\263\344\272\216\350\275\257\344\273\266(V)", nullptr));
        actionHelp_Guid->setText(QCoreApplication::translate("MainWindow", "\345\274\200\345\247\213\344\275\277\347\224\250(G) ", nullptr));
        actionpause->setText(QCoreApplication::translate("MainWindow", "\346\232\202\345\201\234(P)", nullptr));
        test_config->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\346\250\241\345\235\227\351\205\215\347\275\256", nullptr));
        test_manager->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\350\277\220\350\241\214\347\256\241\347\220\206", nullptr));
        actionc->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\351\241\271\351\205\215\347\275\256", nullptr));
#if QT_CONFIG(tooltip)
        actionc->setToolTip(QCoreApplication::translate("MainWindow", "test_case_cofiger", nullptr));
#endif // QT_CONFIG(tooltip)
        actionce->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\345\274\202\345\270\270\351\205\215\347\275\256", nullptr));
#if QT_CONFIG(tooltip)
        actionce->setToolTip(QCoreApplication::translate("MainWindow", "teet_error_configure", nullptr));
#endif // QT_CONFIG(tooltip)
        sys_error_configer->setText(QCoreApplication::translate("MainWindow", "\347\263\273\347\273\237\345\274\202\345\270\270\351\205\215\347\275\256", nullptr));
        dfu_setting->setText(QCoreApplication::translate("MainWindow", "\350\256\276\345\244\207\345\233\272\344\273\266\345\215\207\347\272\247\351\205\215\347\275\256", nullptr));
#if QT_CONFIG(tooltip)
        dfu_setting->setToolTip(QCoreApplication::translate("MainWindow", "\350\256\276\345\244\207\345\233\272\344\273\266\345\215\207\347\272\247\350\256\276\347\275\256", nullptr));
#endif // QT_CONFIG(tooltip)
        groupBox_2->setTitle(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\351\200\232\344\277\241\351\205\215\347\275\256", nullptr));
        UartBoartComboBox->setItemText(0, QCoreApplication::translate("MainWindow", "921600", nullptr));
        UartBoartComboBox->setItemText(1, QCoreApplication::translate("MainWindow", "9600", nullptr));
        UartBoartComboBox->setItemText(2, QCoreApplication::translate("MainWindow", "115200", nullptr));
        UartBoartComboBox->setItemText(3, QCoreApplication::translate("MainWindow", "256000", nullptr));

        UartBoartComboBox->setCurrentText(QCoreApplication::translate("MainWindow", "921600", nullptr));
        configerUartToolButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        toolButton_Write_Addr->setText(QCoreApplication::translate("MainWindow", "\345\206\231\345\205\245", nullptr));
        label_8->setText(QCoreApplication::translate("MainWindow", "\346\263\242\347\211\271\347\216\207\357\274\232", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "\344\270\262\345\217\243\345\217\267\357\274\232", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "\346\250\241\345\235\227ID\357\274\232", nullptr));
        groupBox_4->setTitle(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\344\277\241\346\201\257\351\205\215\347\275\256", nullptr));
        radioButtonTrxTest->setText(QCoreApplication::translate("MainWindow", "TRX_TEST", nullptr));
        radioButtonFlashTest->setText(QCoreApplication::translate("MainWindow", "FLASH_TEST", nullptr));
        radioButtonCanTest->setText(QCoreApplication::translate("MainWindow", "CAN_TEST", nullptr));
        label_9->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\345\274\202\345\270\270\345\244\204\347\220\206", nullptr));
        radioButtonRfTxTest->setText(QCoreApplication::translate("MainWindow", "RF_TX_TEST", nullptr));
        pushButton_TestInfoWrite->setText(QCoreApplication::translate("MainWindow", "\345\206\231\345\205\245", nullptr));
        label_10->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\346\250\241\345\235\227ID", nullptr));
        radioButtonI2cTest->setText(QCoreApplication::translate("MainWindow", "I2C_TEST", nullptr));
        radioButtonGpioTest->setText(QCoreApplication::translate("MainWindow", "GPIO_TEST", nullptr));
        radioButton_AllTest->setText(QCoreApplication::translate("MainWindow", "ALL_TEST", nullptr));
        radioButtonRfRxTest->setText(QCoreApplication::translate("MainWindow", "RF_RX_TEST", nullptr));
        label_120->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\351\241\271\351\205\215\347\275\256", nullptr));
        radioButtonSpiTest->setText(QCoreApplication::translate("MainWindow", "SPI_TEST", nullptr));
        checkBox_AllID->setText(QCoreApplication::translate("MainWindow", "ALL_ID", nullptr));
        comboBox_TestExceptionHandle->setItemText(0, QCoreApplication::translate("MainWindow", "\351\207\215\345\220\257\345\275\223\345\211\215\346\265\213\350\257\225\351\241\271\345\271\266\346\265\213\350\257\225\350\255\246\345\221\212", nullptr));
        comboBox_TestExceptionHandle->setItemText(1, QCoreApplication::translate("MainWindow", "\345\274\200\345\220\257\344\270\213\344\270\252\346\265\213\350\257\225\351\241\271\345\271\266\346\265\213\350\257\225\350\255\246\345\221\212", nullptr));
        comboBox_TestExceptionHandle->setItemText(2, QCoreApplication::translate("MainWindow", "\351\207\215\345\220\257\345\275\223\345\211\215\346\250\241\345\235\227\346\265\213\350\257\225\345\271\266\346\265\213\350\257\225\350\255\246\345\221\212", nullptr));
        comboBox_TestExceptionHandle->setItemText(3, QCoreApplication::translate("MainWindow", "\345\274\200\345\220\257\344\270\213\344\270\252\346\250\241\345\235\227\346\265\213\350\257\225\345\271\266\346\265\213\350\257\225\350\255\246\345\221\212", nullptr));

        groupBox_5->setTitle(QCoreApplication::translate("MainWindow", "\346\225\260\346\215\256\344\277\235\345\255\230\351\205\215\347\275\256", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "\346\225\260\346\215\256\344\277\235\345\255\230\350\267\257\345\276\204", nullptr));
        pushButton_DataSavePathBrowse->setText(QCoreApplication::translate("MainWindow", "\346\265\217\350\247\210", nullptr));
        groupBox_12->setTitle(QCoreApplication::translate("MainWindow", "\347\263\273\347\273\237\347\256\241\347\220\206\351\205\215\347\275\256", nullptr));
        comboBox_SystemExceptionHandle->setItemText(0, QCoreApplication::translate("MainWindow", "\347\263\273\347\273\237\350\255\246\345\221\212\345\271\266\351\207\215\345\220\257\346\265\213\350\257\225", nullptr));
        comboBox_SystemExceptionHandle->setItemText(1, QCoreApplication::translate("MainWindow", "\351\207\215\345\220\257\346\265\213\350\257\225", nullptr));
        comboBox_SystemExceptionHandle->setItemText(2, QCoreApplication::translate("MainWindow", "\347\263\273\347\273\237\350\255\246\345\221\212", nullptr));

        label_12->setText(QCoreApplication::translate("MainWindow", "\347\263\273\347\273\237\345\274\202\345\270\270\345\244\204\347\220\206", nullptr));
        pushButton_SystemExcepWrite->setText(QCoreApplication::translate("MainWindow", "\345\206\231\345\205\245", nullptr));
        label_13->setText(QCoreApplication::translate("MainWindow", "\351\205\215\347\275\256\346\226\207\344\273\266\350\267\257\345\276\204", nullptr));
        pushButton_SaveCfgFile->setText(QCoreApplication::translate("MainWindow", "\344\277\235\345\255\230\351\205\215\347\275\256\346\226\207\344\273\266", nullptr));
        groupBox_3->setTitle(QCoreApplication::translate("MainWindow", "DCXO\346\240\241\345\207\206", nullptr));
        FreqSpecButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        FreqSpecAddrLineEdit->setText(QCoreApplication::translate("MainWindow", "192.168.190.106", nullptr));
        label_98->setText(QCoreApplication::translate("MainWindow", "\351\242\221\350\260\261\344\273\252\345\210\206\346\236\220\344\273\252\357\274\232", nullptr));
        FreqCalibrateButton->setText(QCoreApplication::translate("MainWindow", "\345\274\200\345\247\213\346\240\241\345\207\206", nullptr));
        FreqSpecPortlineEdit->setText(QCoreApplication::translate("MainWindow", "5025", nullptr));
        groupBox->setTitle(QCoreApplication::translate("MainWindow", "\346\212\245\350\255\246\351\202\256\347\256\261\351\205\215\347\275\256", nullptr));
        label_95->setText(QCoreApplication::translate("MainWindow", "\345\217\221\351\200\201\351\202\256\347\256\261", nullptr));
        label_97->setText(QCoreApplication::translate("MainWindow", "\345\217\221\351\200\201\345\257\206\347\240\201", nullptr));
        label_96->setText(QCoreApplication::translate("MainWindow", "\346\216\245\346\224\266\351\202\256\347\256\261", nullptr));
        groupBox_6->setTitle(QCoreApplication::translate("MainWindow", "\346\250\241\345\235\227\350\260\203\350\257\225Log", nullptr));
        groupBox_11->setTitle(QCoreApplication::translate("MainWindow", "\346\250\241\345\235\227\346\265\213\350\257\225\347\212\266\346\200\201", nullptr));
        label_73->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_68->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_37->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_58->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_45->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_35->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_81->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_76->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_17->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_50->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_46->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_78->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_16->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_74->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_85->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_60->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_20->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_59->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_49->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_54->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_55->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_84->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_27->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_38->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_19->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_47->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_44->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_69->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_31->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_86->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_23->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_24->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_18->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_40->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_34->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_48->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_83->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_52->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_51->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_82->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_29->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_75->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_22->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_32->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_77->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_53->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_63->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_65->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_62->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_66->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_64->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_57->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_28->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_72->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_61->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_25->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_15->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_71->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_67->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_43->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_79->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_41->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_42->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_56->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_70->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_21->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_26->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_39->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_30->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_33->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_36->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_87->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_88->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_89->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_90->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_91->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_92->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_93->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_94->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_80->setText(QCoreApplication::translate("MainWindow", "TextLabel", nullptr));
        label_110->setText(QCoreApplication::translate("MainWindow", "\345\272\225\346\235\277\345\217\263\344\270\213\350\247\222", nullptr));
        groupBox_8->setTitle(QCoreApplication::translate("MainWindow", "\346\250\241\345\235\227\346\216\247\345\210\266", nullptr));
        label_14->setText(QCoreApplication::translate("MainWindow", "\346\263\242\347\211\271\347\216\207\357\274\232", nullptr));
        runUartBaudRateComboBox->setItemText(0, QCoreApplication::translate("MainWindow", "9600", nullptr));
        runUartBaudRateComboBox->setItemText(1, QCoreApplication::translate("MainWindow", "115200", nullptr));
        runUartBaudRateComboBox->setItemText(2, QCoreApplication::translate("MainWindow", "256000", nullptr));
        runUartBaudRateComboBox->setItemText(3, QCoreApplication::translate("MainWindow", "921600", nullptr));

        label_11->setText(QCoreApplication::translate("MainWindow", "\344\270\262\345\217\243\345\217\267\357\274\232", nullptr));
        runUarttoolButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        groupBox_10->setTitle(QCoreApplication::translate("MainWindow", "\344\273\252\345\231\250\346\216\247\345\210\266", nullptr));
        digtaVoltagePortlineEdit->setText(QCoreApplication::translate("MainWindow", "4196", nullptr));
        digtalPowerToolButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        digtaVoltagelineEdit->setText(QCoreApplication::translate("MainWindow", "192.160.2451.10", nullptr));
        digtalPowerPortlineEdit->setText(QCoreApplication::translate("MainWindow", "5025", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "\346\225\260\345\255\227\347\224\265\346\265\201\357\274\232", nullptr));
        digtalPowerLineEdit->setText(QCoreApplication::translate("MainWindow", "169.254.154.223", nullptr));
        label_7->setText(QCoreApplication::translate("MainWindow", "\346\225\260\345\255\227\347\224\265\345\216\213\357\274\232", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "\346\225\260\345\255\227\347\224\265\346\272\220\357\274\232", nullptr));
        digtaVoltageToolButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        digtaElectricityPortlineEdit->setText(QCoreApplication::translate("MainWindow", "5025", nullptr));
        digtaElectricityToolButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        digtaElectricityllineEdit->setText(QCoreApplication::translate("MainWindow", "192.168.100.20", nullptr));
        groupBox_9->setTitle(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\346\216\247\345\210\266", nullptr));
        scripTestRadioButton->setText(QCoreApplication::translate("MainWindow", "\350\204\232\346\234\254\346\265\213\350\257\225", nullptr));
        scriptToolButton->setText(QCoreApplication::translate("MainWindow", "\350\277\236\346\216\245", nullptr));
        scriptPortlineEdit->setText(QCoreApplication::translate("MainWindow", "4196", nullptr));
        autoTestToolButton->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\345\274\200\345\247\213", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\347\275\221\345\217\243", nullptr));
        autoTestRadioButton->setText(QCoreApplication::translate("MainWindow", "\350\207\252\345\212\250\346\265\213\350\257\225", nullptr));
        scriptTestToolButton->setText(QCoreApplication::translate("MainWindow", "\346\265\213\350\257\225\345\274\200\345\247\213", nullptr));
        ScriptSelectToolButton->setText(QCoreApplication::translate("MainWindow", "\351\200\211\346\213\251\350\204\232\346\234\254", nullptr));
        groupBox_7->setTitle(QCoreApplication::translate("MainWindow", "\345\215\207\347\272\247\344\277\241\346\201\257\350\256\260\345\275\225", nullptr));
        groupBox_16->setTitle(QCoreApplication::translate("MainWindow", "\345\215\207\347\272\247\345\233\272\344\273\266\347\256\241\347\220\206", nullptr));
        label_100->setText(QCoreApplication::translate("MainWindow", "\345\233\272\344\273\266\350\267\257\345\276\204", nullptr));
        chipInfo_recognize->setText(QCoreApplication::translate("MainWindow", "\350\212\257\347\211\207\350\257\206\345\210\253", nullptr));
        firmware_recognize->setText(QCoreApplication::translate("MainWindow", "\345\233\272\344\273\266\350\257\206\345\210\253", nullptr));
        firmwareLoad->setText(QCoreApplication::translate("MainWindow", "\345\233\272\344\273\266\345\212\240\350\275\275", nullptr));
        groupBox_17->setTitle(QCoreApplication::translate("MainWindow", "\345\215\207\347\272\247\346\226\271\345\274\217\347\256\241\347\220\206", nullptr));
        pushButton_startUpgrade->setText(QCoreApplication::translate("MainWindow", "\345\274\200\345\247\213\345\215\207\347\272\247", nullptr));
        label_101->setText(QCoreApplication::translate("MainWindow", "\345\215\207\347\272\247\346\226\271\345\274\217\357\274\232", nullptr));
        pushButton_startUpgradeAll->setText(QCoreApplication::translate("MainWindow", "\345\205\250\351\203\250\345\215\207\347\272\247", nullptr));
        comboBox_upgradeMode->setItemText(0, QCoreApplication::translate("MainWindow", "\346\225\260\346\215\256\345\215\217\350\256\256\345\215\207\347\272\247", nullptr));
        comboBox_upgradeMode->setItemText(1, QCoreApplication::translate("MainWindow", "AT\346\214\207\344\273\244\345\215\207\347\272\247", nullptr));

        pushButton_stopUpgrade->setText(QCoreApplication::translate("MainWindow", "\345\201\234\346\255\242\345\215\207\347\272\247", nullptr));
        lineEdit_6->setText(QString());
        label_106->setText(QCoreApplication::translate("MainWindow", "\346\217\241\346\211\213\346\225\260\346\215\256\346\265\201", nullptr));
        label_107->setText(QCoreApplication::translate("MainWindow", "FLASH\345\234\260\345\235\200", nullptr));
        label_109->setText(QCoreApplication::translate("MainWindow", "FLASH\345\244\247\345\260\217", nullptr));
        label_108->setText(QCoreApplication::translate("MainWindow", "\345\212\240\345\257\206\345\257\206\351\222\245\345\200\274", nullptr));
        label_105->setText(QString());
        groupBox_21->setTitle(QCoreApplication::translate("MainWindow", "\346\234\254\345\234\260\345\233\272\344\273\266\344\277\241\346\201\257", nullptr));
        label_112->setText(QCoreApplication::translate("MainWindow", "\350\256\276\345\244\207\347\274\226\345\217\267", nullptr));
        label_113->setText(QCoreApplication::translate("MainWindow", "\350\212\257\347\211\207\344\277\241\346\201\257", nullptr));
        label_114->setText(QCoreApplication::translate("MainWindow", "ROM \347\211\210\346\234\254", nullptr));
        label_115->setText(QCoreApplication::translate("MainWindow", "BOOT2\347\211\210\346\234\254", nullptr));
        label_116->setText(QCoreApplication::translate("MainWindow", "APP\347\211\210\346\234\254", nullptr));
        groupBox_22->setTitle(QCoreApplication::translate("MainWindow", "\345\215\207\347\272\247\345\233\272\344\273\266\344\277\241\346\201\257", nullptr));
        label_99->setText(QCoreApplication::translate("MainWindow", "\350\212\257\347\211\207\344\277\241\346\201\257", nullptr));
        label_102->setText(QCoreApplication::translate("MainWindow", "ROM\347\211\210\346\234\254", nullptr));
        label_103->setText(QCoreApplication::translate("MainWindow", "BOOT2\347\211\210\346\234\254", nullptr));
        label_104->setText(QCoreApplication::translate("MainWindow", "APP\347\211\210\346\234\254", nullptr));
        label_111->setText(QCoreApplication::translate("MainWindow", "BINSIZE", nullptr));
        menu_T->setTitle(QCoreApplication::translate("MainWindow", "\351\205\215\347\275\256(C)", nullptr));
        menu_H->setTitle(QCoreApplication::translate("MainWindow", "\345\270\256\345\212\251(H)", nullptr));
        menu_R->setTitle(QCoreApplication::translate("MainWindow", "\350\277\220\350\241\214(R)", nullptr));
        menu_F->setTitle(QCoreApplication::translate("MainWindow", "\346\226\207\344\273\266(F)", nullptr));
        toolBar->setWindowTitle(QCoreApplication::translate("MainWindow", "toolBar", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
