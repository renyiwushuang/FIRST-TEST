#include "send_email.h"

CSendEmailDevice::CSendEmailDevice(QString smtp_host, QString smtp_user_name, QString smtp_pass)
{
    this->m_smtp_host = smtp_host;
    this->m_smtp_user_name = smtp_user_name;
    this->m_smtp_pass = smtp_pass;
}

CSendEmailDevice::~CSendEmailDevice()
{
    delete m_smtp_socket;
    delete m_socket_text_stream;
}

/* SENDER AND RECIVER  */
QString CSendEmailDevice::sendLineAndGrab(QString senddata)
{
    QString incommingData = "";

    if (m_isconnect)
    {
        //int current = m_line_send;
        int loops = 0;

        *m_socket_text_stream << senddata << "\r\n";
        m_socket_text_stream->flush();
        if (senddata != "QUIT") {
            if (m_smtp_socket->waitForReadyRead(m_timeout))
            {
                while (!m_socket_text_stream->atEnd())
                {
                    loops++;
                    QString opera = m_socket_text_stream->readLine()+"\n";
                    incommingData = opera + incommingData;
                }
            }
        } else
        {
            delete m_smtp_socket;
            delete m_socket_text_stream;
            m_isconnect = false;
            return incommingData;
        }
    }
    else
    {
         errorCloseAll();
    }
    return incommingData;
}

QString CSendEmailDevice::encodeBase64( QString xml )
{
    QByteArray text;
    text.append(xml);
    return text.toBase64();
}

QString CSendEmailDevice::decodeBase64( QString xml )
{
    QByteArray xcode("");;
    xcode.append(xml);
    QByteArray precode(QByteArray::fromBase64(xcode));
    QString notetxt = precode.data();
    return notetxt;
}

int CSendEmailDevice::dateSwap(QString form, uint unixtime )
{
    QDateTime fromunix;
    fromunix.setTime_t(unixtime);
    QString numeric = fromunix.toString((const QString)form);
    bool ok;
    return (int)numeric.toFloat(&ok);
}

QString CSendEmailDevice::timeStampMail()
{
    /* mail rtf Date format! http://www.faqs.org/rfcs/rfc788.html */
    QDateTime timer1( QDateTime::currentDateTime() );

    uint unixtime = timer1.toTime_t();
    QDateTime fromunix;
    fromunix.setTime_t(unixtime);


    QStringList RTFdays = QStringList() << "giorno_NULL" << "Mon" << "Tue" << "Wed" << "Thu" << "Fri" << "Sat" << "Sun";
    QStringList RTFmonth = QStringList() << "mese_NULL" << "Jan" << "Feb" << "Mar" << "Apr" << "May" << "Jun" << "Jul" << "Aug" << "Sep" << "Oct" << "Nov" << "Dec";
    QDate timeroad(dateSwap("yyyy",unixtime),dateSwap("M",unixtime),dateSwap("d",unixtime));

    QStringList rtfd_line;
    //rtfd_line.clear();
    rtfd_line.append("Date: ");
    rtfd_line.append(RTFdays.at(timeroad.dayOfWeek()));
    rtfd_line.append(", ");
    rtfd_line.append(QString::number(dateSwap("d",unixtime)));
    rtfd_line.append(" ");
    rtfd_line.append(RTFmonth.at(dateSwap("M",unixtime)));
    rtfd_line.append(" ");
    rtfd_line.append(QString::number(dateSwap("yyyy",unixtime)));
    rtfd_line.append(" ");
    rtfd_line.append(fromunix.toString("hh:mm:ss"));
    //rtfd_line.append(" +0100");
    return QString(rtfd_line.join(""));
}

void CSendEmailDevice::errorCloseAll()
{
    delete m_socket_text_stream;
    m_smtp_socket->close();
}

bool CSendEmailDevice::send(  const QString &to, const QString &subject, const QString &body )
{
    //qDebug()<<"####"<<Q_FUNC_INFO;
    bool res = false;
    int waittime = 5 * 1000;
    this->m_from = m_smtp_user_name;
    m_rcpt = to;
    m_error_MSG.clear();
    m_timeout = waittime;
    m_line_send = 0;
    m_isconnect = false;


    QString tmp = "=?utf-8?B?"+ QByteArray().append(subject).toBase64()+"?=";
    m_message.append("Subject:" + tmp + "\n");
    m_message.append("To: " + to + "\n");
    m_message.append("From: "+m_smtp_user_name+" <" + m_smtp_user_name + ">\n");

    m_message.append("Content-Type: text/html; charset=UTF8;\n");   /* or txt */
    m_message.append("Content-transfer-encoding: 7BIT\n\n\n\n");
    m_message.append(body);
    m_message.replace( tr( "\n" ), tr( "\r\n" ) );
    m_message.replace( tr( "\r\n.\r\n" ),tr( "\r\n..\r\n" ) );

    m_smtp_socket = new QTcpSocket(this);
    connect( this, SIGNAL(signal_sendLine()), this ,SLOT(slot_putSendLine()));

    if (m_smtp_host.size() > 0)
    {
        m_smtp_socket->connectToHost(m_smtp_host,25);
    } else {
        m_smtp_socket->connectToHost("localhost",25);
    }
    if (m_smtp_socket->waitForConnected(m_timeout))
    {
        if (m_smtp_socket->waitForReadyRead(m_timeout))
        {
            m_isconnect = true;
            return  readLiner();
        }
    }
    else
    {
         errorCloseAll();
    }
   return res;
}

