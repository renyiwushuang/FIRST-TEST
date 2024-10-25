#include "thread_freq_accuracy.h"

#define FREQ_CENTER_HZ   7987200000.000000       //中心频率 7987200000 hz
#define FREQ_OFFSET_STD  1000                    //频偏标准范围
#define PEAK_STAND       25                      //峰值标准差

extern stTestCtrlProcotolInfo_t g_stTestReturnInfo;//芯片端回包数据

QByteArray g_RecvDataFreqSpecTcp;     //TCP接收数据缓存区


/**************************************************************************************************
* @brief  : thread_freq_accuracy
* @param  : QThread
* @return : none
* @note   : thread_freq_accuracy类初始化主函数
***************************************************************************************************/
thread_freq_accuracy::thread_freq_accuracy(QThread *parent)
    :QThread(parent)
{
    m_isRun = true;
    span_set = 0;
    y_init = 0.0;
    y_current = 0.00;
    x_current = 0.00;
    span_change_flag = false;
    cat_value = 0x3f;
    cat_set_first_flag = true;
    offset = 0;
    adjust_sta_t = STA_FRE_INITIAL;

    qRegisterMetaType<uint8_t>("uint8_t");
    qRegisterMetaType<uint16_t>("uint16_t");

}

void thread_freq_accuracy::set_serial_response_flag(int cmd)
{
    switch(cmd){
    case Freq_single_tone:
        send_signal_tone_flag = true;break;
    case Freq_cap_save:
        save_cap_value_flag = true;break;
    default:break;
    }
}

/**************************************************************************************************
* @brief  : stop_immediately
* @param  : none
* @return : none
* @note   : 线程锁(守护线程)
***************************************************************************************************/
void thread_freq_accuracy::stop_immediately()
{
    QMutexLocker locker(&m_lock);
    m_isRun = false;
}

