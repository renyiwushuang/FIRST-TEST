#include "time_operate.h"

#include<QTime>
#include<QTimer>
#include<QEventLoop>

/*******************************************************************************
 * delay_msec
 *******************************************************************************/
void delay_msec(uint32_t msec,int blocking)
{
    if(blocking == 0){
        QTime Timer = QTime::currentTime().addMSecs(msec);
        while( QTime::currentTime() < Timer){
        };
    }
    else{
        QEventLoop loop;
        QTimer::singleShot(msec, &loop, SLOT(quit()));
        loop.exec();
    }
}
