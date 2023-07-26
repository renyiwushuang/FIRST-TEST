import pyvisa as visa
import time
import warnings
import string
import sys
import numpy as np


class class_config:
    RFOUTPUT = '22.0'
    RFINPUT = '22.0'
    RFLEVEL = '-40.0'
    RFEXPECTEDPW = '10.0'
    RSCOM = 'COM2'
    RSBAUDRATE = 'B115K'
    PROTOCOL = 'NONE'
    SIGNALTYPE = 'PRBS9'
    SIGNALLEN = '37'
    HWINTERFACE = 'RS232'
    HWPROTOCOL = 'HCI'
    RFCOM = '0'
    PARITY = 'NONE'
    RETRY = 0
    # Test mode chose, will be writen in test case;
    TESTMODE = 'Receiver 1M'  # End with no space.
    PACKAGELEN = '200'
    # Setting param: PER_Search
    PER_SET = 30.8
    START_LEVEL = -112.0
    END_LEVEL = -60.0
    INIT_STATUS = 0
    SET_GAP = 0.2
    ACI_STEP = 1
    ACI_EMAGE_PW = -67
    ACI_LOSS = 8


global Configs
Configs = class_config()


class DTM_test_mode:
    LE1M = 1
    LE2M = 2
    LES2 = 3
    LES8 = 4


sleep_time = 0.3


class RS_CMP200:
    def __init__(self):
        self.rm = None
        self.CMP200 = None
        self.testmode = None
        # open connection to power supply

    def cmd_send(self, cmd):
        res = 0
        self.CMP200.write(cmd)
        while(res == 0):
            res = self.CMP200.query('*OPC?')  # *OPC?命令用于查询当前操作是否完成。
            time.sleep(0.03)

    def CMP200_connect(self, TCPIP):
        self.rm = visa.ResourceManager()
        self.CMP200 = self.rm.open_resource(TCPIP)
        self.CMP200.timeout = 25000

    def systemreset(self):
        self.CMP200.cmd_send('*RST')
        self.CMP200.cmd_send('*CLS')


if __name__ == '__main__':
    CMP_TCPIP = 'TCPIP::192.168.190.63::hislip0::INSTR'
    CMP200 = RS_CMP200
    CMP200.__init__(self=CMP200)
    CMP200.CMP200_connect(self=CMP200, TCPIP=CMP_TCPIP)
    CMP200.systemreset()
