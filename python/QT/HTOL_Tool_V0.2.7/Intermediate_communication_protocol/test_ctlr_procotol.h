#ifndef TESTCTLRPROCOTOL_H
#define TESTCTLRPROCOTOL_H

#include <stdint.h>
#include "communication_common.h"
#include "protocol_crc.h"

#define    DFU_VERSION       0x01

#pragma pack(1)
typedef struct
{
    uint16_t    head_code;
    uint8_t     adv_addr;
    uint8_t     operat_code;
    uint8_t     data_leng;
    uint8_t*    operat_data;
    uint8_t     u8crc;
    uint16_t    tail_code;

}stTestCtrlProcotolPkg;
#pragma pack()


typedef enum
{
    PARSE_SUCCESS_NEW,
    PARSE_FAIL,
    PARSE_HEARD_FAIL,
    PARSE_ADV_ADDR_FAIL,
    PARSE_LENGTH_FAIL,
    PARSE_OPCODE_FAIL,
    PARSE_TAIL_FAIL,
    PARSE_CONDITION_FAIL

}enParseStatue;

typedef enum
{
    GPIO_TEST_CMD         = 0x01,
    SPI_TEST_CMD          = 0x02,
    I2C_TEST_CMD          = 0x03,
    CAN_TEST_CMD          = 0x04,
    FLASH_TEST_CMD        = 0x05,
    RF_TX_TEST_CMD        = 0x06,
    RF_RX_TEST_CMD        = 0x07,
    TRX_CYC_TEST_CMD      = 0x08,
    DCXO_CALIBRAT_CMD     = 0x09,

    GET_DFU_INFO          = 0xE1,
    GET_CHIP_INFO         = 0xE2,
    SHAKE_HAND            = 0xE3,
    UPGRADE_REQ           = 0xE4,
    WRITE_DATA            = 0xE5,
    READ_DATA             = 0xE6,
    ERASE_FLASH           = 0xE7,
    CHECK_DATA            = 0xE8,
    RESET_CHIP            = 0xE9,

    DEVICE_ID_WRITE       = 0xF0,
    DEVICE_ID_READ        = 0xF1,

    TEST_MAX_CMD = DEVICE_ID_READ,

}enTestCtrlCmd;

typedef enum{
    UPGRADE_CHIP_MXD2710  = 0X01,

} enUpgradeChipInfo_t;

typedef enum
{
    UPGRADE_SKIP_SHAKE = 0x01,
    UPGRADE_WITH_SHAKE = 0x02,

} enShakeType_t;

typedef enum
{
    UPGRADE_CODE_TYPE = 0x00,
    UPGRADE_DATA_TYPE = 0x01,

} enUpgradeType_t;

typedef enum
{
    UPGRADE_ALLOW      = 0x00,
    UPGRADE_NOT_ALLOW  = 0x01,

} enUpgradeEnableType_t;

#pragma pack(1)
typedef struct
{
    enUpgradeChipInfo_t enUpgradeChipInfo;
    uint8_t             u8UpgradeRomVersion;
    uint8_t             u8UpgradeBoot2Version;
    uint16_t            u16UpgradeAppVersion;
    uint32_t            u32UpgradeCodeSize;
    uint32_t            u32UpgradeCodeCrc;

}stChipFirmwareInfo_t;

typedef struct
{
    uint32_t      u32CrcAddr;
    uint32_t      u32CrcLen;
    uint32_t      u32CrcInit;

}stFirmwareCheckInfo_t;

typedef struct
{
    uint8_t      u8RstMode;
    uint16_t     u16DelayTime;

}stFirmwareRestart_t;

typedef struct
{
    enUpgradeEnableType_t upgradeEnableType;
    uint8_t              upgradeMaxPackageLength;

}stUpgradeRspInfo_t;


typedef struct
{
    enTestCtrlCmd testCaseType;
    uint8_t       dataLength;
    uint8_t       testDataResult[256];

}stTestCtrlProcotolInfo_t;

typedef enum
{
    EN_RET_OK   = 0x00,
    EN_RET_ERR  = 0x01,
}EN_RET_STA_T;

typedef enum{
    CONFIGER_TYPE,
    SEND_DATA_TYPE,
    RECIVE_DATA_TYPE
}enLogType;

extern void test_ctrl_protocol_package_format(stTestCtrlProcotolPkg* testCtrlPakageTemp,
                                              uint8_t advAddr,
                                              enTestCtrlCmd opCode,
                                              uint8_t dataLength,
                                              uint8_t* dataSrouce);

extern enParseStatue parse_test_ctrl_protocol_package(stRingBuff_t *pRingBuff,stTestCtrlProcotolInfo_t* stTestCtrlProcotolInfo);

#endif // TESTCTLRPROCOTOL_H
