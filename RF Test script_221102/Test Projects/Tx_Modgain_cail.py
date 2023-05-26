import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _AgilentN9020A_spectrum
from HCI import HCI_For_Serial

# LAN INFORMATION
SPEC_TCPIP = 'TCPIP::192.168.190.22::INSTR'

# BOARD INFORMATION
BoardNum = '#1'
loadCap = 95  # 9.5pF

# ENVIRONMENT
Temp = '25℃'

# CONDITIONS
OTW_VAL = [0, 100]


class TxPowerDef:
    TX_NEG20_DBM = 0
    TX_NEG5_DBM = 1
    TX_0_DBM = 2
    TX_5_DBM = 3
    TX_7_DBM = 4
    TX_10_DBM = 5


class VcoPowerDef:
    LDO_VCO_850mV = 0
    LDO_VCO_900mV = 1
    LDO_VCO_950mV = 2
    LDO_VCO_1000mV = 3
    LDO_VCO_1050mV = 4
    LDO_VCO_1100mV = 5
    LDO_VCO_1150mV = 6
    LDO_VCO_1200mV = 7


class LdoActDef:
    LDO_ACT_1300mV = 0
    LDO_ACT_1250mV = 1
    LDO_ACT_1200mV = 2
    LDO_ACT_1150mV = 3
    LDO_ACT_1100mV = 4
    LDO_ACT_1050mV = 5
    LDO_ACT_1000mV = 6
    LDO_ACT_950mV = 7


class LdoRfDef:
    LDO_RF_850mV = 0
    LDO_RF_900mV = 1
    LDO_RF_950mV = 2
    LDO_RF_1000mV = 3
    LDO_RF_1050mV = 4
    LDO_RF_1100mV = 5
    LDO_RF_1150mV = 6
    LDO_RF_1200mV = 7


SamplesNum = 3


class Result_data:
    Flo1MHz = np.array(np.zeros(1 * SamplesNum))
    Flo2MHz = np.array(np.zeros(1 * SamplesNum))
    ModGainCali = np.array(np.zeros(1 * SamplesNum))


result_data = Result_data()


class HCI_para:
    PORT = 'COM3'
    BPS = 115200


class Tx_MODGAIN_CALI:
    def __init__(self):
        self.MXD2670 = None
        self.SPEC = None
        self.MODGAIN = 0
        self.Flo0MHz = 0.0
        self.Flo100MHz = 0.0

    def Tx_modgain_test_init(self):
        # spectrum init
        self.SPEC = _AgilentN9020A_spectrum.Agilent_MXA_N9020A
        self.SPEC.spectrum_init(self=self.SPEC, TCPIP=SPEC_TCPIP)
        self.SPEC.identity(self=self.SPEC)
        self.SPEC.getInitialParamsAgilent(self=self.SPEC)
        self.SPEC.setSpanMHz(self=self.SPEC, span=100)
        self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=2450)
        time.sleep(0.5)
        print('spectrum init success')

        # device init
        self.MXD2670 = HCI_For_Serial.HCI_Serial
        self.MXD2670.HCI_serial_port_refresh(self=self.MXD2670)
        self.MXD2670.HCI_port_init(self=self.MXD2670, port=HCI_para.PORT, bps=HCI_para.BPS, timeout=2)
        self.MXD2670.HCI_set_dcxo_loadcap_val(self=self.MXD2670, loadCap=95)
        print('device init success')

    def Tx_Modgain_Test(self):
        mg_sample_num = 20
        modgain_sample = np.array(np.zeros(mg_sample_num))
        freqMHz_sample = np.array(np.zeros(mg_sample_num))
        # print(modgain_sample)

        for otw_indxe in range(0, 2):
            print('otw_indxe', otw_indxe)
            self.MXD2670.HCI_single_tone(self=self.MXD2670, freqMHz=2440, powerSel=TxPowerDef.TX_10_DBM)
            self.MXD2670.HCI_otw_debug_modgain(self=self.MXD2670, OTW_VAL=OTW_VAL[otw_indxe])
            self.SPEC.setSpanMHz(self=self.SPEC, span=100)
            time.sleep(10)
            self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=2450)
            time.sleep(10)
            tempFreqMHz = self.SPEC.getMaxPowerFreqMHz(self=self.SPEC)
            print(tempFreqMHz)
            self.SPEC.setSpanMHz(self=self.SPEC, span=1)
            self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=tempFreqMHz)
            for i in range(0, mg_sample_num):
                time.sleep(0.2)
                freqMHz_sample[i] = self.SPEC.getMaxPowerFreqMHz(self=self.SPEC)
                print(freqMHz_sample[i])
            if otw_indxe == 0:
                self.Flo0MHz = freqMHz_sample.sum() / mg_sample_num
                print('OTW:', OTW_VAL[otw_indxe], 'FLO:', self.Flo0MHz)
            else:
                self.Flo100MHz = freqMHz_sample.sum() / mg_sample_num
                print('OTW:', OTW_VAL[otw_indxe], 'FLO:', self.Flo100MHz)

        for i in range(0, mg_sample_num):
            time.sleep(0.2)
            modgain_sample[i] = self.MXD2670.HCI_get_modgain_cail_val(self=self.MXD2670, freqMHz=round((self.Flo100MHz+self.Flo0MHz)/2))  # 2438
            # print(modgain_sample[i])
        print(modgain_sample)
        self.MODGAIN = modgain_sample.sum() / mg_sample_num
        print(self.MODGAIN)

        return [self.Flo0MHz, self.Flo100MHz, self.MODGAIN]

    def Tx_Modgain_test_end(self):
        self.SPEC.disconnect(self=self.SPEC)


