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

Test_Channle = 20
Start_level = -30
End_level = -110
Test_gap = 1
Send_package = 1500
Level_range = np.linspace(End_level,Start_level,81)
CMW_TCPIP = 'TCPIP::192.168.190.63::INSTR'
BoardNum = '#2屏蔽箱_NOWIFI'
HCIPort = 'COM5'

class ResultDef:
    Packnum_1M = np.array(np.zeros(len(Level_range)))

class DTM_test_mode:
    LE1M = 1
    LE2M = 2
    LES2 = 3
    LES8 = 4

class RfTestModeDef:
    LE1M = 1
    LE2M = 2
    LES2 = 4
    LES8 = 3


class PayloadTypeDef:
    PRBS9 = 0
    HALF10 = 1
    MIX10 = 2
    PRBS15 = 3
    ALL1 = 4
    ALL0 = 5
    HALF01 = 6
    MIX01 = 7

class RegAcgModeDef:
    AUTO = 0
    GAIN0 = 1
    GAIN1 = 3
    GAIN2 = 5

def get_per_data( self, device, CH, mode, rfmode):
    result = np.array(np.zeros(len(Level_range)))
    self.per_search_mode(self=self, test_mode=mode)
    self.per_search_channel(self=self, CH=CH )
    position = 0
    err_num=0
    for level in Level_range:
        device.HCI_rf_rx_test(self=device, channel=CH, test_mode=rfmode)
        time.sleep(0.05)
        # self.per_send_only(self=self, level=level)
        self.per_send_only(self=self, level=level)
        num = device.HCI_rf_rx_end(self=device)
        err_num = Send_package-num
        print('err_num is ' + str(err_num))
        result[position] = err_num
        position = position+1
        time.sleep(0.05)
    return result

if __name__ == "__main__":

    print('Test start.')
    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)

while 1:
    MXD2670.HCI_rf_rx_end(self=MXD2670)
    MXD2670.HCI_rf_rx_test(self=MXD2670,channel=25, test_mode=RfTestModeDef.LE2M)
    a = MXD2670.HCI_rssi_read(self=MXD2670)
    b = MXD2670.HCI_rssi_read_dbm(self=MXD2670)
    c0 = MXD2670.HCI_rssi_agc0_read(self=MXD2670)
    c1 = MXD2670.HCI_rssi_agc1_read(self=MXD2670)
    c2 = MXD2670.HCI_rssi_agc2_read(self=MXD2670)
    d = MXD2670.HCI_power_ant_sub_val_read(self=MXD2670)
    e = MXD2670.HCI_rssi_2_bit_read(self=MXD2670)
    print('Rssi='+str(a[0])+'   '+'Agc='+str(a[0])+'   '+'Rssi_db'+str(b)+'   '+'Rssi_2_bit'+str(e))
    print('rssi_agc0='+ str(c0)+'   '+'rssi_agc1='+ str(c1)+'   '+'rssi_agc2='+ str(c2) +'   '+'power_ant='+str(d))
    time.sleep(0.05)


    # RCMW500.stop_per(self=RCMW500)
    # time.sleep(0.1)
    # Packnum_2M = get_per_data(self=RCMW500, device=MXD2670, CH=Test_Channle, mode=DTM_test_mode.LE2M, rfmode=RfTestModeDef.LE2M)
    # RCMW500.stop_per(self=RCMW500)
    # time.sleep(0.1)
    # Packnum_S2 = get_per_data(self=RCMW500, device=MXD2670, CH=Test_Channle, mode=DTM_test_mode.LES2, rfmode=RfTestModeDef.LES2)
    # RCMW500.stop_per(self=RCMW500)
    # time.sleep(0.1)
    # Packnum_S8 = get_per_data(self=RCMW500, device=MXD2670, CH=Test_Channle, mode=DTM_test_mode.LES8, rfmode=RfTestModeDef.LES8)
    # RCMW500.stop_per(self=RCMW500)
    # time.sleep(0.1)
    #
    #     writer = pd.ExcelWriter(
    #         OUTPUT_path + datetime.now().strftime(
    #             'DTM_GAIN_MODE_'+str(reg_mode) + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)
    #     WRITER_DATA_INDEX = {'Level\n(dBm)': Level_range}
    #     WRITER_DATA_1M= {'Package nuber @1M': Packnum_1M/all_num}
    #     WRITER_DATA_2M= {'Package nuber @2M': Packnum_2M/all_num}
    #     WRITER_DATA_S2 = {'Package nuber @S2': Packnum_S2/all_num}
    #     WRITER_DATA_S8 = {'Package nuber @S8': Packnum_S8/all_num}
    #
    #     ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_1M, **WRITER_DATA_2M, **WRITER_DATA_S2, **WRITER_DATA_S8)
    #     result_data = pd.DataFrame(ALL_DATA)
    #     result_data.to_excel(writer, 'Gain mode test', float_format='%.5f')
    #     writer.save()
    #     writer.close()

print('Test end')

    
    