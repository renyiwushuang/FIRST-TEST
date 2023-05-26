import time
import _Agilent34410A_multimeter


METER_IP = 'TCPIP::169.254.4.10::inst0::INSTR'

if __name__ == '__main__':
    CUR = _Agilent34410A_multimeter.Multimeter
    CUR.meter_init(self=CUR, TCPIP=METER_IP)
    CUR.config_to_dci_mode(self=CUR)
    current_mA = CUR.get_current_mA(self=CUR)
    print('{:.2f}'.format(current_mA))
    CUR.close(self=CUR)

    currentMeter = _Agilent34410A_multimeter.Multimeter
    currentMeter.meter_init(self=currentMeter, TCPIP=METER_IP)
    currentMeter.config_to_dci_mode(self=currentMeter)
    current_mA = currentMeter.get_current_mA(self=currentMeter)
    print('{:.2f}'.format(current_mA))
    CUR.close(self=currentMeter)
