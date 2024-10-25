#ifndef PROTOCOL_CRC_H
#define PROTOCOL_CRC_H

/**********************************************************************************************************************
 * @file     crc.h
 * @version  V1.0
 * @date     2020/01/06
 * @history
 * @note
 **********************************************************************************************************************
 * @attention
 *
 * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS WITH CODING INFORMATION REGARDING THEIR
 * PRODUCTS IN ORDER FOR THEM TO SAVE TIME. AS A RESULT, MAXSCEND SHALL NOT BE HELD LIABLE FOR ANY DIRECT,
 * INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE
 * USE MADE BY CUSTOMERS OF THE CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
 *
 * Copyright (c) 2016~2020, Maxscend Microelectronics Company Limited.
 * All rights reserved.
 *********************************************************************************************************************/


//=====================================================================================================================
// DEFINE
//=====================================================================================================================
#define CRC32_DEFAULT                      ( 0xFFFFFFFF )

#include <stdint.h>


/**
 * @brief  Get crc8 maxim.
 * @param  pu8Buf: The source data.
 * @param  u32Len: The length of data.
 * @param  u8OldCRC8: The last crc value.
 * @return uint8: crc8.
 */
extern uint8_t rom_crc8_maxim(const uint8_t* pu8Data, uint32_t u32Len, uint8_t u8OldCRC8);


/**
 * @brief  Get crc16 ccitt.
 * @param  pu8Buf: The source data.
 * @param  u32Len: The length of data.
 * @param  u16OldCRC16: The last crc value.
 * @return uint16: crc16.
 */
extern uint16_t rom_get_crc16_ccitt(const uint8_t* pu8Data, uint32_t u32Len, uint16_t u16OldCRC16);


/**
 * @brief  Get crc32.
 * @param  pu8Buf: The source data.
 * @param  u32Len: The length of data.
 * @param  u32OldCRC32: The last crc value.
 * @return uint32: crc32.
 */
extern uint32_t rom_get_crc32(const uint8_t *pu8Buf, uint32_t u32Len, uint32_t u32OldCRC32);


#endif // PROTOCOL_CRC_H