if __name__ == "__main__":
    TxCali = Tx_MODGAIN_CALI
    TxCali.Tx_modgain_test_init(self=TxCali)
    print(TxCali.Tx_Modgain_Test(self=TxCali))
    TxCali.Tx_Modgain_test_end(self=TxCali)

    # result_data = Result_data()
    # count = 0
    # for FreqMHzIdx in range(StartMHz, StopMHz, 2):
    #     TempList = PA.PA_channel_current(self=PA, ChFreqMHz=FreqMHzIdx, ACW=255, VDD_RF=1.3 + 0.12,
    #                                      LdoVco=HCI_For_Serial.VcoPowerDef.LDO_VCO_900mV,
    #                                      LdoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV,
    #                                      TxPwr=HCI_For_Serial.TxPowerDef.TX_10_DBM)
    #     print('ChannelFreq:', FreqMHzIdx,
    #           'OutputPower:', '{:.2f}'.format(TempList[0]), 'dBm ', 'RFCurrent:',
    #           '{:.2f}'.format(TempList[1]), 'mA')
    #     DATA.fre_index[count] = FreqMHzIdx
    #     DATA.ReadPowerDBM[count] = round(TempList[0], 2)
    #     DATA.VddRFCurrentMA[count] = round(TempList[1], 2)
    #     count += 1
    #     # print('ChannelFreq:', DATA.fre_index,
    #     #       'OutputPower:', DATA.ReadPowerDBM, 'dBm ', 'RFCurrent:',
    #     #       DATA.VddRFCurrentMA, 'mA')
    #
    #     # time.sleep(0.2)
    #
    # PA.PA_test_end(self=PA)
    #
    # OUTPUT_path = '.\\'
    # OUTPUT_end = BoardNum
    # OUTPUT_form = '.xlsx'
    # writer = pd.ExcelWriter(
    #     OUTPUT_path + datetime.now().strftime(
    #         'PA_VMD_TxPwr_Current_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)
    #
    # fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    # # WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    # WRITER_DATA_POWER = {'Tx_Power\n(Mhz)': DATA.ReadPowerDBM}
    # WRITER_DATA_CURRENT = {'RF_Current\n(deg)': DATA.VddRFCurrentMA}
    #
    # # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    # ALL_DATA = dict(**WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    # # print(ALL_DATA)
    #
    # result_data = pd.DataFrame(ALL_DATA)
    # result_data.to_excel(writer, 'Tx_Power', float_format='%.5f')
    # writer.save()
    # writer.close()
    #
    # ########## LP  ##########
    # DATA2 = Result_data()
    # result_data2 = Result_data()
    # PA.PA_channel_current_test_init(self=PA)
    #
    # count = 0
    # for FreqMHzIdx in range(StartMHz, StopMHz, 2):
    #     TempList = PA.PA_channel_current(self=PA, ChFreqMHz=FreqMHzIdx, ACW=255, VDD_RF=1.3 + 0.12,
    #                                      LdoVco=HCI_For_Serial.VcoPowerDef.LDO_VCO_900mV,
    #                                      LdoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV,
    #                                      TxPwr=HCI_For_Serial.TxPowerDef.TX_0_DBM)
    #     print('ChannelFreq:', FreqMHzIdx,
    #           'OutputPower:', '{:.2f}'.format(TempList[0]), 'dBm ', 'RFCurrent:',
    #           '{:.2f}'.format(TempList[1]), 'mA')
    #     DATA2.fre_index[count] = FreqMHzIdx
    #     DATA2.ReadPowerDBM[count] = round(TempList[0], 2)
    #     DATA2.VddRFCurrentMA[count] = round(TempList[1], 2)
    #     count += 1
    #     # print('ChannelFreq:', DATA.fre_index,
    #     #       'OutputPower:', DATA.ReadPowerDBM, 'dBm ', 'RFCurrent:',
    #     #       DATA.VddRFCurrentMA, 'mA')
    #
    #     # time.sleep(0.2)
    #
    # PA.PA_test_end(self=PA)
    #
    # OUTPUT_path2 = '.\\'
    # OUTPUT_end2 = BoardNum
    # OUTPUT_form2 = '.xlsx'
    # writer2 = pd.ExcelWriter(
    #     OUTPUT_path2 + datetime.now().strftime(
    #         'PA_LP_TxPwr_Current_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end2 + OUTPUT_form2)
    #
    # fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    # # WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    # WRITER_DATA_POWER2 = {'Tx_Power\n(Mhz)': DATA2.ReadPowerDBM}
    # WRITER_DATA_CURRENT2 = {'RF_Current\n(deg)': DATA2.VddRFCurrentMA}
    #
    # # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    # ALL_DATA2 = dict(**WRITER_DATA_POWER2, **WRITER_DATA_CURRENT2)
    # # print(ALL_DATA)
    #
    # result_data2 = pd.DataFrame(ALL_DATA2)
    # result_data2.to_excel(writer2, 'Tx_Power', float_format='%.5f')
    # writer2.save()
    # writer2.close()
