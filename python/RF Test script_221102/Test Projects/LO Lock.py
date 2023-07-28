import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _AgilentE5052B_signalsource
from HCI import HCI_For_Serial

PN_TCPIP = 'TCPIP::192.168.190.32::INSTR'
BoardNum = '#1'
HCIPort = 'COM3'
Temp = '25℃'


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


StartMHz = 2270
StopMHz = 2780+1
SamplesNum = StopMHz - StartMHz


class Result_data:
    fre_index = np.array(np.zeros(1 * SamplesNum))
    RMS_Jitter = np.array(np.zeros(1 * SamplesNum))


DATA = Result_data()
TXPWR = TxPowerDef()
VCOPWR = VcoPowerDef()

if __name__ == "__main__":
    DATA = Result_data()

    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)

    # ####### VCO_LDO 900mV #######
    # VcoLdoSel = VCOPWR.LDO_VCO_900mV
    # VcoLdoSelSrt = '900mV'
    # SSA = _AgilentE5052B_signalsource.Agilent_E5052B
    # SSA.spectrum_init(self=SSA, TCPIP=PN_TCPIP)
    # SSA.identity(self=SSA)
    # SSA.spectrum_config(self=SSA)
    #
    # MXD2670.HCI_vco_ldo_voltage(self=MXD2670, powerSel=VcoLdoSel)
    # # get testing data
    # for i in range(SamplesNum):
    #     FreqMHz = StartMHz+i
    #     MXD2670.HCI_single_tone(self=MXD2670, freqMHz=FreqMHz, powerSel=TXPWR.TX_10_DBM)
    #     SSA.updateMarker(self=SSA, Marker1='1000', Marker2='10000', Marker3='100000', Marker4='1000000',
    #                      Marker5='10000000')
    #     time.sleep(0.2)
    #
    #     # print(SSA.getPowerDBM(self=SSA))
    #     DATA.fre_index[i] = SSA.getFreqkHz(self=SSA)
    #     DATA.RMS_Jitter[i] = SSA.getDeg(self=SSA)
    #     print(FreqMHz, DATA.fre_index[i], DATA.RMS_Jitter[i])
    #
    # SSA.disconnect(self=SSA)
    #
    # OUTPUT_path = '.\\'
    # OUTPUT_end = BoardNum
    # OUTPUT_form = '.xlsx'
    # writer = pd.ExcelWriter(
    #     OUTPUT_path + datetime.now().strftime(
    #         'LO_Lock_' + Temp + '_' + VcoLdoSelSrt + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)
    #
    # fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    # WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    # WRITER_DATA_RMS_Jitter = {'RMS_Jitter\n(deg)': DATA.RMS_Jitter}
    #
    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_RMS_Jitter)
    #
    # result_data = pd.DataFrame(ALL_DATA)
    # result_data.to_excel(writer, 'VCO Lock', float_format='%.5f')
    # writer.save()
    # writer.close()

    ####### VCO_LDO 950mV #######
    # VcoLdoSel = VCOPWR.LDO_VCO_950mV
    # VcoLdoSelSrt = '950mV'
    # SSA = _AgilentE5052B_signalsource.Agilent_E5052B
    # SSA.spectrum_init(self=SSA, TCPIP=PN_TCPIP)
    # SSA.identity(self=SSA)
    # SSA.spectrum_config(self=SSA)
    #
    # MXD2670.HCI_vco_ldo_voltage(self=MXD2670, powerSel=VcoLdoSel)
    # # get testing data
    # for i in range(SamplesNum):
    #     FreqMHz = StartMHz+i
    #     MXD2670.HCI_single_tone(self=MXD2670, freqMHz=FreqMHz, powerSel=TXPWR.TX_10_DBM)
    #     SSA.updateMarker(self=SSA, Marker1='1000', Marker2='10000', Marker3='100000', Marker4='1000000',
    #                      Marker5='10000000')
    #     time.sleep(0.2)
    #
    #     # print(SSA.getPowerDBM(self=SSA))
    #     DATA.fre_index[i] = SSA.getFreqkHz(self=SSA)
    #     DATA.RMS_Jitter[i] = SSA.getDeg(self=SSA)
    #     print(FreqMHz, DATA.fre_index[i], DATA.RMS_Jitter[i])
    #
    # SSA.disconnect(self=SSA)
    #
    # OUTPUT_path = '.\\'
    # OUTPUT_end = BoardNum
    # OUTPUT_form = '.xlsx'
    # writer = pd.ExcelWriter(
    #     OUTPUT_path + datetime.now().strftime(
    #         'LO_Lock_' + Temp + '_' + VcoLdoSelSrt + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)
    #
    # fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    # WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    # WRITER_DATA_RMS_Jitter = {'RMS_Jitter\n(deg)': DATA.RMS_Jitter}
    #
    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_RMS_Jitter)
    #
    # result_data = pd.DataFrame(ALL_DATA)
    # result_data.to_excel(writer, 'VCO Lock', float_format='%.5f')
    # writer.save()
    # writer.close()

    ####### VCO_LDO 1000mV #######
    VcoLdoSel = VCOPWR.LDO_VCO_1000mV
    VcoLdoSelSrt = '1000mV'
    SSA = _AgilentE5052B_signalsource.Agilent_E5052B
    SSA.spectrum_init(self=SSA, TCPIP=PN_TCPIP)
    SSA.identity(self=SSA)
    SSA.spectrum_config(self=SSA)

    MXD2670.HCI_vco_ldo_voltage(self=MXD2670, powerSel=VcoLdoSel)
    # get testing data
    for i in range(SamplesNum):
        FreqMHz = StartMHz+i
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=FreqMHz, powerSel=TXPWR.TX_10_DBM)
        SSA.updateMarker(self=SSA, Marker1='1000', Marker2='10000', Marker3='100000', Marker4='1000000',
                         Marker5='10000000')
        time.sleep(0.2)

        # print(SSA.getPowerDBM(self=SSA))
        DATA.fre_index[i] = SSA.getFreqkHz(self=SSA)
        DATA.RMS_Jitter[i] = SSA.getDeg(self=SSA)
        print(FreqMHz, DATA.fre_index[i], DATA.RMS_Jitter[i])

    SSA.disconnect(self=SSA)

    OUTPUT_path = '.\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime(
            'LO_Lock_' + Temp + '_' + VcoLdoSelSrt + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    fre_index = np.linspace(StartMHz, StopMHz, SamplesNum)
    WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    WRITER_DATA_RMS_Jitter = {'RMS_Jitter\n(deg)': DATA.RMS_Jitter}

    ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_RMS_Jitter)

    result_data = pd.DataFrame(ALL_DATA)
    result_data.to_excel(writer, 'VCO Lock', float_format='%.5f')
    writer.save()
    writer.close()
