#include "communication_protcol.h"
#include "communication_common.h"
#include "string.h"

#include <QMessageBox>
#include <QDebug>


/*******************************************************************************
 * function: MXD Protocol Handle.
 * 1、assembled_mxd_protocol_package.
 * 2、parse_mxd_protocol_package.
 * 3、processing_chip_recive_data.
 * 4、processing_instrument_recive_data.
 *******************************************************************************/

/*******************************************************************************
 * 1、assembled_mxd_protocol_package.
 *******************************************************************************/
stMxdProtocolPackage_t assembled_mxd_protocol_package(
        PROTOCOL_ADDRESS_E     srcAddress,
        PROTOCOL_ADDRESS_E     dstAddress,
        PROTOCOL_CMD_TYPE_E    cmdTypeValue,
        PROTOCOL_CMD_GROUP_E   cmdGroupValue,
        uint16_t cmdValue,
        uint8_t* data, uint16_t dataLen)
{
    stMxdProtocolPackage_t send_protocol_package;

    send_protocol_package.head_code[0]  =   PROTOCOL_HEAD_CODE0;    //包头区-起始码0
    send_protocol_package.head_code[1]  =   PROTOCOL_HEAD_CODE1;    //包头区-起始码1
    send_protocol_package.src_address   =   srcAddress;             //包头区-数据源地址
    send_protocol_package.dst_address   =   dstAddress;             //包头区-数据目标地址
    send_protocol_package.data_len      =   dataLen + 6;            //包头区-数据长度
    uint16_t crc8 = crc8_maxim(&(send_protocol_package.head_code[0]),6);
    send_protocol_package.Head_crc8     =   crc8;                   //包头区-包头校验

    send_protocol_package.cmd_type      =   cmdTypeValue;           //数据区-命令操作类型
    send_protocol_package.cmd_group     =   cmdGroupValue;          //数据区-命令组
    send_protocol_package.cmd_value     =   cmdValue;               //数据区-命令值
    send_protocol_package.reserve[0]    =   0x00;                   //数据区-预留0
    send_protocol_package.reserve[1]    =   0x00;                   //数据区-预留1
    memcpy(send_protocol_package.data, data, dataLen);              //数据区-发送数据

    uint16_t crc16 = crc16_ccitt_xmode(&(send_protocol_package.cmd_type),
                                         send_protocol_package.data_len);
    send_protocol_package.data_crc16[0] =   crc16 & 0xFF;           //包尾区-数据区CRC16L
    send_protocol_package.data_crc16[1] =   ((crc16 & 0xFF00) >> 8);//包尾区-数据区CRC16H
    send_protocol_package.tail_code[0]  =   PROTOCOL_TAIL_CODE0;    //包尾区-协议包尾码
    send_protocol_package.tail_code[1]  =   PROTOCOL_TAIL_CODE1;    //包尾区-协议包尾码

    send_protocol_package.protocol_len  =   17 + dataLen;           //协议包长

    return send_protocol_package;
}

/*******************************************************************************
 * 1.1、assembled_mxd_protocol_package.
 *******************************************************************************/
stMxdProtocolPackage_t assembled_mxd_extern_protocol_package(
        PROTOCOL_ADDRESS_E      srcAddress,
        PROTOCOL_ADDRESS_E      dstAddress,
        PROTOCOL_CMD_TYPE_E     cmdTypeValue,
        PROTOCOL_CMD_GROUP_E    cmdGroupValue,
        uint16_t                cmdValue,
        uint16_t                reserveValue,
        uint8_t *data, uint16_t u16DataLen)
{
    stMxdProtocolPackage_t send_protocol_package;

    send_protocol_package.head_code[0]  =   PROTOCOL_HEAD_CODE0;        //包头区-起始码0
    send_protocol_package.head_code[1]  =   PROTOCOL_HEAD_CODE1;        //包头区-起始码1
    send_protocol_package.src_address   =   srcAddress;                 //包头区-数据源地址
    send_protocol_package.dst_address   =   dstAddress;                 //包头区-数据目标地址
    send_protocol_package.data_len      =   u16DataLen + 6;             //包头区-数据长度
    uint16_t crc8 = crc8_maxim(&(send_protocol_package.head_code[0]),6);
    send_protocol_package.Head_crc8     =   crc8;                       //包头区-包头校验

    send_protocol_package.cmd_type      =   cmdTypeValue;               //数据区-命令操作类型
    send_protocol_package.cmd_group     =   cmdGroupValue;              //数据区-命令组
    send_protocol_package.cmd_value     =   cmdValue;                   //数据区-命令值
    send_protocol_package.reserve[0]    =   reserveValue & 0X00FF;      //数据区-预留0
    send_protocol_package.reserve[1]    =   reserveValue & 0XFF00>>8;   //数据区-预留1
    memcpy(send_protocol_package.data, data, u16DataLen);               //数据区-发送数据

    uint16_t crc16 = crc16_ccitt_xmode(&(send_protocol_package.cmd_type),
                                         send_protocol_package.data_len);
    send_protocol_package.data_crc16[0] =   crc16 & 0xFF;               //包尾区-数据区CRC16L
    send_protocol_package.data_crc16[1] =   ((crc16 & 0xFF00) >> 8);    //包尾区-数据区CRC16H
    send_protocol_package.tail_code[0]  =   PROTOCOL_TAIL_CODE0;        //包尾区-协议包尾码
    send_protocol_package.tail_code[1]  =   PROTOCOL_TAIL_CODE1;        //包尾区-协议包尾码

    send_protocol_package.protocol_len  =   17 + u16DataLen;            //协议包长

    return send_protocol_package;
}


