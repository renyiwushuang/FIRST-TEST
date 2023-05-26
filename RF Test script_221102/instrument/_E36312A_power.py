import pyvisa as visa
import time
import warnings


class Waveform:
    def __init__(self):
        self.rm = None
        self.E36312A = None
        # open connection to power supply

    def power_init(self, TCPIP):
        self.rm = visa.ResourceManager()
        self.E36312A = self.rm.open_resource(TCPIP)

    def set_parameters(self):
        # set the power supply channel 1 to 1V and 0.01A current limit
        self.E36312A.write(':APPLy %s,%G,%G' % ('CH1', 2.0, 2))
        # turn on output for channel 1
        self.E36312A.write(':OUTPut:STATe %d' % (1))
        # wait for 500ms for the output to stabilize
        time.sleep(0.5)

    def set_ch1_voltage(self, vol, cur):
        if cur == 0:
            cur = 1
        # set the voltage measurement for channel 1 to use the external sense line
        self.E36312A.write(':SOURce:VOLTage:SENSe:SOURce %s,(%s)' % ('INTernal', '@1'))
        # set the power supply channel 1 to 1V and 0.01A current limit
        self.E36312A.write(':APPLy %s,%G,%G' % ('CH1', vol, cur))

    def power_ch1_on(self):
        self.E36312A.write(':APPLy %s' % 'CH1')
        # turn on output for channel 1
        self.E36312A.write(':OUTPut:STATe %d' % (1))
        # wait for 500ms for the output to stabilize
        time.sleep(0.3)

    def power_ch1_off(self):
        self.E36312A.write(':APPLy %s' % 'CH1')
        # Turn off channels
        self.E36312A.write(':OUTPut:STATe %d' % (0))

    def get_ch1_voltage(self):
        self.E36312A.write(':APPLy %s' % 'CH1')
        voltage = self.E36312A.query_ascii_values(':MEASure:SCALar:VOLTage:DC? (%s)' % ('@1'))
        # print("Voltage ", voltage)
        return voltage[0]

    def get_ch1_current(self):
        self.E36312A.write(':APPLy %s' % 'CH1')
        # measure the current
        current = self.E36312A.query_ascii_values(':MEASure:SCALar:CURRent:DC? (%s)' % ('@1'))
        # print("Current ", current)
        return current[0]

    def get_ch1_resistance(self):
        voltage = self.get_ch1_voltage()
        current = self.get_ch1_current()
        return voltage / current

    def close(self):
        self.E36312A.close()
        self.rm.close()

if __name__ == "__main__":
    print("power supply test")
    PWR = Waveform
    # Waveform.power_init(self=PWR, TCPIP='TCPIP::192.168.190.74::inst0::INSTR')
    Waveform.power_init(self=PWR, TCPIP='TCPIP::192.168.190.74::inst0::INSTR')