#include "bin_file_parse.h"
#include "string.h"
#include <QDebug>
#include <QFile>
#include <QDataStream>

/***********************************************************************************************************************************
 * Location temp value define.
 **********************************************************************************************************************************/


/***********************************************************************************************************************************
 * function: upgrade protocol handle.
 **********************************************************************************************************************************/

/*******************************************************************************
 * 1、get mxd bin file info.
 *******************************************************************************/
bool get_mxd_bin_file_info(QString filePatch, stMxdBinInfo * mxdBinInfo)
{
    uint8_t updateBinInfoBuff[16] = {0};

    if(filePatch.isEmpty() == false){
        QFile binfile;
        binfile.setFileName(filePatch);

        bool opetationState = binfile.open(QIODevice::ReadOnly);
        if(opetationState == true){

            QDataStream in(&binfile);
            in.setByteOrder(QDataStream::LittleEndian);
            in.readRawData((char*)updateBinInfoBuff,16);
            binfile.close();
        }

        mxdBinInfo->binFlag      = updateBinInfoBuff[0]+(updateBinInfoBuff[1]<<8);
        mxdBinInfo->chipType     = updateBinInfoBuff[2];
        mxdBinInfo->upgradeCode  = updateBinInfoBuff[3];
        mxdBinInfo->romVersion   = updateBinInfoBuff[4];
        mxdBinInfo->bootVersion  = updateBinInfoBuff[5];
        mxdBinInfo->appVersion   = updateBinInfoBuff[6]+(updateBinInfoBuff[7]<<8);

        mxdBinInfo->binSize      = (updateBinInfoBuff[8])+((updateBinInfoBuff[9])<<8);
        mxdBinInfo->binSize      += ((updateBinInfoBuff[10])<<16)+((updateBinInfoBuff[11])<<24);

        mxdBinInfo->binCrc       = updateBinInfoBuff[12];
        mxdBinInfo->binCrc       += (updateBinInfoBuff[13]<<8);
        mxdBinInfo->binCrc       += (updateBinInfoBuff[14]<<16);
        mxdBinInfo->binCrc       += (updateBinInfoBuff[15]<<24);

        return true;
    }
    return false;
}

/*******************************************************************************
 * 2、get mxd bin file data.
 *******************************************************************************/
bool get_mxd_bin_file_data(QString filePatch, uint32_t skipStep,uint16_t size,uint8_t*reciveData)
{
    skipStep = 16+ skipStep;

    if(filePatch.isEmpty() == false){

        QFile ota_file;
        ota_file.setFileName(filePatch);
        bool opetation_state = ota_file.open(QIODevice::ReadOnly);

        if(opetation_state == true){

            QDataStream in(&ota_file);
            in.skipRawData(skipStep);//跳过skipStep个样点
            in.setByteOrder(QDataStream::LittleEndian);
            in.readRawData((char*)reciveData,size);
        }
        return true;
    }
    return false;
}

/*******************************************************************************
 * 3、close mxd bin file.
 *******************************************************************************/
bool close_mxd_bin_file(QString filePatch)
{
    if(filePatch.isEmpty() == false){

        QFile ota_file;
        ota_file.setFileName(filePatch);
        bool opetation_state = ota_file.open(QIODevice::ReadOnly);
        if(opetation_state == true){
            ota_file.close();
        }
        return true;
    }
    return false;
}