/*******************************************************************************
 * processing_mxd_protocol_parse_error_data.
 *******************************************************************************/
static void processing_mxd_protocol_parse_error_data(stRingBuff_t *pRingBuff,
                                                     uint32_t error_cnt)
{
    uint8_t  parse_err_data = 0;                        //干扰数据存储变量
    for(uint32_t i=0; i< error_cnt; i++){
        pop_ring_buf(pRingBuff,&parse_err_data);        //弹出解析错误数据
        qDebug("parse_err_data %d",parse_err_data);
    }
}

/*******************************************************************************
 * processing_mxd_protocol_parse_success_data
 *******************************************************************************/
static void processing_mxd_protocol_parse_success_data(stRingBuff_t *pRingBuff,
                                                       uint32_t data_cnt)
{
    uint8_t  parse_data = 0;                            //解析正确数据存储变量
    for(uint32_t i=0; i< data_cnt; i++){
        pop_ring_buf(pRingBuff,&parse_data);            //弹出解析错误数据
        //qDebug("parse_data %d",parse_data);
    }
}

/*******************************************************************************
 * 2、parse_mxd_protocol_package.
 *******************************************************************************/
stMxdProtocolPackage_t parse_mxd_protocol_package(stRingBuff_t *pRingBuff)
{
    int idx = 0;                                    //循环buffer索引变量
    int really_data_len = 0;                        //有效负载数据长度
    int recv_len =  get_ring_buff_cnt(pRingBuff);   //循环buffer数据长度

    stMxdProtocolPackage_t protocolRecv;            //存储当前数据包解析出来的数据

    if(NULL==pRingBuff || recv_len < 17){           //解析进入判断条件
        protocolRecv = {};
        return protocolRecv;

    } else {                                        //进入解析处理
        while(!is_ring_buff_empty(pRingBuff))
        {
            idx = RING_BUF_IDX_tail(0,pRingBuff->tail);//得到循环队列中的下标索引

            //包头区处理：起始码0 起始码1 数据源地址 数据目标地址 数据长度 包头校验
            protocolRecv.head_code[0] = pRingBuff->buffer[RING_BUF_IDX(idx)];
            if(protocolRecv.head_code[0] != PROTOCOL_HEAD_CODE0){
                processing_mxd_protocol_parse_error_data(pRingBuff,1); continue;
            }

            protocolRecv.head_code[1] = pRingBuff->buffer[RING_BUF_IDX(idx + 1)];
            if(protocolRecv.head_code[1] != PROTOCOL_HEAD_CODE1){
                processing_mxd_protocol_parse_error_data(pRingBuff,2); continue;
            }

            protocolRecv.src_address = pRingBuff->buffer[RING_BUF_IDX(idx + 2)];
            protocolRecv.dst_address = pRingBuff->buffer[RING_BUF_IDX(idx + 3)];
            protocolRecv.data_len    = pRingBuff->buffer[RING_BUF_IDX(idx + 4)];
            protocolRecv.data_len   += pRingBuff->buffer[RING_BUF_IDX(idx + 5)] << 8;
            if(protocolRecv.data_len < 6){
                processing_mxd_protocol_parse_error_data(pRingBuff,6); continue;
            }
            really_data_len = protocolRecv.data_len - 6;

            protocolRecv.Head_crc8 = pRingBuff->buffer[RING_BUF_IDX(idx + 6)];
            uint8_t protoco_crc8 = ring_buff_crc8_maxim(pRingBuff,idx,6);
            if(protocolRecv.Head_crc8 != protoco_crc8){
                processing_mxd_protocol_parse_error_data(pRingBuff,7); continue;
            }

            //断包检测返回
            if(recv_len < 11 + protocolRecv.data_len){
                break;
            }

            //数据区处理：命令类型 命令组 命令值 预留值 负载数据
            protocolRecv.cmd_type   = pRingBuff->buffer[RING_BUF_IDX(idx + 7)];
            protocolRecv.cmd_group  = pRingBuff->buffer[RING_BUF_IDX(idx + 8)];
            protocolRecv.cmd_value  = pRingBuff->buffer[RING_BUF_IDX(idx + 9)];
            protocolRecv.cmd_value += pRingBuff->buffer[RING_BUF_IDX(idx + 10)] << 8;
            protocolRecv.reserve[0] = pRingBuff->buffer[RING_BUF_IDX(idx + 11)];
            protocolRecv.reserve[1] = pRingBuff->buffer[RING_BUF_IDX(idx + 12)];

            for(uint16_t n = 0; n < really_data_len; n++){  //协议包负载数据
                protocolRecv.data[n] =  pRingBuff->buffer[RING_BUF_IDX(idx + 13 + n)];
                //qDebug()<<"protocolRecv.data:"<<protocolRecv.data[n];
            }

            //包尾区处理：校验码0 校验码1 包尾码0 包尾码1
            protocolRecv.data_crc16[0] = pRingBuff->buffer[RING_BUF_IDX(idx + 13 + really_data_len)];
            protocolRecv.data_crc16[1] = pRingBuff->buffer[RING_BUF_IDX(idx + 14 + really_data_len)];
            uint16_t crc16 = ring_buff_crc16_ccitt_xmode(pRingBuff,RING_BUF_IDX(idx + 7),protocolRecv.data_len);

            if( (protocolRecv.data_crc16[0] == (crc16 & 0xFF)) &&
                (protocolRecv.data_crc16[1] == ((crc16 >> 8) & 0xFF))){
            }
            else{
                qDebug()<<"protocolRecv.data_crc16[0]:"<<protocolRecv.data_crc16[0];
                qDebug()<<"crc16[0]:"<<(crc16 & 0xFF);
                qDebug()<<"protocolRecv.data_crc16[1]:"<<protocolRecv.data_crc16[1];
                qDebug()<<"crc16[1]:"<<((crc16 >> 8) & 0xFF);
            }

            protocolRecv.tail_code[0] = pRingBuff->buffer[RING_BUF_IDX(idx + 15 + really_data_len)];
            if(protocolRecv.tail_code[0] != PROTOCOL_TAIL_CODE0)
            {
                qDebug()<<"protocolRecv.tail_code[0]:"<<protocolRecv.tail_code[0];
                processing_mxd_protocol_parse_error_data(pRingBuff,16 + really_data_len); continue;
            }

            protocolRecv.tail_code[1] = pRingBuff->buffer[RING_BUF_IDX(idx + 16 + really_data_len)];
            if(protocolRecv.tail_code[1] != PROTOCOL_TAIL_CODE1)
            {
                qDebug()<<"protocolRecv.tail_code[1]:"<<protocolRecv.tail_code[1];
                processing_mxd_protocol_parse_error_data(pRingBuff,17 + really_data_len); continue;
            }
            qDebug()<<"protocolRecv.tail_code[1] OK";

            /******************************单包解析结束***********************************/
            //提取完整通信数据包
            processing_mxd_protocol_parse_success_data(pRingBuff,17 + really_data_len);

            protocolRecv.protocol_len = 17 + really_data_len;
            qDebug("protocolRecv.protocol_len: %d", protocolRecv.protocol_len);

            return protocolRecv;
        }
        protocolRecv = {};
        return protocolRecv;
    }
}

