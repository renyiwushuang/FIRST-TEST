# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:51:16 2019

@author: Administrator
"""
import serial
import visa
from bs4 import BeautifulSoup



f = open('serialconfig.html','r',encoding='utf-8')
ff = f.read()
soup = BeautifulSoup(ff,'lxml')

visa_dll = soup.find('visa',id= 'visa32_dll_addr').value.get_text()
tcp_addr = soup.find('visa',id= 'tcp_addr').value.get_text()
rm = visa.ResourceManager(visa_dll)
tcp_inst = rm.open_resource(tcp_addr)
print(tcp_inst.query('*IDN?'))
print(tcp_inst.query(':TRIGger:STATus?'))


portx = soup.find('serial',id= 'port').value.get_text()
bps = int(soup.find('serial',id= 'bps').value.get_text())
waitTime =int(soup.find('serial',id= 'waittime').value.get_text())
ser = serial.Serial(portx,bps,timeout = waitTime)
flag = tcp_inst.query(':TRIGger:STATus?')
while flag=='WAIT\n' :
    s = ser.readline()
    print(s)
    flag = tcp_inst.query(':TRIGger:STATus?')

print('Triged')
ser.close()
