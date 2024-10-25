#ifndef TIME_OPERATE_H
#define TIME_OPERATE_H

#include <stdint.h>


typedef enum{
    Timeout_flag    = 1,
    Right_reponse   = 2,
    Time_close      = 3,

}EN_TIME_FLAG_T;



/*******************************************************************************
 * delay_msec
 *******************************************************************************/
void delay_msec(uint32_t msec,int blocking);

#endif //TIME_OPERATE_H
