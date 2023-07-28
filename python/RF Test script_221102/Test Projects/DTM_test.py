import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _RS_CMW500
from HCI import HCI_For_Serial

Configs = _RS_CMW500.Configs

CMW_TCPIP = 'TCPIP::192.168.190.63::INSTR'
BoardNum = 'ALL_test_-45°#1'

Channel_range = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                 30, 31, 32, 33, 34, 35, 36, 37, 38, 39)
ACi_channel = (3,15,37)
Inband_channel = (2,19,37)
# Inband_channel = Channel_range

class Result_offset_carrier:
    FRE_ACC = np.array(np.zeros(1*40))
    FRE_OFF = np.array(np.zeros(1*40))
    FRE_DRI = np.array(np.zeros(1*40))
    MAX_DRI = np.array(np.zeros(1*40))
    INI_FRE_DRI = np.array(np.zeros(1*40))
    DF2_99 = np.array(np.zeros(1*40))      # %99 △F2

class Result_modulation:
    DF1_AVG = np.array(np.zeros(1*40))
    DF1_99 = np.array(np.zeros(1*40))
    DF2_99 = np.array(np.zeros(1*40))
    DF2_AVG = np.array(np.zeros(1*40))


class Result_per_search:
    Rx_1M = np.array(np.zeros(1*40))
    Rx_2M = np.array(np.zeros(1*40))
    Rx_S2 = np.array(np.zeros(1*40))
    Rx_S8 = np.array(np.zeros(1*40))

class DTM_test_mode:
    LE1M = 1
    LE2M = 2
    LES2 = 3
    LES8 = 4

def Tx_mode_test(self,mode,writer):
    if(mode == 1):
        name = '1M'
    elif( mode == 2 ):
        name = '2M'
    elif( mode == 4 ):
        name = 'S8'
    FRE_ACC = np.array(np.zeros(1*40))
    FRE_OFF = np.array(np.zeros(1*40))
    FRE_DRI = np.array(np.zeros(1*40))
    MAX_DRI = np.array(np.zeros(1*40))
    INI_FRE_DRI = np.array(np.zeros(1*40))
    DF2_99 = np.array(np.zeros(1*40))      # %99 △F2
    self.offset_carrier_mode(self=self, test_mode=mode)
    for CH in Channel_range:
        # self.stop_mev(self=self)
        time.sleep(0.1)
        self.offset_carrier_channel(self=self, CH=CH)
        temp_data = self.offset_carrier_get_data(self=self)
        DF2_99[CH] = temp_data[0]
        FRE_ACC[CH] = temp_data[1]
        FRE_DRI[CH] = temp_data[2]
        MAX_DRI[CH] = temp_data[3]
        FRE_OFF[CH] = temp_data[4]
        INI_FRE_DRI[CH] = temp_data[5]
    
    self.stop_mev(self=self)
    DF1_AVG_mod = np.array(np.zeros(1 * 40))
    DF1_99_mod = np.array(np.zeros(1 * 40))
    DF2_99_mod = np.array(np.zeros(1 * 40))
    DF2_AVG_mod = np.array(np.zeros(1 * 40))
    self.modulation_mode(self=self, test_mode=mode)
    for CH in Channel_range:
        # self.stop_mev(self=self)
        time.sleep(0.1)
        self.modulation_channel(self=self, CH=CH)
        temp_data = self.modulation_get_data(self=self)
        # ('Data_Fram is: DF1_AVG; DF2_99; DF2_AVG')
        # S8 ('Data_Fram is: DF1_AVG; DF1_99')
        if( mode == 4):
            DF1_AVG_mod[CH] = temp_data[0]
            DF1_99_mod[CH] = temp_data[1]
        else:
            DF1_AVG_mod[CH] = temp_data[0]
            DF2_99_mod[CH] = temp_data[1]
            DF2_AVG_mod[CH] = temp_data[2]
    
    self.stop_mev(self=self)
    Base_freq = np.array(np.ones(len(Channel_range))*2402)
    Freq_index = Base_freq + np.array(Channel_range)*2
    Frequence = {'Frequence (Mhz)': Freq_index}
    RESULT_DF1_AVG = { 'DF1_AVG': DF1_AVG_mod/1000 }
    RESULT_DF2_99 = { 'DF2_99': DF2_99_mod/1000 }
    RESULT_DF1_DF2 = { 'df2/df1': DF2_AVG_mod/DF1_AVG_mod }
    RESULT_FRE_ACC = { 'Freq_ACC': FRE_ACC/1000 }
    RESULT_FRE_OFF = { 'Freq_offset': FRE_OFF/1000 }
    RESULT_FRE_DRI = { 'Freq_drift': FRE_DRI/1000 }
    RESULT_MAX_DRI = { 'Max_drift': MAX_DRI/1000 }
    RESULT_INI_FRE_DRI = { 'Initial_drift': INI_FRE_DRI/1000 }
    RESULT_ALL = dict(**Frequence, **RESULT_DF1_AVG, **RESULT_DF2_99, **RESULT_DF1_DF2, **RESULT_FRE_ACC, **RESULT_FRE_OFF, **RESULT_FRE_DRI, **RESULT_MAX_DRI, **RESULT_INI_FRE_DRI)
    result_data = pd.DataFrame(RESULT_ALL)
    result_data.to_excel(writer, 'DTM TX@'+name, float_format='%.2f')

