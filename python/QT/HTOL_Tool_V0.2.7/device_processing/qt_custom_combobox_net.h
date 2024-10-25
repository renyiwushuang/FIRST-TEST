#ifndef QT_CUSTOMCOMBOBOX_NET_H
#define QT_CUSTOMCOMBOBOX_NET_H

#include <QComboBox>

class Qt_custom_combobox_net : public QComboBox
{
    Q_OBJECT

public:
    explicit Qt_custom_combobox_net(QWidget *parent = nullptr,bool askoccupy=0);
    ~Qt_custom_combobox_net()override;

    void showPopup()override;
    void setAskOccupy(const bool &flag);
    QLineEdit *txtIP1;

private:
    bool mAskOccupy;
};

#endif // QT_CUSTOMCOMBOBOX_NET_H
