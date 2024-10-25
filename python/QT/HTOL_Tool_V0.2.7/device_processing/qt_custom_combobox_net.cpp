#include "qt_custom_combobox_net.h"

#include <QHostInfo>
#include <QNetworkInterface>
#include <QNetworkAddressEntry>
#include <QInputDialog>
#include <QLineEdit>
#include <QDebug>
#include <QMouseEvent>

Qt_custom_combobox_net::Qt_custom_combobox_net(QWidget *parent,bool askoccupy) :
    QComboBox(parent),mAskOccupy(askoccupy)
{
}

Qt_custom_combobox_net::~Qt_custom_combobox_net()
{
}

QString get_text = NULL;
uint8_t text_close = 0;

/*******************************************************************************
 * 1、show pop up.
 *******************************************************************************/
void Qt_custom_combobox_net::showPopup()
{
    QString current_text = this->currentText();
    QStringList namelist;
    namelist.clear();
    QComboBox::clear();

    namelist.append("127.0.0.1");
    QHostInfo info = QHostInfo::fromName(QHostInfo::localHostName());
    for (int i = 0;i < info.addresses().size();i++)
    {
        if(info.addresses()[i].toString().contains("192.168")){
            namelist.append(info.addresses()[i].toString());
        }
        if(info.addresses()[i].toString().contains("169.254")){
            namelist.append(info.addresses()[i].toString());
        }
    }
    namelist.append("Custom");

    QComboBox::addItems(namelist);
    setCurrentText(current_text);
    QComboBox::showPopup();
}

/*******************************************************************************
 * 2、set ask occupy.
 *******************************************************************************/
void Qt_custom_combobox_net::setAskOccupy(const bool &flag)
{
    mAskOccupy = flag;
}

