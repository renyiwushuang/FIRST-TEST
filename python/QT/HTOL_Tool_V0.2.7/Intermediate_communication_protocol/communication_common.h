#ifndef COMMUNICATION_COMMON_H
#define COMMUNICATION_COMMON_H

#include <stdint.h>

/*******************************************************************************
 * Ring buffer define
 *******************************************************************************/
typedef enum{
    OPERATOR_SUCCESS,
    OPERATOR_FAIL

}RING_BUFF_OPERATION_STA;

#define RING_SIZE  (1024U)
#define RING_MASK  (RING_SIZE - 1)

typedef uint32_t RingBuffSize_t;
typedef uint8_t  RingBuffType_t;

typedef struct{
    RingBuffSize_t  head;
    RingBuffSize_t  tail;
    RingBuffType_t  buffer[1];  //应该是0长数组，未解决编译警告问题改为1长数组，生成的BUFF长度加1

}stRingBuff_t;

#define RING_BUF_IDX(idx)           ((idx) & RING_MASK)        //循环BUF头索引值
#define RING_BUF_IDX_tail(idx,tail) ((idx + tail) & RING_MASK) //循环BUF数据起始头索引值
#define RING_BUF_FIFO_OVERRIDE                                 //循环BUF覆盖功能

/*******************************************************************************
 * 循环BUF满：返回1，否则返回0
 *******************************************************************************/
inline bool is_ring_buff_full(stRingBuff_t *pRingBuff) {
  return (((pRingBuff->head + 1) & RING_MASK) == pRingBuff->tail);
}

/*******************************************************************************
 * 循环BUF空：返回1，否则返回0
 *******************************************************************************/
inline bool is_ring_buff_empty(stRingBuff_t *pRingBuff) {
  return (pRingBuff->head == pRingBuff->tail);
}

/*******************************************************************************
 * 获取循环BUF的有效长度，即计数cnt
 *******************************************************************************/
inline uint32_t get_ring_buff_cnt(stRingBuff_t *pRingBuff) {
  return ((pRingBuff->head - pRingBuff->tail + RING_SIZE) & RING_MASK);
}

/*******************************************************************************
 * 动态创建循环BUF
 *******************************************************************************/
extern stRingBuff_t* creat_ring_buff(int capacity);

/*******************************************************************************
 * 写入数据到循环BUF
 *******************************************************************************/
extern RING_BUFF_OPERATION_STA push_ring_buf(stRingBuff_t *pRingBuff, uint8_t data);

/*******************************************************************************
 * 读取循环BUF的数据
 *******************************************************************************/
extern RING_BUFF_OPERATION_STA pop_ring_buf(stRingBuff_t *pRingBuff, uint8_t *data);

/*******************************************************************************
 * crc16_ccitt_xmode
 *******************************************************************************/
extern uint16_t crc16_ccitt_xmode(uint8_t *data, uint32_t u32Len);

/*******************************************************************************
 * ring_buff_crc16_ccitt_xmode
 *******************************************************************************/
extern uint16_t ring_buff_crc16_ccitt_xmode(const stRingBuff_t *pRingBuff, int idx,
                                            uint32_t u32Len);

/*******************************************************************************
 * crc8_maxim
 *******************************************************************************/
extern uint8_t crc8_maxim(uint8_t *data, uint8_t u8Len);

/*******************************************************************************
 * ring_buff_crc8_maxim
 *******************************************************************************/
extern uint8_t  ring_buff_crc8_maxim(const stRingBuff_t *pRingBuff, int idx,
                                     uint32_t u32Len);

#endif // COMMUNICATION_COMMON_H
