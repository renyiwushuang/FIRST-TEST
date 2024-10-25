#include "test_ctlr_procotol.h"
#include <QDebug>

/**********************************************************************************************************************
 * location variable define.
 **********************************************************************************************************************/
#define TEST_CTRL_HEAD_CODE  0XA2C5
#define TEST_CTRL_TAIL_CODE  0XB3D6

#define TEST_CTRL_RETERN_HEAD_CODE  0XB2D5
#define TEST_CTRL_RETURN_TAIL_CODE  0XC3E6

/**********************************************************************************************************************
 * function: test ctrl protocol handle.
 * 1、test_ctrl_protocol_package_format.
 * 2、parse_test_ctrl_protocol_package.
 **********************************************************************************************************************/

/**********************************************************************************************************************
 * 1、test_ctrl_protocol_package_format.
 **********************************************************************************************************************/
void test_ctrl_protocol_package_format(stTestCtrlProcotolPkg* testCtrlPakageTemp,
                                       uint8_t advAddr, enTestCtrlCmd opCode, uint8_t dataLength, uint8_t* dataSrouce)
{
    uint8_t u8Buff[256] = {0};//????
    testCtrlPakageTemp->head_code    = TEST_CTRL_HEAD_CODE;
    testCtrlPakageTemp->adv_addr     = advAddr;
    testCtrlPakageTemp->operat_code  = opCode;
    testCtrlPakageTemp->data_leng    = dataLength;
    testCtrlPakageTemp->operat_data  = dataSrouce;

    u8Buff[0] = testCtrlPakageTemp->adv_addr;
    u8Buff[1] = testCtrlPakageTemp->operat_code;
    u8Buff[2] = testCtrlPakageTemp->data_leng;

    if(dataLength != 0)
    {
        for(uint8_t i=0; i<dataLength; i++)
        {
            u8Buff[3+i] = testCtrlPakageTemp->operat_data[i];
        }
    }

    testCtrlPakageTemp->u8crc        = rom_crc8_maxim(u8Buff, 3+dataLength, 0x00);
    testCtrlPakageTemp->tail_code    = TEST_CTRL_TAIL_CODE;
}

/*******************************************************************************
 * process_ctrl_protocol_parse_error_data.
 *******************************************************************************/
static void process_ctrl_protocol_parse_error_data( stRingBuff_t *pRingBuff,uint32_t errorrCnt)
{
    uint8_t  parseErrorData = 0;                        //干扰数据存储变量
    for(uint32_t i=0; i< errorrCnt; i++){
        pop_ring_buf(pRingBuff,&parseErrorData);        //弹出解析错误数据
        //qDebug("parse_err_data %d",parse_err_data);
    }
}

/*******************************************************************************
 * process_ctrl_protocol_parse_success_data.
 *******************************************************************************/
static void process_ctrl_protocol_parse_success_data( stRingBuff_t *pRingBuff,uint32_t succesCnt)
{
    uint8_t  parseSuccessData = 0;                        //数据存储变量
    for(uint32_t i=0; i< succesCnt; i++){
        pop_ring_buf(pRingBuff,&parseSuccessData);        //弹出解析数据
        //qDebug("parseSuccessData %d",parseSuccessData);
    }
}

uint8_t dataLeng = 0;
/**********************************************************************************************************************
 * 2、parse_test_ctrl_protocol_package.
 **********************************************************************************************************************/
enParseStatue parse_test_ctrl_protocol_package(stRingBuff_t *pRingBuff, stTestCtrlProcotolInfo_t*stTestCtrlProcotolInfo)
{
    if(NULL==pRingBuff || get_ring_buff_cnt(pRingBuff)< 6){ //解析进入判断条件
        qDebug("解析条件不满足");
        return PARSE_CONDITION_FAIL;
    } else { //进入解析处理
        while (false == is_ring_buff_empty(pRingBuff)) {

            qDebug("解析条件满足");
            //uint8_t data_leng = 0;  //接收数据长度

            int index = RING_BUF_IDX_tail(0,pRingBuff->tail); //得到循环队列中的下标索引

            if(pRingBuff->buffer[index] != (TEST_CTRL_RETERN_HEAD_CODE & 0x00FF)){        //包头校验
                qDebug("[1]test head0 parse fail %02x",pRingBuff->buffer[index]);
                process_ctrl_protocol_parse_error_data(pRingBuff,1);    continue;
            }

            if(pRingBuff->buffer[index+1] != ((TEST_CTRL_RETERN_HEAD_CODE & 0xFF00)>>8)){
                qDebug("[2]test head1 parse fail %02x",pRingBuff->buffer[index+1]);
                process_ctrl_protocol_parse_error_data(pRingBuff,2);    continue;
            }

            //qDebug("test head code parse success");

            if(pRingBuff->buffer[index+2] > 200){                                       //地址校验
                qDebug("[3]test addr parse fail %02x",pRingBuff->buffer[index+2]);
                process_ctrl_protocol_parse_error_data(pRingBuff,3);    continue;
            }

            if(pRingBuff->buffer[index+3]> TEST_MAX_CMD){                          //操作码校验
                qDebug("[4]test case  parse fail,%02x",pRingBuff->buffer[index+3]);
                process_ctrl_protocol_parse_error_data(pRingBuff,4);    continue;
            } else {
                stTestCtrlProcotolInfo->testCaseType = (enTestCtrlCmd)pRingBuff->buffer[index+3];
            }

            if((pRingBuff->buffer[index+4] > 250)||(pRingBuff->buffer[index+4]< 0)){     //包长校验
                qDebug("[5]test lenght parse fail %02x",pRingBuff->buffer[index+4]);
                process_ctrl_protocol_parse_error_data(pRingBuff,5);    continue;
            }

            //数据长度
            dataLeng = pRingBuff->buffer[index+4];
            stTestCtrlProcotolInfo->dataLength = dataLeng;

            //校验码
            uint8_t u8Crc = rom_crc8_maxim(&pRingBuff->buffer[index+2], 3+dataLeng, 0x00);
            if(pRingBuff->buffer[index+5+dataLeng] != u8Crc){
                qDebug("[6]test crc parse fail %02x",pRingBuff->buffer[index+5+dataLeng]);
                process_ctrl_protocol_parse_error_data(pRingBuff,6+dataLeng);    continue;
            }

            //("test data parse success");
            for(uint8_t copyNum=0; copyNum<dataLeng; copyNum++)
            {
                stTestCtrlProcotolInfo->testDataResult[copyNum] = pRingBuff->buffer[index + 5 + copyNum];
            }

            if(pRingBuff->buffer[index+6+dataLeng] != (TEST_CTRL_RETURN_TAIL_CODE & 0x00FF)){ //包尾校验
                qDebug("[6]test tail0 parse fail  src[E6]  recv[%02x]",pRingBuff->buffer[index+6+dataLeng]);
                qDebug("[6]dataLeng [%02x]",dataLeng);

                process_ctrl_protocol_parse_error_data(pRingBuff,7+dataLeng);    continue;
            }

            if(pRingBuff->buffer[index+7+dataLeng] != ((TEST_CTRL_RETURN_TAIL_CODE & 0xFF00)>>8)){
                qDebug("[7]test tail1 parse fail src[c3]  recv[%02x]",pRingBuff->buffer[index+7+dataLeng]);
                process_ctrl_protocol_parse_error_data(pRingBuff,8+dataLeng);    continue;
            }

            qDebug("test parse success");
            process_ctrl_protocol_parse_success_data(pRingBuff,8+dataLeng);
            return PARSE_SUCCESS_NEW;
        }
        return PARSE_FAIL;
    }
}
