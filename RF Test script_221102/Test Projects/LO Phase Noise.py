import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _AgilentE5052B_signalsource
from HCI import HCI_For_Serial

PN_TCPIP = 'TCPIP::192.168.190.32::INSTR'
BoardNum = 'DCDC#1_3'
HCIPort = 'COM5'

class TxPowerDef:
    TX_NEG20_DBM = 0
    TX_NEG5_DBM = 1
    TX_0_DBM = 2
    TX_5_DBM = 3
    TX_7_DBM = 4
    TX_10_DBM = 5


class Result_data:
    fre_index = np.array(np.zeros(1 * 40))
    DATA_1K = np.array(np.zeros(1 * 40))
    DATA_10K = np.array(np.zeros(1 * 40))
    DATA_100K = np.array(np.zeros(1 * 40))
    DATA_1M = np.array(np.zeros(1 * 40))
    DATA_10M = np.array(np.zeros(1 * 40))
    RMS_Jitter = np.array(np.zeros(1 * 40))


DATA = Result_data()
TXPWR = TxPowerDef()


sleep_time = 0.6
if __name__ == "__main__":
    DATA = Result_data()

    ####### 0dBm PN #######
    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCIPort, bps=115200, timeout=2)
    #
    SSA = _AgilentE5052B_signalsource.Agilent_E5052B
    SSA.spectrum_init(self=SSA, TCPIP=PN_TCPIP)
    SSA.identity(self=SSA)
    SSA.spectrum_config(self=SSA)
    #
    # # get testing data
    # for i in range(40):
    #     channel = i
    #     FreqMHz = (2402 + channel*2)
    #     MXD2670.HCI_single_tone(self=MXD2670, freqMHz=FreqMHz, powerSel=TXPWR.TX_0_DBM)
    #     MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=255, TxGainSel=HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_5)
    #     MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1150mV)
    #     SSA.updateMarker(self=SSA, Marker1='1000', Marker2='10000', Marker3='100000', Marker4='1000000',
    #                      Marker5='10000000')
    #     time.sleep(sleep_time)
    #
    #     MarkTable = SSA.getMarkerdBcHz(self=SSA)
    #     print(MarkTable)
    #     # print(SSA.getPowerDBM(self=SSA))
    #
    #     DATA.fre_index[i] = SSA.getFreqkHz(self=SSA)
    #     DATA.DATA_1K[i] = MarkTable[0]
    #     DATA.DATA_10K[i] = MarkTable[1]
    #     DATA.DATA_100K[i] = MarkTable[2]
    #     DATA.DATA_1M[i] = MarkTable[3]
    #     DATA.DATA_10M[i] = MarkTable[4]
    #     DATA.RMS_Jitter[i] = SSA.getDeg(self=SSA)
    #
    # SSA.disconnect(self=SSA)
    #
    # OUTPUT_path = 'D:\\DCDC_DATA\\'
    # OUTPUT_end = BoardNum
    # OUTPUT_form = '.xlsx'
    # writer = pd.ExcelWriter(
    #     OUTPUT_path + datetime.now().strftime('LO_PhaseNoise_0dBm_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)
    #
    # fre_index = np.linspace(2402, 2480, 40)
    # WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    # WRITER_DATA_1K = {'1k\n(dBc/Hz)': DATA.DATA_1K}
    # WRITER_DATA_10K = {'10k\n(dBc/Hz)': DATA.DATA_10K}
    # WRITER_DATA_100K = {'100k\n(dBc/Hz)': DATA.DATA_100K}
    # WRITER_DATA_1M = {'1M\n(dBc/Hz)': DATA.DATA_1M}
    # WRITER_DATA_10M = {'10M\n(dBc/Hz)': DATA.DATA_10M}
    # WRITER_DATA_RMS_Jitter = {'RMS_Jitter\n(deg)': DATA.RMS_Jitter}
    #
    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_1K, **WRITER_DATA_10K, **WRITER_DATA_100K, **WRITER_DATA_1M,
    #                 **WRITER_DATA_10M, **WRITER_DATA_RMS_Jitter)
    #
    # result_data = pd.DataFrame(ALL_DATA)
    # result_data.to_excel(writer, 'Phase Noise', float_format='%.5f')
    # try:
    #     writer.save()
    # except:
    #     print("report save warning")


    ####### 10dBm PN #######
    SSA.spectrum_init(self=SSA, TCPIP=PN_TCPIP)
    SSA.identity(self=SSA)
    SSA.spectrum_config(self=SSA)

    # get testing data
    for i in range(40):
        channel = i
        FreqMHz = (2402 + channel*2)
        MXD2670.HCI_single_tone(self=MXD2670, freqMHz=FreqMHz, powerSel=TXPWR.TX_10_DBM)
        MXD2670.HCI_tx_pa_acw_config(self=MXD2670, AcwVal=255, TxGainSel=HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_5)
        MXD2670.HCI_ldo_rf_voltage(self=MXD2670, ldoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1150mV)
        SSA.updateMarker(self=SSA, Marker1='1000', Marker2='10000', Marker3='100000', Marker4='1000000',
                         Marker5='10000000')
        time.sleep(sleep_time)

        MarkTable = SSA.getMarkerdBcHz(self=SSA)
        print(MarkTable)
        # print(SSA.getPowerDBM(self=SSA))

        DATA.fre_index[i] = SSA.getFreqkHz(self=SSA)
        DATA.DATA_1K[i] = MarkTable[0]
        DATA.DATA_10K[i] = MarkTable[1]
        DATA.DATA_100K[i] = MarkTable[2]
        DATA.DATA_1M[i] = MarkTable[3]
        DATA.DATA_10M[i] = MarkTable[4]
        DATA.RMS_Jitter[i] = SSA.getDeg(self=SSA)

    SSA.disconnect(self=SSA)

    OUTPUT_path = 'D:\\DCDC_DATA\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime('LO_PhaseNoise_10dBm_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    fre_index = np.linspace(2402, 2480, 40)
    WRITER_DATA_INDEX = {'Frequence\n(Mhz)': DATA.fre_index}
    WRITER_DATA_1K = {'1k\n(dBc/Hz)': DATA.DATA_1K}
    WRITER_DATA_10K = {'10k\n(dBc/Hz)': DATA.DATA_10K}
    WRITER_DATA_100K = {'100k\n(dBc/Hz)': DATA.DATA_100K}
    WRITER_DATA_1M = {'1M\n(dBc/Hz)': DATA.DATA_1M}
    WRITER_DATA_10M = {'10M\n(dBc/Hz)': DATA.DATA_10M}
    WRITER_DATA_RMS_Jitter = {'RMS_Jitter\n(deg)': DATA.RMS_Jitter}

    ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_1K, **WRITER_DATA_10K, **WRITER_DATA_100K, **WRITER_DATA_1M,
                    **WRITER_DATA_10M, **WRITER_DATA_RMS_Jitter)

    result_data = pd.DataFrame(ALL_DATA)
    result_data.to_excel(writer, 'Phase Noise', float_format='%.5f')
    try:
        writer.save()
    except:
        print("report save warning")