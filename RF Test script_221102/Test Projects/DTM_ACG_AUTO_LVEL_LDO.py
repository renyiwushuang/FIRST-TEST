# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import time
import copy
from instrument import _RS_CMW500
from datetime import datetime
from HCI import HCI_For_Serial

Configs = _RS_CMW500.Configs

Test_Channle = 20
Start_level = -30
End_level = -110
Test_gap = 1
Send_package = 1500
Level_range = np.linspace(End_level, Start_level, 81)
CMW_TCPIP = 'TCPIP::192.168.190.63::INSTR'
BoardNum = '#2'
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


class Result_acg:
    result = np.array(np.zeros(len(Level_range)))
    rssi = np.array(np.zeros(len(Level_range)))
    acg = np.array(np.zeros(len(Level_range)))
    rssi_db = np.array(np.zeros(len(Level_range)))


def get_per_data(self, device, CH, mode, rfmode):

    result = np.array(np.zeros(len(Level_range)))
    rssi = np.array(np.zeros(len(Level_range)))
    acg = np.array(np.zeros(len(Level_range)))
    rssi_db = np.array(np.zeros(len(Level_range)))

    self.per_search_mode(self=self, test_mode=mode)
    self.per_search_channel(self=self, CH=CH)
    position = 0
    err_num = 0
    for level in Level_range:
        device.HCI_rf_rx_test(self=device, channel=CH, test_mode=rfmode)
        time.sleep(0.05)
        self.per_send_only(self=self, level=level)
        num = device.HCI_rf_rx_end(self=device)
        err_num = Send_package - num
        print('err_num is ' + str(err_num))
        result[position] = err_num
        temp_rssi = device.HCI_rssi_read(self=device)
        temp_rssi_db = device.HCI_rssi_read_dbm(self=device)
        if (num == 0):
            rssi[position] = 0
            rssi_db[position] = 0
        else:
            rssi[position] = temp_rssi[0]
            rssi_db[position] = temp_rssi_db
        acg[position] = temp_rssi[1]
        position = position + 1
        time.sleep(0.05)
    return_data = [result,rssi,acg,rssi_db]
    return return_data


if __name__ == "__main__":

    LDO_range = [HCI_For_Serial.LdoRfDef.LDO_RF_850mV, HCI_For_Serial.LdoRfDef.LDO_RF_900mV, HCI_For_Serial.LdoRfDef.LDO_RF_950mV,
                 HCI_For_Serial.LdoRfDef.LDO_RF_1000mV, HCI_For_Serial.LdoRfDef.LDO_RF_1050mV, HCI_For_Serial.LdoRfDef.LDO_RF_1100mV,
                 HCI_For_Serial.LdoRfDef.LDO_RF_1150mV, HCI_For_Serial.LdoRfDef.LDO_RF_1200mV]

    #Channel20 = 22.8db
    Configs.RSBAUDRATE = 'B96K'
    Configs.RFOUTPUT = '22.8'
    Configs.RFINPUT = '22.8'
    Configs.PACKAGELEN = '1500'

    print('Test start.')
    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)

    all_num = np.array(np.ones(len(Level_range)) * Send_package / 100)

    RCMW500 = _RS_CMW500.RS_CMW500
    RCMW500.__init__(self=RCMW500)
    RCMW500.CMW500_connect(self=RCMW500, TCPIP=CMW_TCPIP)

    OUTPUT_path = 'D:\\DTM_GAIN\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'

    DTM_mode = [DTM_test_mode.LE1M, DTM_test_mode.LE2M, DTM_test_mode.LES2, DTM_test_mode.LES8]
    # DTM_mode = [ DTM_test_mode.LES2, DTM_test_mode.LES8 ]

    for LDO in LDO_range:
        MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=LDO)
        for DTM in DTM_mode:
            RFmode = DTM
            if (DTM == 3):
                RFmode = 4
            elif (DTM == 4):
                RFmode = 3

            if (DTM == 1):
                name = '1M'
            elif (DTM == 2):
                name = '2M'
            elif (DTM == 4):
                name = 'S8'
            else:
                name = 'S2'
            time.sleep(0.1)
            MXD2670.HCI_reg_acg_mode(self=MXD2670, AcgMode=RegAcgModeDef.AUTO)
            time.sleep(0.1)
            Packnum_1M_AUTO = get_per_data(self=RCMW500, device=MXD2670, CH=Test_Channle, mode=DTM, rfmode=RFmode)
            RCMW500.stop_per(self=RCMW500)

            writer = pd.ExcelWriter(
                OUTPUT_path + datetime.now().strftime(
                    'DTM_AUTO_GAIN_CH20_LDO_'+str(LDO) +'_' + name + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

            # return_data = [result, rssi, acg, rssi_db]
            WRITER_DATA_INDEX = {'Level\n(dBm)': Level_range}
            WRITER_DATA_AUTO = {'Gain AUTO (Err per)': Packnum_1M_AUTO[0] / all_num}
            WRITER_DATA_RSSI_AUTO = {'Gain AUTO RSSI': Packnum_1M_AUTO[1]}
            WRITER_DATA_RSSIDB_AUTO = {'Gain AUTO RSSI (dB)': Packnum_1M_AUTO[3]}
            WRITER_DATA_ACG_AUTO = {'Gain AUTO AGC': Packnum_1M_AUTO[2]}

            ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_AUTO, **WRITER_DATA_RSSI_AUTO, **WRITER_DATA_RSSIDB_AUTO,
                            **WRITER_DATA_ACG_AUTO)


            result_data = pd.DataFrame(ALL_DATA)
            result_data.to_excel(writer, 'Gain mode test' + name, float_format='%.5f')
            writer.save()
            writer.close()



    print('Test end')