# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import time
from instrument import _RS_CMW500, _AgilentN5181A_signalgenerator
from datetime import datetime
from HCI import HCI_For_Serial

Configs = _RS_CMW500.Configs


CMW_TCPIP = 'TCPIP::192.168.190.63::INSTR'
SG_TCPIP = 'TCPIP::192.168.190.32::INSTR'
BoardNum = 'DTM_ACI#1'
HCIPort = 'COM5'

# CMW500_set config
Configs.RETRY = 0
Configs.RFOUTPUT = '22.0'
Configs.RFINPUT = '22.0'
Configs.PACKAGELEN = '200'
Configs.RSBAUDRATE = 'B96K'
Pack_num = 200

# 30MHz-6GHz  4 interfere level
# Level0_step = 10
# Level1_step = 3
# Level2_step = 3
# Level3_step = 25

interfere0 = -30
interfere1 = -35
interfere2 = -35
interfere3 = -30


Freq_level0 = np.linspace(30, 2000, 198)
Freq_level1 = np.linspace(2003, 2399, 133)
Freq_level2 = np.linspace(2484, 2997, 172)
Freq_level3 = np.linspace(3000, 6000, 121)


Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                 30, 31, 32, 33, 34, 35, 36, 37, 38, 39)


def blocking_get_data(self, device, CH, test_mode):
    rfmode = test_mode
    if (test_mode == 3):
        rfmode = 4
    elif (test_mode == 4):
        rfmode = 3
    device.HCI_rf_rx_test(self=device, channel=CH, test_mode=rfmode)
    self.per_search_channel(self=self, CH=CH)
    self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER ')
    self.aci_data_querry(self=self)
    num = device.HCI_rf_rx_end(self=device)
    per = (Pack_num-num)*100/Pack_num
    return per


def blocking_level_data(self, CH, freq_map, device, signal, power, test_mode):
    Result = np.matrix(np.zeros(len(freq_map) * len(CH)
                                ).reshape(len(freq_map), len(CH)))
    self.per_search_channel(self=self, CH=CH)
    for Channel in range(len(CH)):
        for freq in range(len(freq_map)):
            signal.set_output_para(
                self=signal, FreqMHz=freq_map[freq], PowerDBM=power)
            signal.instr_output_on(self=signal)
            per = blocking_get_data(
                self=self, device=device, CH=CH[Channel], test_mode=test_mode)
            Result[freq, Channel] = per

    return Result


def blocking_test(self, CH, device, signal, test_mode=[_RS_CMW500.DTM_test_mode]):
    self.per_search_mode(self=self, test_mode=test_mode)

    Result_Level0 = blocking_level_data(self=self, CH=CH, level_map=Freq_level0,
                                        device=device, signal=signal, power=interfere0, test_mode=test_mode)

    Result_Level1 = blocking_level_data(self=self, CH=CH, level_map=Freq_level1, device=device, signal=signal,
                                        power=interfere1, test_mode=test_mode)

    Result_Level2 = blocking_level_data(self=self, CH=CH, level_map=Freq_level2, device=device, signal=signal,
                                        power=interfere2, test_mode=test_mode)

    Result_Level3 = blocking_level_data(self=self, CH=CH, level_map=Freq_level3, device=device, signal=signal,
                                        power=interfere3, test_mode=test_mode)

    Result_ALL = [Result_Level0, Result_Level1, Result_Level2, Result_Level3]
    return Result_ALL


def Blocking_write_data(data, writer, name):
    data0 = pd.DataFrame(data[0])
    data0.to_excel(writer, 'ACI_Level0_' + name, float_format='%.2f')
    data1 = pd.DataFrame(data[1])
    data1.to_excel(writer, 'ACI_Level1_' + name, float_format='%.2f')
    data2 = pd.DataFrame(data[2])
    data2.to_excel(writer, 'ACI_Level2_' + name, float_format='%.2f')
    data3 = pd.DataFrame(data[3])
    data3.to_excel(writer, 'ACI_Level3_' + name, float_format='%.2f')


def Blocking_test_all(self, CH, writer, device, signal):
    Result_1M = blocking_test(self=self, CH=CH, device=device,
                              signal=signal, test_mode=_RS_CMW500.DTM_test_mode.LE1M)
    self.stop_per(self=self)
    Blocking_write_data(data=Result_1M, writer=writer, name='1M')
    Result_2M = blocking_test(self=self, CH=CH, device=device,
                              signal=signal, test_mode=_RS_CMW500.DTM_test_mode.LE2M)
    self.hci_aci_stop(self=self)
    Blocking_write_data(data=Result_2M, writer=writer, name='2M')


if __name__ == "__main__":
    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)

    SG = _AgilentN5181A_signalgenerator.Signalgenerator
    SG.instr_init(self=SG, TCPIP=SG_TCPIP)

    SG.set_output_para(self=SG, FreqMHz=2402, PowerDBM=0)
    SG.instr_output_on(self=SG)

    print('Test start.')
    RCMW500 = _RS_CMW500.RS_CMW500
    RCMW500.__init__(self=RCMW500)
    RCMW500.CMW500_connect(self=RCMW500, TCPIP=CMW_TCPIP)

    OUTPUT_path = 'D:\\DTM_ACI\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime(
            'DTM_ACI' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    Blocking_test_all(self=RCMW500, CH=Channel_range,
                      writer=writer, device=MXD2670, signal=SG)

    RCMW500.stop_per(self=RCMW500)

    writer.save()
    writer.close()
