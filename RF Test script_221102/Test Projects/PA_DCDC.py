import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _AgilentN9020A_spectrum
from HCI import HCI_For_Serial

# LAN INFORMATION
SPEC_TCPIP = 'TCPIP::192.168.190.122::INSTR'

# BOARD INFORMATION
BoardNum = 'LDO#1_2'

# ENVIRONMENT
Temp = '25℃'

# CONDITIONS
StartMHz = 2402
StopMHz = 2480 + 2
SamplesNum = int((StopMHz - StartMHz) / 2)
StartACW = 0
StopACW = 256
StepACW = 2
SamplesAcwNum = int((StopACW - StartACW) / 2)


class TxPowerDef:
    TX_NEG20_DBM = 0
    TX_NEG5_DBM = 1
    TX_0_DBM = 2
    TX_5_DBM = 3
    TX_7_DBM = 4
    TX_10_DBM = 5





class Result_data:
    fre_index = np.array(np.zeros(1 * SamplesNum))
    ReadPowerDBM = np.array(np.zeros(1 * SamplesNum))



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

    def PA_dcdc_init(self):
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

    def PA_channel_power(self, ChFreqMHz, ACW, TxGain,TxPwr=[TxPowerDef]):
        self.OutputPowerDBM = 0
        self.MXD2670.HCI_single_tone(self=self.MXD2670, freqMHz=ChFreqMHz, powerSel=TxPwr)
        self.MXD2670.HCI_tx_pa_acw_config(self=self.MXD2670, AcwVal=ACW, TxGainSel=TxGain )
        self.MXD2670.HCI_ldo_rf_voltage(self=self.MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV)
        time.sleep(0.1)
        self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=ChFreqMHz)
        time.sleep(0.3)
        self.OutputPowerDBM = self.SPEC.getMaxFreqPower(self=self.SPEC)
        return [self.OutputPowerDBM]


if __name__ == "__main__":
    TempList = []
    PA = PA_Test

    PA.PA_dcdc_init(self=PA)

    # MXD2670 = HCI_For_Serial.HCI_Serial
    # MXD2670.HCI_serial_port_refresh(self=MXD2670)
    # MXD2670.HCI_port_init(self=MXD2670, port=HCI_para.PORT, bps=115200, timeout=2)

    ########## VMD  ##########
    DATA = Result_data()
    result_data = Result_data()
    count = 0
    for FreqMHzIdx in range(StartMHz, StopMHz, 2):
        # HCI_single_tone(self=PA, freqMHz=FreqMHzIdx, powerSel=[TxPowerDef])
        TempList = PA.PA_channel_power(self=PA, ChFreqMHz=FreqMHzIdx, ACW=230, TxGain=HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_5,TxPwr=HCI_For_Serial.TxPowerDef.TX_10_DBM)

        # print('ChannelFreq:', FreqMHzIdx,
        #       'OutputPower:', '{:.2f}'.format(TempList[0]), 'dBm ', 'RFCurrent:',
        #       '{:.2f}'.format(TempList[1]), 'mA')
        DATA.fre_index[count] = FreqMHzIdx
        DATA.ReadPowerDBM[count] = round(TempList[0], 2)
        count += 1
        # print('ChannelFreq:', DATA.fre_index,
        #       'OutputPower:', DATA.ReadPowerDBM, 'dBm ', 'RFCurrent:',
        #       DATA.VddRFCurrentMA, 'mA')

        # time.sleep(0.2)

    PA.PA_test_end(self=PA)

    OUTPUT_path = 'D:\\DCDC_DATA\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime(
            'PA_VMD_TxPwr_DCDC_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    WRITER_DATA_POWER = {'Tx_Power\n(Mhz)': DATA.ReadPowerDBM}

    ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER)
    # ALL_DATA = dict(**WRITER_DATA_POWER)
    # print(ALL_DATA)

    result_data = pd.DataFrame(ALL_DATA)
    result_data.to_excel(writer, 'Tx_Power', float_format='%.2f')
    writer.save()
    writer.close()

    ######### LP  ##########
    DATA2 = Result_data()
    result_data2 = Result_data()
    PA.PA_dcdc_init(self=PA)

    count = 0
    for FreqMHzIdx in range(StartMHz, StopMHz, 2):

        TempList = PA.PA_channel_power(self=PA, ChFreqMHz=FreqMHzIdx, ACW=255, TxGain=HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_5,TxPwr=HCI_For_Serial.TxPowerDef.TX_0_DBM)

        # print('ChannelFreq:', FreqMHzIdx,
        #       'OutputPower:', '{:.2f}'.format(TempList[0]), 'dBm ', 'RFCurrent:',
        #       '{:.2f}'.format(TempList[1]), 'mA')
        DATA2.fre_index[count] = FreqMHzIdx
        DATA2.ReadPowerDBM[count] = round(TempList[0], 2)
        count += 1
        # print('ChannelFreq:', DATA.fre_index,
        #       'OutputPower:', DATA.ReadPowerDBM, 'dBm ', 'RFCurrent:',
        #       DATA.VddRFCurrentMA, 'mA')

        # time.sleep(0.2)

    PA.PA_test_end(self=PA)

    OUTPUT_path2 = 'D:\\DCDC_DATA\\'
    OUTPUT_end2 = BoardNum
    OUTPUT_form2 = '.xlsx'
    writer2 = pd.ExcelWriter(
        OUTPUT_path2 + datetime.now().strftime(
            'PA_LP_TxPwr_DCDC_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end2 + OUTPUT_form2)

    # fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    WRITER_DATA_INDEX2 = {'Frequence\n(Mhz)': DATA.fre_index}
    WRITER_DATA_POWER2 = {'Tx_Power\n(Mhz)': DATA2.ReadPowerDBM}
    # WRITER_DATA_CURRENT2 = {'RF_Current\n(deg)': DATA2.VddRFCurrentMA}

    ALL_DATA2 = dict(**WRITER_DATA_INDEX2, **WRITER_DATA_POWER2)
    # ALL_DATA2 = dict(**WRITER_DATA_POWER2, **WRITER_DATA_CURRENT2)
    # print(ALL_DATA)

    result_data2 = pd.DataFrame(ALL_DATA2)
    result_data2.to_excel(writer2, 'Tx_Power_', float_format='%.2f')
    writer2.save()
    writer2.close()

