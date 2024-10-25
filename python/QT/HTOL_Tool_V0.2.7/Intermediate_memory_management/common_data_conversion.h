#ifndef COMMON_DATA_CONVERSION_H
#define COMMON_DATA_CONVERSION_H

#include "intermediate_communication_protocol/communication_common.h "

#include <stdint.h>
#include <qstring.h>

/*******************************************************************************
 * StringTohex
 *******************************************************************************/
uint8_t StringTohex(QString String);

/*******************************************************************************
 * StringToByteArray
 *******************************************************************************/
QByteArray StringToByteArray(QString String);

/*******************************************************************************
 * string_to_bytearray
 *******************************************************************************/
QByteArray string_to_bytearray(QString String);

/*******************************************************************************
 * data_uint32_to_bytearry
 *******************************************************************************/
QByteArray data_uint32_to_bytearry(uint32_t date);

/*******************************************************************************
 * ringBuffToByteArray
 *******************************************************************************/
QByteArray ringBuffToByteArray(stRingBuff_t *pRingBuff,uint32_t u32Len);

/*******************************************************************************
 * ByteArrayToString
 *******************************************************************************/
QString ByteArrayToString(QByteArray &ba);

/*******************************************************************************
 * big_to_little_endian
 *******************************************************************************/
uint32_t big_to_little_endian(uint32_t data);

/*******************************************************************************
 * ByteArrayToString
 *******************************************************************************/
void ByteArrayToAscii(QByteArray sendByteArray,char* pAsciiOutBuff);

/*******************************************************************************
 * HexToAscii
 *******************************************************************************/
void HexToAscii(char *pHex, char *pAscii, uint32_t u32Len);

/*******************************************************************************
 * ascii_to_hex (only for data part)
 *******************************************************************************/
void ascii_to_hex(uint8_t* ascii_array,uint8_t* hex_array,uint16_t array_len);

#endif // COMMON_DATA_CONVERSION_H
