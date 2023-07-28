import time
import _E36312A_power


P0WER_CONFIG_OFFSET = 0.005
POWER_TAB = [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30]
POWER_SUPPLY_IP = 'TCPIP::169.254.174.241::inst0::INSTR'

def as_num(x):
    y = '{:.6f}'.format(x)  # .10f 保留10位小数
    return y


if __name__ == '__main__':
    E363 = _E36312A_power.Waveform
    """
    E363.__init__(self=E363, TCPIP=POWER_SUPPLY_IP)
    E363.set_ch1_voltage(self=E363, vol=1.25, cur=1)
    E363.power_ch1_on(self=E363)
    time.sleep(2)
    print('{:.3f}'.format(E363.get_ch1_voltage(self=E363)))
    print('{:.6f}'.format(E363.get_ch1_current(self=E363)))
    E363.power_ch1_off(self=E363)
    E363.close(self=E363)
"""

   # E363.__init__(self=E363, TCPIP=POWER_SUPPLY_IP)
    E363.__init__(self=E363, TCPIP=POWER_SUPPLY_IP)
    E363.set_ch1_voltage(self=E363, vol=(POWER_TAB[0]+P0WER_CONFIG_OFFSET), cur=0.5)
    E363.power_ch1_on(self=E363)
    for index in range(len(POWER_TAB)):
        E363.set_ch1_voltage(self=E363, vol=(POWER_TAB[index]+P0WER_CONFIG_OFFSET), cur=0.5)
        time.sleep(3)
        VOUT = E363.get_ch1_voltage(self=E363)
        print("voltage set:", POWER_TAB[index], "out:",VOUT)
    E363.power_ch1_off(self=E363)
    E363.close(self=E363)

    E363.__init__(self=E363, TCPIP=POWER_SUPPLY_IP)
    E363.set_ch1_voltage(self=E363, vol=(3.3+P0WER_CONFIG_OFFSET), cur=0.5)
    E363.power_ch1_on(self=E363)




