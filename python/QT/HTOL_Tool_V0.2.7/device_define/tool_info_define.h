#ifndef TOOL_INFODEFINE_H
#define TOOL_INFODEFINE_H
#include <QObject>


#define CFG_GROUP                            "TOOL_INFO"
#define CFG_KEY_TOOL_NAME                    "TOOL_NAME"
#define CFG_KEY_TOOL_DOMAIN                  "TOOL_DOMAIN"
#define CFG_KEY_TOOL_TYPE                    "TOOL_TYPE"
#define CFG_KEY_TOOL_FOR_CHIP_TYPE           "TOOL_FOR_CHIP_TYPE"
#define CFG_KEY_TOOL_FOR_APPLICATION_TYPE    "TOOL_FOR_APPLICATION_TYPE"
#define CFG_KEY_TOOL_BRIEF                   "TOOL_BRIEF"
#define CFG_KEY_TOOL_VERSION                 "TOOL_VERSION"
#define CFG_KEY_UPTATA_DATA                  "UPTATA_DATA"

class VToolInfoEnum:public QObject
{
    Q_OBJECT
public:
    typedef enum
    {
        BLE = 0,
        UWB = 1,
    }enToolDomain;

    typedef enum
    {
        PC = 0,
        APP = 1,
    }enToolType;

    typedef enum
    {
        MXD265X = 0,
        MXD266X = 1,
        MXD267X = 2,
        MXD271X = 3,
    }enToolForChipType;

    typedef enum
    {
        MCU_APPLICATION = 0,
        TEST_APPLICATION = 1,
        APP_APPLICATION = 2,
    }enToolForApplicationType;

    Q_ENUM(enToolDomain)
    Q_ENUM(enToolType)
    Q_ENUM(enToolForChipType)
    Q_ENUM(enToolForApplicationType)
};

typedef enum
{
    installed = 0,
    uninstalled = 1,
}enToolState;


struct stToolInfo
{
    QString toolName;
    VToolInfoEnum::enToolDomain toolDomian;
    VToolInfoEnum::enToolType toolType;
    int toolForChipType;                 //enToolForChipType 枚举值对应bit位置1为支持该芯片类型
    int toolForApplicationType;          //enToolForApplicationType 枚举值对应bit位置1为适用的应用范围
    QString toolBrief;
    QString toolVersion;
    QString toolUpdataData;
};

struct stToolsInfo
{
    enToolState toolState;
};


#endif // BLE_CMD_DEFINE_H
