#ifndef THREAD_RECIVE_MAXSCEND_DEVICE_H
#define THREAD_RECIVE_MAXSCEND_DEVICE_H

#include <QThread>
#include "Intermediate_communication_protocol/test_ctlr_procotol.h"

/*******************************************************************************
 * thread_recive_maxscend_device: use for parse maxscend chip send data then
 * send data to test script.
 *******************************************************************************/
class thread_recive_maxscend_device : public QThread
{
    Q_OBJECT

public:
    thread_recive_maxscend_device(QObject* parent = nullptr);

public:
    void run() ;

signals:
    void recive_maxscend_data_thread_signal(stTestCtrlProcotolInfo_t msg);
};

#endif // THREAD_RECIVE_MAXSCEND_DEVICE_H