def inband_test(self,mode,writer):
    if( mode == 1 ):
        name = '1M'
    else:
        name = '2M'
    Result = np.matrix(np.zeros(81 * 40).reshape(81, 40))
    self.inband_mode(self=self, test_mode=mode)
    for CH in Inband_channel:
        temp_data = self.inband_get_data(self=self, CH=CH)
        Result[0:,CH] = temp_data
    self.stop_mev(self=self)
    data = pd.DataFrame(Result)
    data.to_excel(writer, 'In-band_' + name , float_format='%.2f')

def Tx_mode_test_all(self,writer):
    # Tx_mode_test(self=self, mode=1, writer=writer)
    Tx_mode_test(self=self, mode=2, writer=writer)
    # Tx_mode_test(self=self, mode=4, writer=writer)
    self.mev_close(self=self)


def Per_search_test_all(self,writer):
    ACC_1M = self.per_search_test(self=self, Channel= Channel_range, mode=1)
    self.stop_per(self=self)
    ACC_2M = self.per_search_test(self=self, Channel= Channel_range, mode=2)
    self.stop_per(self=self)
    ACC_S2 = self.per_search_test(self=self, Channel= Channel_range, mode=3)
    self.stop_per(self=self)
    ACC_S8 = self.per_search_test(self=self, Channel= Channel_range, mode=4)
    self.stop_per(self=self)
    Base_freq = np.array(np.ones(len(Channel_range))*2402)
    Freq_index = Base_freq + np.array(Channel_range)*2
    RESULT_FREQ_INDEX = {'Freq (MHz)' : Freq_index}
    RESULT_PER_ACC1M = {'1M': ACC_1M}
    RESULT_PER_ACC2M = {'2M': ACC_2M}
    RESULT_PER_ACCS2 = {'S2': ACC_S2}
    RESULT_PER_ACCS8 = {'S8': ACC_S8}
    RESULT_PER_ACC = dict(**RESULT_FREQ_INDEX, **RESULT_PER_ACC1M, **RESULT_PER_ACC2M, **RESULT_PER_ACCS2, **RESULT_PER_ACCS8)
    # RESULT_PER_ACC = dict(**RESULT_FREQ_INDEX, **RESULT_PER_ACC1M)#, **RESULT_PER_ACC2M, **RESULT_PER_ACCS2, **RESULT_PER_ACCS8)

    data = pd.DataFrame(RESULT_PER_ACC)  # )#
    data.to_excel(writer, 'per_serach', float_format='%.2f')  # ‘page_1’是

def single_per_tset(self,writer,mode):
    ACC_1M = self.per_search_test(self=self, Channel= Channel_range, mode=mode)
    self.stop_per(self=self)
    Base_freq = np.array(np.ones(len(Channel_range)) * 2402)
    Freq_index = Base_freq + np.array(Channel_range) * 2
    RESULT_FREQ_INDEX = {'Freq (MHz)': Freq_index}
    RESULT_PER_ACC1M = {'1M': ACC_1M}
    RESULT_PER_ACC = dict(**RESULT_FREQ_INDEX, **RESULT_PER_ACC1M)#, **RESULT_PER_ACC2M, **RESULT_PER_ACCS2, **RESULT_PER_ACCS8)

    data = pd.DataFrame(RESULT_PER_ACC)  # )#
    data.to_excel(writer, 'per_serach', float_format='%.2f')  # ‘page_1’是


def Inband_test_all(self,writer):
    inband_test(self=self, mode=1, writer=writer)
    self.mev_close(self=self)
    inband_test(self=self, mode=2, writer=writer)
    self.mev_close(self=self)

def Aci_write_data(data, writer, name):
    Base_freq = np.array(np.ones(len(ACi_channel))*2402)
    Freq_index = Base_freq + np.array(Channel_range)*2
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


def Aci_test_all(self,CH, writer):
    Result_1M = self.hci_aci_test(self=self, CH=CH, test_mode=DTM_test_mode.LE1M)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_1M, writer=writer, name='1M')
    Result_2M = self.hci_aci_test(self=self, CH=CH, test_mode=DTM_test_mode.LE2M)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_2M, writer=writer, name='2M')
    Result_S2 = self.hci_aci_test(self=self, CH=CH, test_mode=DTM_test_mode.LES2)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_S2, writer=writer, name='S2')
    Result_S8 = self.hci_aci_test(self=self, CH=CH, test_mode=DTM_test_mode.LES8)
    self.hci_aci_stop(self=self)
    Aci_write_data(data=Result_S8, writer=writer, name='S8')




if __name__ == "__main__":
    print('Test start.')
    Configs.RETRY = 0
    Configs.RFOUTPUT = '22.0'
    Configs.RFINPUT = '22.0'
    Configs.PACKAGELEN = '200'
    Configs.RSBAUDRATE = 'B115K'
    RCMW500 = _RS_CMW500.RS_CMW500
    RCMW500.__init__(self=RCMW500)
    RCMW500.CMW500_connect( self=RCMW500, TCPIP=CMW_TCPIP)

    OUTPUT_path = 'D:\\DTM_TRX\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime(
            'DTM_TEST_200包' + '_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    # single_per_tset(self=RCMW500, writer=writer, mode=1)

    RCMW500.mev_close(self=RCMW500)
    Tx_mode_test_all(self=RCMW500, writer=writer)
    # Inband_test_all(self=RCMW500, writer=writer)
    RCMW500.mev_close(self=RCMW500)

    # Per_search_test_all(self=RCMW500, writer=writer)
    Aci_test_all(self=RCMW500, CH=ACi_channel, writer=writer)
    RCMW500.stop_per(self=RCMW500)
    writer.save()
    writer.close()