#include "qt_custom_label.h"


/*******************************************************************************
 *  该函数将label控件变成一个圆形指示灯，需要指定颜色color以及直径size
 *  color 0:grey 1:red 2:green 3:yellow
 *  size  单位是像素
 *******************************************************************************/
uint8_t set_led(QLabel* label, int color, int size)
{
    label->setText("");     // 将label中的文字清空

    // 设置矩形大小
    // 如果ui界面设置的label大小比最小宽度和高度小，矩形将被设置为最小宽度和最小高度；
    // 如果ui界面设置的label大小比最小宽度和高度大，矩形将被设置为最大宽度和最大高度；
    QString min_width = QString("min-width: %1px;").arg(size);              // 最小宽度：size
    QString min_height = QString("min-height: %1px;").arg(size);            // 最小高度：size
    QString max_width = QString("max-width: %1px;").arg(size);              // 最小宽度：size
    QString max_height = QString("max-height: %1px;").arg(size);            // 最小高度：size

    // 设置边界形状及边框
    QString border_radius = QString("border-radius: %1px;").arg(size/2);    // 边框是圆角，半径为size/2
    QString border = QString("border:1px solid black;");                    // 边框为1px黑色

    // 设置背景颜色
    QString background = "background-color:";
    switch (color) {
    case 0: 
        background += "rgb(190,190,190)";// 灰色
        break;
    case 1:  
        background += "rgb(255,0,0)";// 红色
        break;
    case 2: 
        background += "rgb(0,255,0)";// 绿色
        break;
    case 3:
        background += "rgb(255,255,0)";// 黄色
        break;
    default:
        break;
    }

    const QString SheetStyle = min_width + min_height + max_width + max_height + border_radius + border + background;
    label->setStyleSheet(SheetStyle);

    return 1;
}

