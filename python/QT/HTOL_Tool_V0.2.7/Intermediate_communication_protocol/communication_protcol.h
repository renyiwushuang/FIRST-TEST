#ifndef COMMUNICATION_PROTCOL_H
#define COMMUNICATION_PROTCOL_H

#include <stdint.h>
#include "communication_common.h"

#define PROTOCOL_DADA_LENG 1024

#define PROTOCOL_HEAD_CODE0         (0x3D)
#define PROTOCOL_HEAD_CODE1         (0x4C)
#define PROTOCOL_TAIL_CODE0         (0xA1)
#define PROTOCOL_TAIL_CODE1         (0xB2)

typedef enum { //协议设备地址
    MXD_CHIP_ADDRESS0           =   0x00,
    MXD_CHIP_ADDRESS1           =   0x01,
    PC_ADDRESS                  =   0x10,
    MCU_ADDRESS                 =   0x20,
    POWER_ADDRESS0              =   0x30,
    POWER_ADDRESS1              =   0x31,
    DMM_ADDRESS                 =   0x40,
    OSCILLOSCOPE_ADDRESS        =   0x50,
    E_LOAD_ADDRESS              =   0x60,
    SPEC_ADDRESS                =   0x70,
    SIGNAL_GENERATOR_ADDRESS    =   0x80,
    ENSEMBLE_TESTER_ADDRESS     =   0x90,
    LOGIC_ANALYZER_ADDRESS      =   0xA0,
    NETWORK_ANALYSIS_ADDRESS    =   0xB0,
    N0_OTHER_ADDRESS            =   0xFF,

}PROTOCOL_ADDRESS_E;


typedef enum { //协议命令操作类型
    CMD_SEND                    =   0x01,  //下发命令
    CMD_RETURN                  =   0x02,  //数据同步返回命令
    CMD_REPORT                  =   0x03,  //数据异步上报命令

}PROTOCOL_CMD_TYPE_E;


typedef enum { //协议命令组类型
    BLE_CMD_GROUP               =   0x01,
    ANALOG_CMD_GROUP            =   0x02,
    DIGIT_CMD_GROUP             =   0x03,
    RF_CMD_GROUP                =   0x04,
    MTP_CMD_GROUP               =   0x05,
    APPLICATION_CMD_GROUP       =   0x06,
    TEST_PARA_CMD_GROUP         =   0x08,

}PROTOCOL_CMD_GROUP_E;


typedef enum { //协议解析结果
    PARSE_SUCCESS               =   0x00,
    PARSE_HEAD_ERROR            =   0x01,
    PARSE_DATA_MIN_LEN_ERROR    =   0x02,
    PARSE_HEAD_CRC_VERIFY_ERROR =   0x03,
    PARSE_CMD_TYPE_ERROR        =   0x04,
    PARSE_CMD_GROUP_ERROR       =   0x05,
    PARSE_RESERVE_ERROR         =   0x06,
    PARSE_DATA_CRC_VERIFY_ERROR =   0x07,
    PARSE_TAIL_ERROR            =   0x08,
    PARSE_PACKAGE_MIN_LENG_ERROR=   0x09,

}PROTOCOL_PARSE_STA;


typedef enum{ //协议运行状态
    RUN_SUCCESS,
    RUN_ERROR,
    RUN_IDEL,

}PROTOCOL_RUN_STA;


#pragma pack(1)
typedef struct { //测试协议数据包结构体
    uint8_t  head_code[2];               //包头区-起始码
    uint8_t  src_address;                //包头区-源地址
    uint8_t  dst_address;                //包头区-目标地址
    uint16_t data_len;                   //包头区-数据长度
    uint8_t  Head_crc8;                  //包头区-包头CRC8校验

    uint8_t  cmd_type;                   //数据区-命令类型
    uint8_t  cmd_group;                  //数据区-命令组
    uint16_t cmd_value;                  //数据区-命令值
    uint8_t  reserve[2];                 //数据区-数据区预留值
    uint8_t  data[PROTOCOL_DADA_LENG];   //数据区-数据区值

    uint8_t  data_crc16[2];              //包尾区-数据区CRC16校验
    uint8_t  tail_code[2];               //包尾区-包尾码
    uint16_t protocol_len;

}stMxdProtocolPackage_t;

typedef struct{     //协议解析结构体
    PROTOCOL_ADDRESS_E  send_port;
    uint16_t            send_length;
    uint8_t             send_data[1024+64];

}stThreadRecivDataMsg_t;

#pragma pack()

/*******************************************************************************
 * 1、assembled mxd protocol package.
 *******************************************************************************/
extern stMxdProtocolPackage_t assembled_mxd_protocol_package(
        PROTOCOL_ADDRESS_E      srcAddress,
        PROTOCOL_ADDRESS_E      dstAddress,
        PROTOCOL_CMD_TYPE_E     cmdTypeValue,
        PROTOCOL_CMD_GROUP_E    cmdGroupValue,
        uint16_t                cmdValue,
        uint8_t *data, uint16_t u16DataLen);

/*******************************************************************************
 * 2、assembled mxd extern protocol package.
 *******************************************************************************/
extern stMxdProtocolPackage_t assembled_mxd_extern_protocol_package(
        PROTOCOL_ADDRESS_E      srcAddress,
        PROTOCOL_ADDRESS_E      dstAddress,
        PROTOCOL_CMD_TYPE_E     cmdTypeValue,
        PROTOCOL_CMD_GROUP_E    cmdGroupValue,
        uint16_t                cmdValue,
        uint16_t                reserveValue,
        uint8_t *data, uint16_t u16DataLen);

/*******************************************************************************
 * 3、parse_mxd_protocol_package.
 *******************************************************************************/
extern stMxdProtocolPackage_t parse_mxd_protocol_package(stRingBuff_t *pRingBuff);

/*******************************************************************************
 * 4、processing_chip_recive_data.
 *******************************************************************************/
extern stThreadRecivDataMsg_t processing_chip_recive_data(
        stMxdProtocolPackage_t chipProtocolPackage);

/*******************************************************************************
 * 5、processing_instrument_recive_data.
 *******************************************************************************/
extern stThreadRecivDataMsg_t processing_instrument_recive_data(
        stMxdProtocolPackage_t instrumentProtocolPackage);

#endif  //COMMUNICATION_PROTCOL_H
