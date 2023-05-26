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

if __name__ == "__main__":
    print('Test start.')
    Configs.RETRY = 0
    Configs.RFOUTPUT = '22.0'
    Configs.RFINPUT = '22.0'
    Configs.PACKAGELEN = '200'
    Configs.RSBAUDRATE = 'B115K'

    RCMW500 = _RS_CMW500.RS_CMW500
    RCMW500.__init__(self=RCMW500)
    RCMW500.CMW500_connect(self=RCMW500, TCPIP=CMW_TCPIP)

    channel = 20
    level = -20
    freq = 2402 + channel*2

    RCMW500.hci_aci_mode(self=RCMW500 , test_mode=_RS_CMW500.DTM_test_mode.LE1M)
    RCMW500.hci_aci_channel(self=RCMW500, CH=channel)
    RCMW500.hci_aci_interferer_freq(self=RCMW500, freqMHz=freq-1)
    RCMW500.hci_aci_interferer_level( self=RCMW500, level=level )

