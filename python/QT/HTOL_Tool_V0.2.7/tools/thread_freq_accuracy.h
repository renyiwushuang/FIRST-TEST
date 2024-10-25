#ifndef THREAD_FREQ_ACCURACY_H
#define THREAD_FREQ_ACCURACY_H

#include <QString>
#include <QThread>
#include <QMutex>
#include "Intermediate_communication_protocol/test_ctlr_procotol.h"

/*烧录器频偏校准指令下的操作*/
typedef enum
{
    Freq_single_tone    = 0x01,
    Freq_cap_save       = 0x02
}EN_FREQ_ACCURACY_T;


//自动校准流程状态机
enum ADJUST_STATE{
    STA_FRE_INITIAL = 0,  //初始化频谱仪配置(配置中心频率、SPAN)
    STA_FRE_INIREAD = 1,  //读取频谱仪最初的Y值,作为后面判定是否PEAK OK的标准
    STA_SERL_DANYIN = 2,  //发射单音信号,频谱仪进行无线耦合
    STA_FRE_PEAK = 3,     //频谱仪PEAK SEARCH
    STA_FRE_CHANGE_SPAN = 4,  //频谱仪改变SPAN进行细调
    STA_FRE_GETX = 5,     //获取频谱仪当前频率
    STA_SERL_SET_CAT = 6, //根据频偏计算并设置cat值,发送单音信号再次调整直到<1k
    STA_SERL_READ_CAT = 7,//读取cat值
    STA_SERL_SAVE_CAT = 8,//保存cat值,并确认单音是否关闭 退出校准
    STA_ADJUST_END = 9, //校准结束
};

class thread_freq_accuracy : public QThread
{
    Q_OBJECT
public:
    explicit thread_freq_accuracy(QThread *parent = 0);

    void set_serial_response_flag(int cmd);

private:
    QMutex m_lock;
    bool m_isRun;

    float y_init;//底噪值
    uint span_set;
    double x_current,y_current; //实时的y值
    QString x_str,y_str;
    QString str_send;
    bool span_change_flag;//span改变标志
    uint16_t cat_value;
    bool cat_set_first_flag;//第一次设置电容值
    int offset; //存储偏差值
    ADJUST_STATE adjust_sta_t;

    bool send_signal_tone_flag;
    bool read_cap_value_flag;
    bool write_cap_value_flag;
    bool save_cap_value_flag;

public:
    void stop_immediately();
    void run();//任务处理线程

signals:
    void sigl_tcp_send_control_cmd(QString);     //信号:通知UI线程发送TCP数据
    void sigl_serial_send_cmd(uint8_t, uint16_t);  //信号:通知UI线程发送串口命令
    void sigl_stop_freq_thread();        //信号通知UI停止该线程
    void sigl_display_freq_accuracy_log(QString);  //信号通知UI输出校准log
    void sigl_set_process_value(int);     //信号通知UI设置进度条
    void sigl_display_warnning(QString); //信号通知UI显示警告信息
};

#endif // THREAD_FREQ_ACCURACY_H