/**************************************************************************************************
* @brief  : run
* @param  : none
* @return : none
* @note   : 线程执行函数（频偏校准状态机）
***************************************************************************************************/
void thread_freq_accuracy::run()
{
    enum ADJUST_STATE tmp_sta = STA_FRE_INITIAL;
    uint8_t timeout = 0;
    uint8_t num_err = 0;


    span_change_flag = false;
    cat_value = 0x80;
    cat_set_first_flag = true;
    adjust_sta_t = STA_FRE_INITIAL;

    while(1)
    {
        switch (adjust_sta_t) {
        /* 初始化配置 */
        case STA_FRE_INITIAL:
            qDebug("第0步: 初始化配置频谱仪参数");
            emit sigl_display_warnning(tr("【 Initial configuration spectrometer parameters 】"));
            emit sigl_display_freq_accuracy_log("[0: STA_FRE_INITIAL]");
            emit sigl_tcp_send_control_cmd("SENSe:FREQuency:CENT 7987.2 MHz");//设置频谱仪中心频率:7987.2M
            msleep(20);
            emit sigl_tcp_send_control_cmd("SENSe:FREQuency:SPAN 1 MHz");//设置频谱仪初始SPAN:1 MHz
            msleep(100);
            emit sigl_tcp_send_control_cmd("AVER ON");
            msleep(1000);//1s取平均
            emit sigl_serial_send_cmd(Freq_single_tone, cat_value);
            adjust_sta_t = STA_FRE_INIREAD;
            break;

        /* 读取底噪 */
        case STA_FRE_INIREAD:
            qDebug("第1步: 读取频谱仪底噪");
            emit sigl_display_freq_accuracy_log("[1: STA_FRE_INIREAD]");
            emit sigl_tcp_send_control_cmd("CALC:MARK:MAX");
            msleep(100);
            emit sigl_tcp_send_control_cmd(":CALC:MARK:Y?");
            msleep(300);//延时等待接收,此处至少200ms   //休眠等待信号
            y_str = QString::number(g_RecvDataFreqSpecTcp.toFloat(), 'f', 3);
            emit sigl_display_freq_accuracy_log("y_init:" + y_str);
            y_init = y_str.toFloat();//得到底噪值,作为后面判定是否PEAK OK的标准
            qDebug("  底噪: %f", y_init);
            emit sigl_tcp_send_control_cmd("AVER OFF");
            msleep(20);
            adjust_sta_t = STA_SERL_DANYIN;
            break;

        /* 发送单音信号 */
        case STA_SERL_DANYIN:
            qDebug("第2步: 串口发送单音信号");
            emit sigl_display_freq_accuracy_log("[2: STA_SERL_DANYIN]");
            send_signal_tone_flag = false;
            emit sigl_serial_send_cmd(Freq_single_tone, cat_value);//下发单音信号
            msleep(1000);//延时等待接收,串口最好等待>=300ms稳定
            if(g_stTestReturnInfo.testDataResult[0] == 0)
            { //单音发送反馈ok
                adjust_sta_t = STA_FRE_PEAK ;//STA_FRE_PEAK
            }else{
                adjust_sta_t = STA_SERL_DANYIN;
                num_err++;
                if(num_err>=3){
                    emit sigl_display_warnning(tr("【 Please reinsert 】"));
                    num_err = 0;
                }
            }
            adjust_sta_t = STA_FRE_PEAK ;//STA_FRE_PEAK
            break;

        /* 获取峰值 */
        case STA_FRE_PEAK:
            qDebug("第3步: 获取频谱仪峰值");
            emit sigl_display_freq_accuracy_log("[3: STA_FRE_PEAK]");
            emit sigl_tcp_send_control_cmd("CALC:MARK:MAX");
            msleep(100);
            emit sigl_tcp_send_control_cmd(":CALC:MARK:Y?");
            msleep(300);
            y_str = QString::number(g_RecvDataFreqSpecTcp.toFloat(), 'f', 3);
            emit sigl_display_freq_accuracy_log("y_peak:" + y_str);
            y_current = y_str.toFloat();//获取当前峰值
            qDebug("  peak: %f", y_current);
            if((y_current-y_init)>PEAK_STAND || (y_current-y_init)<1)//认定此时获取到peak
            {
                emit sigl_display_warnning("【PEAK OK】");
                adjust_sta_t = STA_FRE_GETX;
                break;
            }
            else //未获取到峰值,重新发送单音
            {
                timeout ++;
                msleep(20);
                tmp_sta = adjust_sta_t;
                if(timeout>=3){  //超过三次都没获取到峰值,则重新读取底噪
                    timeout = 0;
                    emit sigl_display_warnning(tr("【 Please approach the antenna!!】"));
                    //adjust_sta_t = STA_FRE_INIREAD;
                }else{
                    //adjust_sta_t = STA_SERL_DANYIN;
                }
                adjust_sta_t = STA_SERL_DANYIN;
                break;
            }

        /* 调整SPAN */
        case STA_FRE_CHANGE_SPAN:
            msleep(1000);
            qDebug("第4步: 调整频谱仪SPAN");
            emit sigl_display_freq_accuracy_log("[4: STA_FRE_CHANGE_SPAN]");
            qDebug("  当前偏差: %d",offset);
            emit sigl_display_freq_accuracy_log(tr("【 Narrow the SPAN range 】"));
            if(qAbs(offset)>=25000){ //±25k
                qDebug("  设置SPAN: %d khz",qAbs(offset)*2/1000+10);
                QString str = QString("SENSe:FREQuency:SPAN %1 KHz").arg(qAbs(offset)*2/1000+10);
                emit sigl_tcp_send_control_cmd(str);
            }else{
                qDebug(" 设置SPAN: %d khz",50);
                QString str = QString("SENSe:FREQuency:SPAN %1 KHz").arg(qAbs(offset)*2/1000+30);
                emit sigl_tcp_send_control_cmd(str);
                span_change_flag = true;
            }

            msleep(100);
            tmp_sta = adjust_sta_t;
            adjust_sta_t = STA_FRE_PEAK;//调整SPAN后继续获取峰值
            break;

        /* 获取频率 */
        case STA_FRE_GETX:
            qDebug("第5步: 获取频谱仪频率");
            msleep(10);//10s
            emit sigl_display_freq_accuracy_log("[5: STA_FRE_GETX]");
            msleep(10);
            emit sigl_tcp_send_control_cmd("CALC:MARK:MAX");
            msleep(10);
            emit sigl_tcp_send_control_cmd("CALC:MARK:MAX");
            msleep(300);
            emit sigl_tcp_send_control_cmd(":CALC:MARK:X?");
            msleep(1000);//300
            x_str = QString::number(g_RecvDataFreqSpecTcp.toFloat(), 'f', 0);
//            qDebug("xstr: ", x_str);
            emit sigl_display_freq_accuracy_log(tr("Spectrometer frequency:") + x_str);
            x_current = x_str.toULong(nullptr, 10);
            offset = x_current-FREQ_CENTER_HZ;
            qDebug("  获取频率: %f, 当前偏差: %d",x_current, offset);
            emit sigl_display_freq_accuracy_log(QString(tr("Frequency deviation:%1")).arg(offset));

            msleep(300);

            adjust_sta_t = STA_SERL_SET_CAT;
            break;

        /* 设置电容值 */
        case STA_SERL_SET_CAT:
            qDebug("第6步: 串口设置CAT");
            emit sigl_display_freq_accuracy_log("[6: STA_SERL_SET_CAT]");
            if(qAbs(offset)>=FREQ_OFFSET_STD)
            {
                if(offset > 0) //频偏偏大
                {
                    cat_value += 1;
                }
                else //频偏偏小
                {
                    cat_value -= 1;
                }
                emit sigl_serial_send_cmd(Freq_single_tone, cat_value);//设置电容值
                msleep(300);
                if(g_stTestReturnInfo.testDataResult[0] == 0)
                { //反馈ok
                    tmp_sta = adjust_sta_t;
                    if(!span_change_flag){ //未调整SPAN
                        adjust_sta_t = STA_FRE_CHANGE_SPAN;
                    }else{
                        adjust_sta_t = STA_FRE_GETX; //重新获取峰值 STA_FRE_PEAK
                    }
                    break;
                }else{
                    break;
                }
            }
            else
            {
                qDebug("  偏差<1k,改变SPAN再次读取");
                if(!span_change_flag){ //未调整SPAN
                    adjust_sta_t = STA_FRE_CHANGE_SPAN;
                }else{ //已调整好SPAN
                        adjust_sta_t = STA_SERL_SAVE_CAT;
                }
                break;
            }

        /* 保存电容值 */
        case STA_SERL_SAVE_CAT:
            qDebug("第8步: 串口保存CAT");
            emit sigl_display_freq_accuracy_log("[8: STA_SERL_SAVE_CAT]");
            qDebug("  保存cat: %02x, 当前频偏: %d",cat_value, offset);
            emit sigl_display_freq_accuracy_log(QString(tr("Current frequency offset:%1")).arg(offset) + QString(tr("Capacitance Value:%1")).arg(cat_value));
            emit sigl_serial_send_cmd(Freq_cap_save, cat_value);//保存CAT
            msleep(300);
            if(g_stTestReturnInfo.testDataResult[0] == 0)
            { //反馈ok
                adjust_sta_t = STA_ADJUST_END;
                break;
            }else{
                break;
            }

        /* 校准结束 */
        case STA_ADJUST_END:
            qDebug("第9步: 校准结束");
            msleep(10);
            emit sigl_set_process_value(STA_ADJUST_END);
            emit sigl_display_warnning(tr("【Calibration completed】"));
            emit sigl_stop_freq_thread();
            return; //校准完成,退出

        default:
            break;
        }
        emit sigl_set_process_value(adjust_sta_t>tmp_sta?adjust_sta_t:tmp_sta);
    }
}


