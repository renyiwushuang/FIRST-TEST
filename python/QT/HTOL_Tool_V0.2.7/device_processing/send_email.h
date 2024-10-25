#ifndef SEND_EMAIL_H
#define SEND_EMAIL_H

#include <QObject>
#include <QtCore>
#include <QCoreApplication>
#include <QObject>

#include <QTcpSocket>
#include <QString>
#include <QTextStream>
#include <QDebug>
#include <QAbstractSocket>
#include <QDateTime>
#include <QDate>
#include <QLocale>
#include <QObject>
#include <QTcpSocket>


class CSendEmailDevice : public QObject
{
    Q_OBJECT
public:

    CSendEmailDevice(QString smtp_host, QString smtp_user_name, QString smtp_pass);
    ~CSendEmailDevice();

    bool send( const QString &to,const QString &subject, const QString &body );
    bool readLiner();

    QString timeStampMail();
    void errorCloseAll();

    int m_line_send;
    QStringList m_error_MSG;

public slots:
    bool slot_putSendLine();

signals:
    void signal_status( const QString &);
    void signal_sendLine();

private:

    QString sendLineAndGrab(QString send_data);
    QString encodeBase64( QString xml );
    QString decodeBase64( QString xml );
    int dateSwap(QString form, uint unixtime );

    bool m_isconnect;
    QString m_smtp_host;
    QString m_smtp_user_name;
    QString m_smtp_pass;
    QString m_message;
    QString m_output;
    QString m_remote_server_name;
    QString m_mail_status;
    QTextStream *m_socket_text_stream;  //在socket与QTextStream关联，用于数据接收
    QTcpSocket *m_smtp_socket;
    QString m_from;
    QString m_rcpt;
    QString m_response;
    int m_timeout;
};

#endif // SEND_EMAIL_DEVICE_H
