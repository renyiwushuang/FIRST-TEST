# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import time
from datetime import datetime
from HCI import HCI_For_Serial

HCIPort = 'COM5'

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

class TxPowerDef:
    TX_NEG20_DBM = 0
    TX_NEG5_DBM = 1
    TX_0_DBM = 2
    TX_5_DBM = 3
    TX_7_DBM = 4
    TX_10_DBM = 5


if __name__ == "__main__":
    
    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)

    channel = 25
    ChFreqMHz = 2402 + channel*2

    # 1 = single tone , 0 = normal work
    single_tone = 0
    # set Acw  1=10db , 0 = 0db
    Rf_10db = 1

    # Rf_mode = HCI_For_Serial.RfTestModeDef.LE1M
    # LDO_RF = HCI_For_Serial.LdoRfDef.LDO_RF_1200mV
    # LDO_ACT = HCI_For_Serial.LdoActDef.LDO_ACT_1200mV
    #
    # if(Rf_10db):
    #     Power_set = HCI_For_Serial.TxPowerDef.TX_10_DBM
    #     Acw_Val = 235
    #     MXD2670.HCI_pa_mode_config(self=MXD2670, Pa_mode=HCI_For_Serial.TxPaModeDef.VMD_mode)
    # else:
    #     Power_set = HCI_For_Serial.TxPowerDef.TX_0_DBM
    #     Acw_Val = 255
    #     MXD2670.HCI_pa_mode_config(self=MXD2670, Pa_mode=HCI_For_Serial.TxPaModeDef.LP_mode)
    #
    # MXD2670.HCI_pa_power_rfio_cap(self=MXD2670, power_mode=Rf_10db, RfioCapacitor=17)
    # MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=LDO_RF)
    # MXD2670.HCI_ldo_act_voltage(self=MXD2670, ldoAct=LDO_ACT)
    # MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=Acw_Val, TxGainSel=Power_set)
    # if(single_tone):
    #     MXD2670.HCI_single_tone(self=MXD2670, freqMHz=ChFreqMHz, powerSel=Power_set)
    # else:
    #     MXD2670.HCI_rf_tx_test(self=MXD2670, channel=channel, payloadtype=HCI_For_Serial.PayloadTypeDef.ALL1,
    #                            test_mode=Rf_mode)



    # Current

    #     MXD2670.HCI_single_tone(self=MXD2670, freqMHz=ChFreqMHz, powerSel=TxPowerDef.TX_10_DBM)
    # #     #CAP = 17   power_mode 0 == Lp 0dBm ， power_mode 1 == VMD 10dBm
    #     MXD2670.HCI_pa_power_rfio_cap(self=MXD2670, power_mode=1, RfioCapacitor=17)
    #     MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV)
    #     MXD2670.HCI_ldo_act_voltage(self=MXD2670, ldoAct=HCI_For_Serial.LdoActDef.LDO_ACT_1200mV)
    #     MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=235, TxGainSel=TxPowerDef.TX_10_DBM)
    #     MXD2670.HCI_rf_tx_test(self=MXD2670, channel=25, payloadtype=HCI_For_Serial.PayloadTypeDef.ALL1, test_mode=HCI_For_Serial.RfTestModeDef.LE1M)
        # MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=235, TxGainSel=TxPowerDef.TX_10_DBM)

    #
    # else:
    # MXD2670.HCI_single_tone(self=MXD2670, freqMHz=ChFreqMHz, powerSel=TxPowerDef.TX_0_DBM)
        #CAP = 17   power_mode 0 == Lp 0dBm ， power_mode 1 == VMD 10dBm
    # MXD2670.HCI_pa_power_rfio_cap(self=MXD2670, power_mode=0, RfioCapacitor=17)
    # MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV)
    # MXD2670.HCI_ldo_act_voltage(self=MXD2670, ldoAct=HCI_For_Serial.LdoActDef.LDO_ACT_1200mV)
    # MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=255, TxGainSel=TxPowerDef.TX_0_DBM)
    # MXD2670.HCI_rf_tx_test(self=MXD2670, channel=25, payloadtype=HCI_For_Serial.PayloadTypeDef.ALL1, test_mode=HCI_For_Serial.RfTestModeDef.LE1M)

    # if(0):

    MXD2670.HCI_pa_power_rfio_cap(self=MXD2670, power_mode=1, RfioCapacitor=17)
    MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV)
    MXD2670.HCI_ldo_act_voltage(self=MXD2670, ldoAct=HCI_For_Serial.LdoActDef.LDO_ACT_1200mV)
    # # MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=255, TxGainSel=TxPowerDef.TX_0_DBM)
    MXD2670.HCI_reg_acg_mode(self=MXD2670, AcgMode=HCI_For_Serial.RegAcgModeDef.GAIN2)
    MXD2670.HCI_rf_rx_test(self=MXD2670, channel=25, test_mode=HCI_For_Serial.RfTestModeDef.LE2M)
    print('Setting done.')

    # print('start')
    # MXD2670.HCI_rf_rx_test(self=MXD2670, channel=0, test_mode=RfTestModeDef.LE1M)
    # time.sleep(10)
    # num = MXD2670.HCI_rf_rx_end(self=MXD2670)
    # print((num))
    
    
    
    
    
    
    