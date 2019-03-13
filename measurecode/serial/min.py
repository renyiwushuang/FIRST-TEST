# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:51:16 2019

@author: Administrator
"""
#import serial
import visa

visa_dll = 'c:/windows/system32/visa32.dll'
tcp_addr = 'TCPIP::192.168.6.100::inst0::INSTR'
rm = visa.ResourceManager(visa_dll)
tcp_inst = rm.open_resource(tcp_addr)
print(tcp_inst.query('*IDN?'))
print(tcp_inst.query(':TRIGger:STATus?'))

'''
portx = 'COM3'
bps = 460800
waitTime = 1
ser = serial.Serial(portx,bps,timeout = waitTime)
flag = tcp_inst.query(':TRIGger:STATus?')
while flag=='WAIT\n' :
    s = ser.readline()
    print(s)
    flag = tcp_inst.query(':TRIGger:STATus?')

print('Triged')
ser.close()'''