# -*- coding: utf-8 -*-

import pyvisa as visa
import time


class Signalgenerator:

    def __init__(self):
        self.rm = None
        self.N5181A = None

    def instr_init(self, TCPIP):
        self.rm = visa.ResourceManager()
        self.N5181A = self.rm.open_resource(TCPIP)

    def instr_output_on(self):
        self.N5181A.write('OUTP:STAT ON')

    def instr_output_off(self):
        self.N5181A.write('OUTP:STAT OFF')

    def set_output_para(self, FreqMHz, PowerDBM):
        self.N5181A.write('FREQ ' + str(FreqMHz * 1000000))
        self.N5181A.write('POW ' + str(PowerDBM) + 'dBm')

    def close(self):
        self.N5181A.close()
        self.rm.close()