/************************************************************************************
 * 3、processing_chip_recive_data.
 ************************************************************************************/
stThreadRecivDataMsg_t processing_chip_recive_data(stMxdProtocolPackage_t chipProtocolPackage)
{
    stThreadRecivDataMsg_t user_info;//存储用户需要的数据
    user_info.send_port = (PROTOCOL_ADDRESS_E)chipProtocolPackage.dst_address;
    user_info.send_length = chipProtocolPackage.data_len + 11;    //输出整个协议数据包：有效数据包+冗余数据包
    memcpy(user_info.send_data, &chipProtocolPackage, user_info.send_length - 4);
    memcpy(&user_info.send_data[user_info.send_length - 4], &chipProtocolPackage.data_crc16[0], 4);
    return user_info;
}

/************************************************************************************
 * 4、processing_instrument_recive_data.
 ************************************************************************************/
stThreadRecivDataMsg_t processing_instrument_recive_data(stMxdProtocolPackage_t instrumentProtocolPackage)
{
    stThreadRecivDataMsg_t user_info;//存储用户需要的数据
    user_info.send_port = (PROTOCOL_ADDRESS_E)instrumentProtocolPackage.dst_address;
    user_info.send_length = instrumentProtocolPackage.data_len - 6; //输出有效数据包
    memcpy(user_info.send_data, &instrumentProtocolPackage.data, user_info.send_length);
    return user_info;
}
