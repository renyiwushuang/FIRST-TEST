#include "common_data_conversion.h"

#include <QDebug>
#include <QDataStream>
/*******************************************************************************
 * StringTohex
 *******************************************************************************/
uint8_t StringTohex(QString String)
{
    bool ok;
    uint8_t ret = 0;
    String = String.trimmed();
    String = String.simplified();
    QStringList sl = String.split(" ");

    foreach (QString s, sl) {
        if(!s.isEmpty()) {
            char c = s.toInt(&ok,16)&0xFF;
            if(ok){
                ret = c;
            }else{
                qDebug()<<u8"非法的16进制字符："<<s;
            }
        }
    }
    return ret;
}

/*******************************************************************************
 * StringToByteArray
 *******************************************************************************/
QByteArray StringToByteArray(QString String)
{
    bool ok;
    QByteArray ret = 0;
    String = String.trimmed();
    String = String.simplified();
    QStringList sl = String.split(" ");

    foreach (QString s, sl) {
        if(!s.isEmpty()) {
            char c = s.toInt(&ok,16)&0xFF;
            if(ok){
                ret.append(c);
            }else{
                qDebug()<<u8"非法的16进制字符："<<s;
            }
        }
    }
    return ret;
}

/*******************************************************************************
 * string_to_bytearray
 *******************************************************************************/
QByteArray string_to_bytearray(QString String)
{
    QByteArray ret = 0;
    ret = String.toUtf8();

    return ret;
}

/*******************************************************************************
 * ByteArrayToString
 *******************************************************************************/
QString ByteArrayToString(QByteArray &ba)
{
    QDataStream out(&ba,QIODevice::ReadWrite);   //将str的数据 读到out里面去
    QString buf;
    while(!out.atEnd())
    {
        qint8 outChar = 0;
        out >> outChar;   //每次一个字节的填充到 outchar
        QString str = QString("%1").arg(outChar&0xFF,2,16,QLatin1Char('0')).toUpper()
                      + QString(" ");   //2 字符宽度
        buf += str;
    }
    return buf;
}

/*******************************************************************************
 * ByteArrayToString
 *******************************************************************************/
uint32_t big_to_little_endian(uint32_t data)
{
    uint32_t data_temp;
    data_temp  = (data & 0x000000FF)<<24;
    data_temp |= (data & 0x0000FF00)<<8;
    data_temp |= (data & 0x00FF0000)>>8;
    data_temp |= (data & 0xFF000000)>>24;

    return data_temp;
}

/*******************************************************************************
 * ByteArrayToString
 *******************************************************************************/
QByteArray data_uint32_to_bytearry(uint32_t date)
{
    QByteArray bytearray_temp = 0;
    bytearray_temp.append(date & 0x000000FF);
    bytearray_temp.append(date & 0x0000FF00>>8);
    bytearray_temp.append(date & 0x00FF0000>>16);
    bytearray_temp.append(date & 0xFF000000>>24);

    return bytearray_temp;
}

/*******************************************************************************
 * HexToAscii
 *******************************************************************************/
void HexToAscii(char *pHex, char *pAscii, uint32_t u32Len)
{
    char temp[2];
    for (uint32_t i = 0; i < u32Len; i++){

        temp[0] = (pHex[i] & 0xF0) >> 4;
        temp[1] = pHex[i] & 0x0F;

        for (uint32_t j = 0; j < 2; j++){
            if (temp[j] < 10){
                temp[j] += 0x30;
            }
            else{
                if (temp[j] < 16)
                    temp[j] = temp[j] - 10 + 'A';
            }
            *pAscii++ = temp[j];
        }
    }
}

/*******************************************************************************
 * ByteArrayToString
 *******************************************************************************/
void ByteArrayToAscii(QByteArray sendByteArray,char* pAsciiOutBuff)
{
    char send_byteArray_char[1025];
    int len_array = sendByteArray.size();
    memcpy(send_byteArray_char,sendByteArray,len_array);
    HexToAscii(send_byteArray_char, pAsciiOutBuff, len_array);
}

/*******************************************************************************
 * ringBuffToByteArray
 *******************************************************************************/
QByteArray ringBuffToByteArray(stRingBuff_t *pRingBuff,uint32_t u32Len)
{
    QByteArray  byteArray_temp;
    uint8_t     data_temp;

    for (uint32_t i = 0;i < u32Len;i++) {
        pop_ring_buf(pRingBuff,&data_temp);
        byteArray_temp[i] = data_temp;
        data_temp = 0;
    }
    return byteArray_temp;
}

/*******************************************************************************
 * ascii_to_hex (only for data part)
 *******************************************************************************/
void ascii_to_hex(uint8_t* ascii_array,uint8_t* hex_array,uint16_t array_len)
{
    for(uint16_t i=0;i<array_len;i++)
    {
        if((0x2F< ascii_array[i])&&(ascii_array[i]<0X3A)){
          hex_array[i] = ascii_array[i] - 0x30;
        }
        if((0x40< ascii_array[i])&&(ascii_array[i]<0X47)){
          hex_array[i] = ascii_array[i] - 0x41 + 10;
        }
    }
}
