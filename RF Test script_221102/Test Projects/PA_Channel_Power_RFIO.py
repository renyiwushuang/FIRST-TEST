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
METER_TCPIP = 'TCPIP::192.168.190.31::inst0::INSTR'
PWR_TCPIP = 'TCPIP::192.168.190.74::inst0::INSTR'

# BOARD INFORMATION
BoardNum = '#1'

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


class Result_data:
    fre_index = np.array(np.zeros(1 * 32))
    ReadPowerDBM = np.array(np.zeros(1 * 32))
    VddRFCurrentMA = np.array(np.zeros(1 * 32))



result_data = Result_data()


class HCI_para:
    PORT = 'COM3'
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

    def PA_channel_current_test_init(self):
        # spectrum init
        self.SPEC = _AgilentN9020A_spectrum.Agilent_MXA_N9020A
        self.SPEC.spectrum_init(self=self.SPEC, TCPIP=SPEC_TCPIP)
        self.SPEC.identity(self=self.SPEC)
        self.SPEC.getInitialParamsAgilent(self=self.SPEC)
        self.SPEC.setSpanMHz(self=self.SPEC, span=1)
        self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=2440)
        time.sleep(0.5)
        print('spectrum init success')

        # power supply init
        self.PWR = _E36312A_power.Waveform
        self.PWR.power_init(self=self.PWR, TCPIP=PWR_TCPIP)
        self.PWR.set_ch1_voltage(self=self.PWR, vol=1.3, cur=0.5)
        self.PWR.power_ch1_on(self=self.PWR)
        print('power supply init success')

        # meter init
        self.CUR = _Agilent34410A_multimeter.Multimeter
        self.CUR.meter_init(self=self.CUR, TCPIP=METER_TCPIP)
        self.CUR.config_to_dci_mode(self=self.CUR)
        print('meter init success')

        # device init
        self.MXD2670 = HCI_For_Serial.HCI_Serial
        self.MXD2670.HCI_serial_port_refresh(self=self.MXD2670)
        self.MXD2670.HCI_port_init(self=self.MXD2670, port=HCI_para.PORT, bps=HCI_para.BPS, timeout=2)
        print('device init success')

    def PA_channel_current(self, ChFreqMHz, ACW, VDD_RF, LdoVco=[VcoPowerDef], TxPwr=[TxPowerDef], LdoRf=[LdoRfDef]):
        self.OutputPowerDBM = 0
        self.VddRfCurrentMA = 0
        self.PWR.set_ch1_voltage(self=self.PWR, vol=VDD_RF, cur=0.5)
        time.sleep(0.1)

        self.MXD2670.HCI_single_tone(self=self.MXD2670, freqMHz=ChFreqMHz, powerSel=TxPwr)
        TxGainSel = 0
        if TxPwr == TxPowerDef.TX_10_DBM:
            TxGainSel = HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_5
        if TxPwr == TxPowerDef.TX_7_DBM:
            TxGainSel = HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_4
        if TxPwr == TxPowerDef.TX_5_DBM:
            TxGainSel = HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_3
        if TxPwr == TxPowerDef.TX_0_DBM:
            TxGainSel = HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_2
        if TxPwr == TxPowerDef.TX_NEG5_DBM:
            TxGainSel = HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_1
        if TxPwr == TxPowerDef.TX_NEG20_DBM:
            TxGainSel = HCI_For_Serial.TxGainTabIdxDef.TX_GAIN_0

        self.MXD2670.HCI_vco_ldo_voltage(self=self.MXD2670, powerSel=LdoVco)
        self.MXD2670.HCI_ldo_rf_voltage(self=self.MXD2670, ldoRf=LdoRf)
        self.MXD2670.HCI_tx_pa_acw_config(self=self.MXD2670, AcwVal=ACW, TxGainSel=TxGainSel)
        # print('read ACW', self.MXD2670.HCI_read_reg(self=self.MXD2670, reg_addr=0x40008148))
        time.sleep(0.1)
        self.SPEC.setCentralFreqMHz(self=self.SPEC, centralFreq=ChFreqMHz)
        time.sleep(0.3)
        self.OutputPowerDBM = self.SPEC.getMaxFreqPower(self=self.SPEC)
        # print(self.OutputPowerDBM)
        # time.sleep(0.5)
        self.VddRfCurrentMA = self.CUR.get_current_mA(self=self.CUR)

        # print(self.VddRfCurrentMA)
        return [self.OutputPowerDBM, self.VddRfCurrentMA]

    def PA_test_end(self):
        self.PWR.power_ch1_off(self=self.PWR)
        self.PWR.close(self=self.PWR)
        self.CUR.close(self=self.CUR)
        self.SPEC.disconnect(self=self.SPEC)


