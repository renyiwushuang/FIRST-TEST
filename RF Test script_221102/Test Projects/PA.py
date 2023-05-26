import numpy as np
import pandas as pd
import time
from datetime import datetime
from instrument import _AgilentN5181A_signalgenerator,_AgilentN9020A_spectrum


SG_TCPIP = 'TCPIP::192.168.190.19::INSTR'
PSA_TCPIP = 'TCPIP::192.168.190.122::INSTR'
BoardNum = '#线损1_2'
power = 0


if __name__ == "__main__":

    SG = _AgilentN5181A_signalgenerator.Signalgenerator
    SG.instr_init(self=SG, TCPIP=SG_TCPIP)
    SG.set_output_para(self=SG, FreqMHz=2402, PowerDBM=0)
    SG.instr_output_on(self=SG)

    SPEC = _AgilentN9020A_spectrum.Agilent_MXA_N9020A
    SPEC.spectrum_init(self=SPEC, TCPIP=PSA_TCPIP)
    SPEC.identity(self=SPEC)
    SPEC.getInitialParamsAgilent(self=SPEC)

    freq_range = np.linspace(2402, 2480, 40)
    result = np.array(np.zeros(len(freq_range)))
    for i in range(len(freq_range)):
        SG.set_output_para(self=SG, FreqMHz=freq_range[i], PowerDBM=0)
        time.sleep(0.1)
        SPEC.setSpanMHz(self=SPEC, span=2)
        SPEC.setCentralFreqMHz(self=SPEC, centralFreq=freq_range[i])
        time.sleep(0.5)
        peak_power = SPEC.getMaxFreqPower(self=SPEC)
        result[i] = float(peak_power) - power

    OUTPUT_path = 'D:\\'
    OUTPUT_end = BoardNum
    OUTPUT_form = '.xlsx'
    writer = pd.ExcelWriter(
        OUTPUT_path + datetime.now().strftime('POWER_0dBm_%Y-%b-%d-%H-%M-%S') + OUTPUT_end + OUTPUT_form)

    FREQ = {'Freq (MHz)': freq_range}
    POWER_DRI = {'POWER(0dBm)': result}
    ALL_DATA = dict(**FREQ, **POWER_DRI)
    data = pd.DataFrame(ALL_DATA)
    data.to_excel(writer, 'POWER (0dBm)', float_format='%.2f')

    writer.save()
    writer.close()






