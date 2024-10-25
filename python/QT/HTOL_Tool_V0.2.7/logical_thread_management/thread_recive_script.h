#ifndef THREAD_RECIVE_SCRIPT_H
#define THREAD_RECIVE_SCRIPT_H

#include <QThread>
#include "Intermediate_communication_protocol/communication_protcol.h"

/*******************************Script Memory***********************************/
extern stRingBuff_t *lan_script_cmd_recive_ring_buff;

/*******************************************************************************
 * thread_recive_script,for parse script recive data then send data to different
 * device.
 *******************************************************************************/

class thread_recive_script : public QThread
{
    Q_OBJECT
public:
    explicit thread_recive_script(QObject* parent = nullptr);

public:
    bool is_thread_running = true;
    void run();

signals:
    void recive_data_thread_signal(stThreadRecivDataMsg_t msg);//自定义发送的信号

public slots:
    void recive_data_thread_slot();//自定义槽

};

#endif // THREAD_RECIVE_SCRIPT_H