if __name__ == "__main__":
    TempList = []
    PA = PA_Test

    PA.PA_channel_current_test_init(self=PA)

    MXD2670 = HCI_For_Serial.HCI_Serial
    MXD2670.HCI_serial_port_refresh(self=MXD2670)
    MXD2670.HCI_port_init(self=MXD2670, port=HCI_para.PORT, bps=115200, timeout=2)

    VMD_data = Result_data()
    LP_data = Result_data()

    for Capnum in range(32):
        # power mode 0 == LP , Power mode 1 == VMD
        MXD2670.HCI_pa_power_rfio_cap(self=MXD2670, power_mode=1, RfioCapacitor = Capnum)

        ########## VMD  ##########
        DATA = Result_data()
        result_data = Result_data()
        count = 0
        FreqMHzIdx = 2452
        # for FreqMHzIdx in range(StartMHz, StopMHz, 2):
        TempList = PA.PA_channel_current(self=PA, ChFreqMHz=FreqMHzIdx, ACW=255, VDD_RF=1.3 + 0.12,
                                             LdoVco=HCI_For_Serial.VcoPowerDef.LDO_VCO_900mV,
                                             LdoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV,
                                             TxPwr=HCI_For_Serial.TxPowerDef.TX_10_DBM)
        print('ChannelFreq:', Capnum,
                  'OutputPower:', '{:.2f}'.format(TempList[0]), 'dBm ', 'RFCurrent:',
                  '{:.2f}'.format(TempList[1]), 'mA')
        VMD_data.fre_index[Capnum] = Capnum
        VMD_data.ReadPowerDBM[Capnum] = round(TempList[0], 2)
        VMD_data.VddRFCurrentMA[Capnum] = round(TempList[1], 2)

            # print('ChannelFreq:', DATA.fre_index,
            #       'OutputPower:', DATA.ReadPowerDBM, 'dBm ', 'RFCurrent:',
            #       DATA.VddRFCurrentMA, 'mA')

            # time.sleep(0.2)

        ########## LP  ##########
        MXD2670.HCI_pa_power_rfio_cap(self=MXD2670, power_mode=0, RfioCapacitor=Capnum)
        DATA2 = Result_data()
        result_data2 = Result_data()
        PA.PA_channel_current_test_init(self=PA)

        FreqMHzIdx = 2452

        TempList = PA.PA_channel_current(self=PA, ChFreqMHz=FreqMHzIdx, ACW=255, VDD_RF=1.3 + 0.12,
                                         LdoVco=HCI_For_Serial.VcoPowerDef.LDO_VCO_900mV,
                                         LdoRf=HCI_For_Serial.LdoRfDef.LDO_RF_1200mV,
                                         TxPwr=HCI_For_Serial.TxPowerDef.TX_0_DBM)
        print('ChannelFreq:', Capnum,
              'OutputPower:', '{:.2f}'.format(TempList[0]), 'dBm ', 'RFCurrent:',
              '{:.2f}'.format(TempList[1]), 'mA')
        LP_data.fre_index[Capnum] = Capnum
        LP_data.ReadPowerDBM[Capnum] = round(TempList[0], 2)
        LP_data.VddRFCurrentMA[Capnum] = round(TempList[1], 2)
            # print('ChannelFreq:', DATA.fre_index,
            #       'OutputPower:', DATA.ReadPowerDBM, 'dBm ', 'RFCurrent:',
            #       DATA.VddRFCurrentMA, 'mA')

            # time.sleep(0.2)

    PA.PA_test_end(self=PA)


    OUTPUT_path = 'D:\\RF_CAP\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime(
            'PA_VMD_TxPwr_Cap_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    WRITER_DATA_IDEX = {'Cap value': VMD_data.fre_index}
    WRITER_DATA_POWER = {'Tx_Power\n(Mhz)': VMD_data.ReadPowerDBM}
    WRITER_DATA_CURRENT = {'RF_Current\n(deg)': VMD_data.VddRFCurrentMA}

    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    ALL_DATA = dict(**WRITER_DATA_IDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    # print(ALL_DATA)

    result_data = pd.DataFrame(ALL_DATA)
    result_data.to_excel(writer, 'Tx_Power', float_format='%.5f')
    writer.save()
    writer.close()


    OUTPUT_path2 = 'D:\\RF_CAP\\'
    OUTPUT_end2 = BoardNum
    OUTPUT_form2 = '.xlsx'
    writer2 = pd.ExcelWriter(
        OUTPUT_path2 + datetime.now().strftime(
            'PA_LP_TxPwr_Cap_' + Temp + '_' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end2 + OUTPUT_form2)
    WRITER_DATA_IDEX2 = {'Cap value': LP_data.fre_index}
    WRITER_DATA_POWER2 = {'Tx_Power\n(Mhz)': LP_data.ReadPowerDBM}
    WRITER_DATA_CURRENT2 = {'RF_Current\n(deg)': LP_data.VddRFCurrentMA}

    # ALL_DATA = dict(**WRITER_DATA_INDEX, **WRITER_DATA_POWER, **WRITER_DATA_CURRENT)
    ALL_DATA2 = dict(**WRITER_DATA_IDEX2, **WRITER_DATA_POWER2, **WRITER_DATA_CURRENT2)
    # print(ALL_DATA)

    result_data2 = pd.DataFrame(ALL_DATA2)
    result_data2.to_excel(writer2, 'Tx_Power', float_format='%.5f')
    writer2.save()
    writer2.close()


