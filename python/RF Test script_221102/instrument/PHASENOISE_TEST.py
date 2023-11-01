import time
import _AgilentE5052B_signalsource
import xlsxwriter

TCPIP = 'TCPIP::192.168.190.32::INSTR'

if __name__ == '__main__':

    SSA = _AgilentE5052B_signalsource.Agilent_E5052B
    SSA.spectrum_init(self=SSA, TCPIP=TCPIP)
    SSA.identity(self=SSA)
    SSA.spectrum_config(self=SSA)
    SSA.updateMarker(self=SSA, Marker1='1000', Marker2='10000', Marker3='100000', Marker4='1000000', Marker5='10000000')
    print(SSA.getMarkerdBcHz(self=SSA))
    print(SSA.getDeg(self=SSA))
    print(SSA.getPowerDBM(self=SSA))
    print(SSA.getFreqkHz(self=SSA))
    time.sleep(0.5)
    SSA.disconnect(self=SSA)





