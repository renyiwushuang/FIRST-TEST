import time
import _AgilentN9020A_spectrum

TCPIP = 'TCPIP::169.254.74.249::INSTR'

if __name__ == '__main__':

    SPEC = _AgilentN9020A_spectrum.Agilent_MXA_N9020A
    SPEC.spectrum_init(self=SPEC, TCPIP=TCPIP)
    SPEC.identity(self=SPEC)
    SPEC.getInitialParamsAgilent(self=SPEC)
    SPEC.setSpanMHz(self=SPEC, span=2)
    SPEC.setCentralFreqMHz(self=SPEC, centralFreq=2440)
    time.sleep(0.5)
    peak_power = SPEC.getMaxFreqPower(self=SPEC)
    print(peak_power)
    SPEC.setCentralFreqMHz(self=SPEC, centralFreq=4880)
    time.sleep(0.5)
    peak_power = SPEC.getMaxFreqPower(self=SPEC)
    print(peak_power)
    SPEC.setCentralFreqMHz(self=SPEC, centralFreq=7320)
    time.sleep(0.5)
    peak_power = SPEC.getMaxFreqPower(self=SPEC)
    print(peak_power)
#    SPEC.plotInfoAgilent(self=SPEC)
    SPEC.disconnect(self=SPEC)





