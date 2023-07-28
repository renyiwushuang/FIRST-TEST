# -*- coding: utf-8 -*-

import pyvisa as visa
import time


class Multimeter:

    def __init__(self):
        self.rm = None
        self.E34401A = None

    def meter_init(self, TCPIP):
        self.rm = visa.ResourceManager()
        self.E34401A = self.rm.open_resource(TCPIP)

    def config_to_dci_mode(self):
        config = self.E34401A.query('CONF?')
        mtype = config.find('CURR')
        if mtype == -1:
            self.E34401A.write('CONF:CURR:DC')
            time.sleep(0.8)

    def get_current_mA(self):
        config = self.E34401A.query('CONF?')
        mtype = config.find('CURR')
        current = -99
        if mtype == 1:
            ocp_flg = self.E34401A.query_ascii_values('*OPC?')
            #            print(ocp_flg)
            if ocp_flg == [1.0]:
                current = self.E34401A.query_ascii_values('READ?')
            #                print("read current:", current)
            #                print(__name__, "read current:", '{:.10f}'.format(current[0]))
            else:
                print(__name__, "meter can not operation!!!")
        else:
            print(__name__, "meter mode error!!!")
        # return value unit: mA
        return current[0] * 1000

    def close(self):
        self.E34401A.close()
        self.rm.close()
