# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import time
from instrument import _RS_CMW500
from datetime import datetime
from HCI import HCI_For_Serial

Configs = _RS_CMW500.Configs


CMW_TCPIP = 'TCPIP::192.168.190.63::INSTR'
BoardNum = 'DTM_ACI#1'
HCIPort = 'COM5'

#CMW500_set config
Configs.RETRY = 0
Configs.RFOUTPUT = '22.0'
Configs.RFINPUT = '22.0'
Configs.PACKAGELEN = '200'
Configs.RSBAUDRATE = 'B96K'

Pack_num = 200

ACi_channel = (3,15,37)


def aci_mode_get_data(self,device, CH, test_mode ):
    rfmode = test_mode
    if (test_mode == 3):
        rfmode = 4
    elif (test_mode == 4):
        rfmode = 3
    device.HCI_rf_rx_test(self=device, channel=CH, test_mode=rfmode)
    self.cmd_send(self=self, cmd='INIT:BLU:SIGN:RXQ:PER ')
    self.aci_data_querry(self=self)
    num = device.HCI_rf_rx_end(self=device)
    per = (Pack_num-num)*100/Pack_num
    return per



def dtm_aci_test(self, CH, device,test_mode=[_RS_CMW500.DTM_test_mode]):
    Result_IntPwr1 = np.array(np.zeros(len(CH)))
    Result_IntPwr2 = np.array(np.zeros(len(CH)))
    Result_IntPwr3 = np.array(np.zeros(len(CH)))
    Result_IntPwr4 = np.array(np.zeros(len(CH)))
    Result_IntPwr5 = np.array(np.zeros(len(CH)))
    Result_IntPwr6 = np.array(np.zeros(len(CH)))
    Result_IntPwr7 = np.array(np.zeros(len(CH)))
    Result_IntPwr8 = np.array(np.zeros(len(CH)))
    Result_IntPwr9 = np.array(np.zeros(len(CH)))
    Result_IntPwr10 = np.array(np.zeros(len(CH)))
    Result_IntPwr11 = np.array(np.zeros(len(CH)))
    Result_IntPwr12 = np.array(np.zeros(len(CH)))
    Result_IntPwr13 = np.array(np.zeros(len(CH)))

    self.hci_aci_mode(self=self, test_mode=test_mode)
    Per = 0
    band_range = np.linspace(-6, 6, 13)
    IntPwr_range = [-40, -50, -70, -60, -65, -70, -70, -70, -70, -65, -60, -40, -30]
    for channel in range(len(CH)):
        self.hci_aci_channel(self=self, CH=CH[channel])
        freq = 2402 + CH[channel] * 2
        temp_result = np.array(np.zeros(len(band_range)))
        for bd in band_range:
            IntPwr = IntPwr_range[int(bd) + 6]
            if(test_mode==2):
                freq_intpwr = freq + bd*2
            else:
                freq_intpwr = freq + bd
            self.hci_aci_interferer_freq(self=self, freqMHz=freq_intpwr)
            while (30.8 - Per) > 0:
                self.hci_aci_interferer_level(self=self, level=IntPwr)
                Per = aci_mode_get_data(self=self, device=device, CH=CH[channel], test_mode=test_mode)
                IntPwr = IntPwr + Configs.ACI_STEP
            Per = 0
            IntPwr = IntPwr - Configs.ACI_STEP
            temp_result[int(bd + 6)] = Configs.ACI_EMAGE_PW - IntPwr + Configs.ACI_LOSS
        # Total 13 value in each CH
        Result_IntPwr1[channel] = temp_result[0]
        Result_IntPwr2[channel] = temp_result[1]
        Result_IntPwr3[channel] = temp_result[2]
        Result_IntPwr4[channel] = temp_result[3]
        Result_IntPwr5[channel] = temp_result[4]
        Result_IntPwr6[channel] = temp_result[5]
        Result_IntPwr7[channel] = temp_result[6]
        Result_IntPwr8[channel] = temp_result[7]
        Result_IntPwr9[channel] = temp_result[8]
        Result_IntPwr10[channel] = temp_result[9]
        Result_IntPwr11[channel] = temp_result[10]
        Result_IntPwr12[channel] = temp_result[11]
        Result_IntPwr13[channel] = temp_result[12]

    Result = [Result_IntPwr1, Result_IntPwr2, Result_IntPwr3, Result_IntPwr4, Result_IntPwr5, Result_IntPwr6,
              Result_IntPwr7, Result_IntPwr8, Result_IntPwr9, Result_IntPwr10, Result_IntPwr11, Result_IntPwr12,
              Result_IntPwr13]
    return Result

def Aci_write_data(data, writer, name):
    Base_freq = np.array(np.ones(len(ACi_channel))*2402)
    Freq_index = Base_freq + np.array(ACi_channel)*2
    RESULT_FREQ_INDEX = {'Freq (MHz)' : Freq_index}
    RESULT_ACI1 = {'IntPwr1': data[0]}
    RESULT_ACI2 = {'IntPwr2': data[1]}
    RESULT_ACI3 = {'IntPwr3': data[2]}
    RESULT_ACI4 = {'IntPwr4': data[3]}
    RESULT_ACI5 = {'IntPwr5': data[4]}
    RESULT_ACI6 = {'IntPwr6': data[5]}
    RESULT_ACI7 = {'IntPwr7': data[6]}
    RESULT_ACI8 = {'IntPwr8': data[7]}
    RESULT_ACI9 = {'IntPwr9': data[8]}
    RESULT_ACI10 = {'IntPwr10': data[9]}
    RESULT_ACI11 = {'IntPwr11': data[10]}
    RESULT_ACI12 = {'IntPwr12': data[11]}
    RESULT_ACI13 = {'IntPwr13': data[12]}
    RESULT_ACI_ALL = dict(**RESULT_FREQ_INDEX, **RESULT_ACI1, **RESULT_ACI2, **RESULT_ACI3, **RESULT_ACI4, **RESULT_ACI5,
                          **RESULT_ACI6, **RESULT_ACI7, **RESULT_ACI8, **RESULT_ACI9, **RESULT_ACI10, **RESULT_ACI11,
                          **RESULT_ACI12, **RESULT_ACI13)
    data = pd.DataFrame(RESULT_ACI_ALL)  # )#
    data.to_excel(writer, 'ACI_test in '+name, float_format='%.2f')  # ‘page_1’是


def Aci_test_all(self,CH, writer ,device):
    Result_1M = dtm_aci_test(self=self, CH=CH, device=device, test_mode=_RS_CMW500.DTM_test_mode.LE1M)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_1M, writer=writer, name='1M')
    Result_2M = dtm_aci_test(self=self, CH=CH, device=device, test_mode=_RS_CMW500.DTM_test_mode.LE2M)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_2M, writer=writer, name='2M')
    Result_S2 = dtm_aci_test(self=self, CH=CH, device=device, test_mode=_RS_CMW500.DTM_test_mode.LES2)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_S2, writer=writer, name='S2')
    Result_S8 = dtm_aci_test(self=self, CH=CH, device=device, test_mode=_RS_CMW500.DTM_test_mode.LES8)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_S8, writer=writer, name='S8')

if __name__ == "__main__":
    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)

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

    Aci_test_all(self=RCMW500, CH=ACi_channel, writer=writer, device=MXD2670)

    RCMW500.stop_per(self=RCMW500)

    writer.save()
    writer.close()
