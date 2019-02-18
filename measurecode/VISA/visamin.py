# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:28:16 2019

@author: Administrator
"""

import visa

visa_dll = 'c:/windows/system32/visa32.dll'
tcp_addr = 'TCPIP::192.168.7.175::inst0::INSTR'
rm = visa.ResourceManager(visa_dll)
tcp_inst = rm.open_resource(tcp_addr)
print(tcp_inst.query('*IDN?'))
print(tcp_inst.query(':TRIGger:STATus?'))