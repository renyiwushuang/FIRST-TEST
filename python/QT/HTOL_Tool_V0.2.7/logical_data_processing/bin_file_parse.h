#ifndef BIN_FILE_PARSE_H
#define BIN_FILE_PARSE_H

#include "string"
#include <QString>


typedef struct{

    uint16_t        binFlag;
    uint8_t         chipType;
    uint8_t         upgradeCode;
    uint8_t         romVersion;
    uint8_t         bootVersion;
    uint16_t        appVersion;
    uint32_t        binSize;
    uint32_t        binCrc;

}stMxdBinInfo;


extern bool get_mxd_bin_file_info(QString filePatch,stMxdBinInfo * mxdBinInfo);

extern bool get_mxd_bin_file_data(QString filePatch, uint32_t skipStep,uint16_t size,uint8_t*reciveData);

extern bool close_mxd_bin_file(QString filePatch);

#endif  //BIN_FILE_PARSE_H
