#include "thread_recive_script.h"
#include <QTime>
#include <QDebug>

thread_recive_script::thread_recive_script(QObject *parent) : QThread(parent)
{
     qRegisterMetaType<stThreadRecivDataMsg_t>("stThreadRecivDataMsg_t");
}

void thread_recive_script:: recive_data_thread_slot()
{
    qDebug()<<" thread_recive_script run end \r\n";
}

void thread_recive_script:: run()
{
//    PROTOCOL_ADDRESS_E recive_thread_Package_dst;
//    stMxdProtocolPackage_t script_protocolRecv;     //存储当前数据包解析出来的数据
//    stThreadRecivDataMsg_t user_info;               //存储用户需要的数据

//    while (true) {
//        if(0 == is_ring_buff_empty(lan_script_cmd_recive_ring_buff))
//        {
//            script_protocolRecv = parse_mxd_protocol_package(lan_script_cmd_recive_ring_buff);
//            recive_thread_Package_dst = (PROTOCOL_ADDRESS_E)script_protocolRecv.dst_address;

//            if(recive_thread_Package_dst != N0_OTHER_ADDRESS)
//            {
//                if(recive_thread_Package_dst < POWER_ADDRESS0){
//                    user_info = processing_chip_recive_data(script_protocolRecv);
//                }
//                else{
//                    user_info = processing_instrument_recive_data(script_protocolRecv);
//                }
//                emit recive_data_thread_signal(user_info);
//            }
//        }
//        usleep(1);
//    }
}


