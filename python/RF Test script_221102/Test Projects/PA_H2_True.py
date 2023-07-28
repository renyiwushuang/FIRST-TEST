import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _AgilentN9020A_spectrum
from instrument import _E36312A_power
from instrument import _Agilent34410A_multimeter
from HCI import HCI_For_Serial

# LAN INFORMATION
SPEC_TCPIP = 'TCPIP::192.168.190.106::INSTR'

# BOARD INFORMATION
BoardNum = '#1'

# ENVIRONMENT
Temp = '25℃'

# CONDITIONS



class TxPowerDef:
    TX_NEG20_DBM = 0
    TX_NEG5_DBM = 1
    TX_0_DBM = 2
    TX_5_DBM = 3
    TX_7_DBM = 4
    TX_10_DBM = 5





class Result_data:
    H1 = np.array(np.zeros(1 * 32))
    H2 = np.array(np.zeros(1 * 32))
    H3 = np.array(np.zeros(1 * 32))



result_data = Result_data()


class HCI_para:
    PORT = 'COM5'
    BPS = 115200


class PA_Test:
    def __init__(self):
        self.MXD2670 = None
        self.CUR = None
        self.PWR = None
        self.SPEC = None
        self.DATA = Result_data()
        self.ACW = 0
        self.OutputPowerDBM = 0
        self.VddRfCurrentMA = 0

    def PA_h2_init(self):
        # spectrum init
        self.SPEC = _AgilentN9020A_spectrum.Agilent_MXA_N9020A
        self.SPEC.spectrum_init(self=self.SPEC, TCPIP=SPEC_TCPIP)
        self.SPEC.identity(self=self.SPEC)
        self.SPEC.getInitialParamsAgilent(self=self.SPEC)
        self.SPEC.setSpanMHz(self=self.SPEC, span=1)
        self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=2440)
        time.sleep(0.5)
        print('spectrum init success')

        # device init
        self.MXD2670 = HCI_For_Serial.HCI_Serial
        self.MXD2670.HCI_serial_port_refresh(self=self.MXD2670)
        self.MXD2670.HCI_port_init(self=self.MXD2670, port=HCI_para.PORT, bps=HCI_para.BPS, timeout=2)
        print('device init success')

    def PA_test_end(self):
        self.SPEC.disconnect(self=self.SPEC)


