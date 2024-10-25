#ifndef QT_CUSTOM_COMBOBOX_UART_H
#define QT_CUSTOM_COMBOBOX_UART_H

#include <QComboBox>

class Qt_custom_combobox_uart : public QComboBox
{
    Q_OBJECT
public:
    Qt_custom_combobox_uart(QWidget *parent = nullptr,bool askoccupy=0);
    ~Qt_custom_combobox_uart()override;

    void showPopup()override;
    void setAskOccupy(const bool &flag);

private:
    bool mAskOccupy;
};

#endif // QT_CUSTOM_COMBOBOX_UART_H