bool  CSendEmailDevice::readLiner()
{
    bool res = false;
    if (m_isconnect)
    {
        QTextCodec *codecx;
        codecx = QTextCodec::codecForMib(106);
        m_socket_text_stream = new QTextStream( m_smtp_socket );
        m_socket_text_stream->setCodec(codecx);

        int loops = 0;
        while (!m_socket_text_stream->atEnd())
        {
            loops++;
            m_response = m_socket_text_stream->readLine();
        }
        if (m_response.size() > 0)
        {
            m_remote_server_name = m_response;
            m_mail_status = m_response.left(3);
            if (m_mail_status == "220")
            {
                m_response="";
                m_line_send = 1;
                res = true;
            }
        }
        else
        {
            errorCloseAll();
        }
    }
    return res;
}

/* LINE SENDER  */
bool CSendEmailDevice::slot_putSendLine()
{
    static bool res = true;
    int current = m_line_send;
    QString temp_m_smtp_user_name = "<" + m_smtp_user_name + ">";
    QString temp_m_rcpt = "<" + m_rcpt + ">";
    switch(current)
    {
        case 1:
            m_response = sendLineAndGrab("ehlo localhost");
            //qDebug() << "ehlo localhost回复：" <<  m_response << "\r\n";
            if(m_response.size() > 0){

                if(m_response.contains("250", Qt::CaseInsensitive)){
                    m_line_send = 2;
                    emit signal_sendLine();
                }else{
                    m_error_MSG.append(m_response);
                    res=false;
                }
            } else{
                res=false;
            }
            m_response ="";
            break;

        case 2:
            m_response = sendLineAndGrab("AUTH LOGIN");
            //qDebug() << "AUTH LOGIN回复：" <<  m_response << "\r\n";
            if(m_response.size() > 0){
                if(m_response.contains("334", Qt::CaseInsensitive)){
                    m_line_send = 3;
                    emit signal_sendLine();
                } else{
                    m_error_MSG.append(m_response);
                    res= false;
                }
            } else{
                res= false;
            }
            m_response ="";
            break;

        case 3:
            m_response = sendLineAndGrab(encodeBase64(m_smtp_user_name));   /* username send */
            //qDebug() << "m_smtp_user_name 回复：" <<  m_response << "\r\n";
            if(m_response.size() > 0) {
                if(m_response.contains("334", Qt::CaseInsensitive)){
                    m_line_send = 4;
                    emit signal_sendLine();
                } else{
                    m_error_MSG.append(m_response);
                    res= false;
                }
            } else{
                res=false;
            }
            m_response ="";
            break;

        case 4:
            m_response = sendLineAndGrab(encodeBase64(m_smtp_pass));     /* pass send */
            //qDebug() << "m_smtp_pass 回复：" <<  m_response << "\r\n";
            if (m_response.size() > 0){
                if (m_response.contains("235", Qt::CaseInsensitive)){
                    m_line_send = 5;
                    emit signal_sendLine();
                } else{
                    m_error_MSG.append(m_response);
                    res= false;
                }
            } else{
                res= false;
            }
            m_response ="";
            break;

        case 5:
            m_response = sendLineAndGrab(tr("MAIL FROM: %1").arg(temp_m_smtp_user_name));
            //qDebug() << "MAIL FROM m_smtp_user_name回复：" <<  m_response << "\r\n";
            if (m_response.size() > 0){
                if(m_response.contains("ok", Qt::CaseInsensitive)){
                    m_line_send = 6;
                    emit signal_sendLine();
                } else{
                    m_error_MSG.append(m_response);
                    res= false;
                }
            } else{
                res= false;
            }
            m_response ="";
            break;

        case 6:
            m_response = sendLineAndGrab("RCPT TO: "+temp_m_rcpt);
            //qDebug() << "RCPT TO m_rcpt回复：" <<  m_response << "\r\n";
            if (m_response.size() > 0) {
                if (m_response.contains("ok", Qt::CaseInsensitive)){
                    m_line_send = 7;
                    emit signal_sendLine();
                } else{
                    m_error_MSG.append(m_response);
                    res = false;
                }
            } else{
                res = false;
            }
            m_response ="";
            break;

        case 7:
            m_response = sendLineAndGrab("DATA");
            //qDebug() << "DATA回复：" <<  m_response << "\r\n";
            if(m_response.size() > 0){
               if(m_response.contains("354", Qt::CaseInsensitive)){
                   m_line_send = 8;
                   emit signal_sendLine();
               } else{
                   m_error_MSG.append(m_response);
                   res = false;
               }
            } else{
                res = false;
            }
            m_response ="";
            break;

        case 8:
            m_response = sendLineAndGrab(m_message+"\r\n.");
            //qDebug() << "m_message回复：" <<  m_response << "\r\n";
            if(m_response.size() > 0){
               if(m_response.contains("ok", Qt::CaseInsensitive)){
                   m_line_send = 9;
                   emit signal_sendLine();
               } else{
                   m_error_MSG.append(m_response);
                   res = false;
               }
            } else{
                res = false;
            }
            m_response ="";
            break;

        case 9:
            sendLineAndGrab("QUIT");
            break;
        default:
            break;
    }
    if(!res){
        qDebug() << "邮件发送失败,error message:" << m_error_MSG <<"\r\n";
    }
    return res;
}


