#include "qt_custom_combobox_uart.h"
#include <QtSerialPort/QSerialPortInfo>
#include <QtSerialPort/QSerialPort>
#include <QMouseEvent>

Qt_custom_combobox_uart::Qt_custom_combobox_uart(QWidget *parent,bool askoccupy):
    QComboBox(parent),mAskOccupy(askoccupy)
{}

Qt_custom_combobox_uart::~Qt_custom_combobox_uart()
{}

/*******************************************************************************
 * 1、show pop up.
 *******************************************************************************/
void Qt_custom_combobox_uart::showPopup()
{
    QString current_text = this->currentText();
    QStringList namelist;
    namelist.clear();
    QComboBox::clear();
    foreach(const QSerialPortInfo &info, QSerialPortInfo::availablePorts())
    {
        QSerialPort serial;
        serial.setPort(info);
        if(mAskOccupy){
            if(serial.open(QIODevice::ReadWrite))           //遍历可打开串口
            {
                namelist.append(serial.portName());
                serial.close();
            }
            else{
                if(serial.portName()==current_text){        //当前串口如果打开也要添加
                    namelist.append(serial.portName());
                }
            }
        }
        else{                                               //遍历添加所有串口
            namelist.append(serial.portName());

        }
    }
    QComboBox::addItems(namelist);
    setCurrentText(current_text);
    QComboBox::showPopup();
}
