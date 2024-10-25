#include "thread_recive_maxscend_device.h"
#include "Intermediate_memory_management/communication_memory_manager.h"


extern stRingBuff_t *g_uartTestProtocolReciveRingBuff;

thread_recive_maxscend_device::thread_recive_maxscend_device(QObject *parent) : QThread(parent)
{
     qRegisterMetaType<stTestCtrlProcotolInfo_t>("stTestCtrlProcotolInfo_t");
}

stTestCtrlProcotolInfo_t testCtrlProtocolInfo;      //存储用户需要的数据

void thread_recive_maxscend_device :: run()
{
    enParseStatue  parseStatue = PARSE_CONDITION_FAIL;

    while (true) {

        if(false == is_ring_buff_empty(g_uartTestProtocolReciveRingBuff)){

            if(get_ring_buff_cnt(g_uartTestProtocolReciveRingBuff) >6){

                //qDebug("into thread handler");
                parseStatue = parse_test_ctrl_protocol_package(g_uartTestProtocolReciveRingBuff,&testCtrlProtocolInfo);

                //qDebug("testDataResult %d",testCtrlProtocolInfo.testDataResult[0]);
                if(parseStatue == PARSE_SUCCESS_NEW){          //转发到应用层
                    emit recive_maxscend_data_thread_signal(testCtrlProtocolInfo);
                }else{
                   qDebug("parseStatue %d",parseStatue);
                }
            }

        }
        usleep(1);
    }
}