if __name__ == "__main__":
    PA = PA_Test

    PA.PA_h2_init(self=PA)

    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCI_para.PORT, bps=115200, timeout=2)

    Base_Freq_MHz = 2440;

    VMD_data = Result_data()
    LP_data = Result_data()

    for H2_value in range(16):
        # power mode 0 == LP , Power mode 1 == VMD
        MXD2670.HCI_tx_pa_h2_config(self=MXD2670, H2Val=H2_value)

        ########## VMD  ##########
        MXD2670.HCI_single_tone(self=MXD2670,freqMHz=Base_Freq_MHz, powerSel=5)

        DATA = Result_data()
        result_data = Result_data()
        PA.SPEC.setCentralFreqMHz(self=PA.SPEC, centralFreq=Base_Freq_MHz)
        TempList_NoH = PA.SPEC.getPowerDBM(self=PA.SPEC, freq= Base_Freq_MHz)
        time.sleep(0.3)
        PA.SPEC.setCentralFreqMHz(self=PA.SPEC, centralFreq=Base_Freq_MHz*2)
        TempList_H2 = PA.SPEC.getPowerDBM(self=PA.SPEC, freq= Base_Freq_MHz*2)
        time.sleep(0.3)
        PA.SPEC.setCentralFreqMHz(self=PA.SPEC, centralFreq=Base_Freq_MHz*3)
        TempList_H3 = PA.SPEC.getPowerDBM(self=PA.SPEC, freq=Base_Freq_MHz*3)
        time.sleep(0.3)
        print('ChannelFreq:', H2_value,
                  'OutputPower:', '{:.2f}'.format(TempList_NoH), 'dBm ', 'RFCurrent:',)

        VMD_data.H1[H2_value] = TempList_NoH
        VMD_data.H2[H2_value] = round(TempList_H2)
        VMD_data.H3[H2_value] = round(TempList_H3)

        ########## LP  ##########
        # MXD2670.HCI_tx_pa_h2_config(self=MXD2670, H2Val=H2_value)
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=Base_Freq_MHz, powerSel=2)
        DATA2 = Result_data()
        result_data2 = Result_data()
        PA.PA_h2_init(self=PA)
        PA.SPEC.setCentralFreqMHz(self=PA.SPEC, centralFreq=Base_Freq_MHz)
        TempList_NoH = PA.SPEC.getPowerDBM(self=PA.SPEC, freq=Base_Freq_MHz)
        time.sleep(0.3)
        PA.SPEC.setCentralFreqMHz(self=PA.SPEC, centralFreq=Base_Freq_MHz * 2)
        TempList_H2 = PA.SPEC.getPowerDBM(self=PA.SPEC, freq=Base_Freq_MHz * 2)
        time.sleep(0.3)
        PA.SPEC.setCentralFreqMHz(self=PA.SPEC, centralFreq=Base_Freq_MHz * 3)
        TempList_H3 = PA.SPEC.getPowerDBM(self=PA.SPEC, freq=Base_Freq_MHz * 3)

        print('ChannelFreq:', H2_value,
                  'OutputPower:', '{:.2f}'.format(TempList_NoH), 'dBm ', 'RFCurrent:',)

        LP_data.H1[H2_value] = TempList_NoH
        LP_data.H2[H2_value] = round(TempList_H2)
        LP_data.H3[H2_value] = round(TempList_H3)


    PA.PA_test_end(self=PA)


    OUTPUT_path = 'D:\\RF_H2\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime(
            'PA_VMD_H2_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    Index = np.linspace(0,15,16)
    WRITER_DATA_IDEX = {'PA_H2 0x4000881c[4:1]': Index}
    WRITER_DATA_H1 = {'Tx_Power\n(Mhz)': VMD_data.H1}
    WRITER_DATA_H2 = {'Tx_Power\n(Mhz)': VMD_data.H2}
    WRITER_DATA_H3 = {'RF_Current\n(deg)': VMD_data.H3}

    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    ALL_DATA = dict(**WRITER_DATA_IDEX, **WRITER_DATA_H1, **WRITER_DATA_H2, **WRITER_DATA_H3)
    # print(ALL_DATA)

    result_data = pd.DataFrame(ALL_DATA)
    result_data.to_excel(writer, 'Tx_Power', float_format='%.5f')
    writer.save()
    writer.close()


    OUTPUT_path2 = 'D:\\RF_H2\\'
    OUTPUT_end2 = BoardNum
    OUTPUT_form2 = '.xlsx'
    writer2 = pd.ExcelWriter(
        OUTPUT_path2 + datetime.now().strftime(
            'PA_LP_H2_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end2 + OUTPUT_form2)
    Index = np.linspace(0,15,16)
    WRITER2_DATA_IDEX = {'PA_H2 0x4000881c[4:1]': Index}
    WRITER2_DATA_H1 = {'Tx_Power\n(Mhz)': LP_data.H1}
    WRITER2_DATA_H2 = {'Tx_Power\n(Mhz)': LP_data.H2}
    WRITER2_DATA_H3 = {'RF_Current\n(deg)': LP_data.H3}

    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    ALL_DATA2 = dict(**WRITER2_DATA_IDEX, **WRITER2_DATA_H1, **WRITER2_DATA_H2, **WRITER2_DATA_H3)
    # print(ALL_DATA)

    result_data2 = pd.DataFrame(ALL_DATA2)
    result_data2.to_excel(writer2, 'PA_H2', float_format='%.5f')
    writer2.save()
    writer2.close()


