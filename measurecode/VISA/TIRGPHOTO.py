# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:27:28 2019

@author: Administrator
"""
import matplotlib.pyplot as plt
import pyvisa
import numpy

visa_dll = 'c:/windows/system32/visa32.dll'
tcp_addr = 'TCPIP::169.254.250.113::inst0::INSTR'
rm = pyvisa.ResourceManager(visa_dll)
tcp_inst = rm.open_resource(tcp_addr)
print(tcp_inst.query('*IDN?'))
print(tcp_inst.query(':TRIGger:STATus?'))
tcp_inst.write(':STOP')
tcp_inst.write(':WAV:SOUR CHAN2')
tcp_inst.write(':WAV:MODE RAW')
tcp_inst.write(':WAV:FORM WORD')


over = True

starpoint = 1
step = 250000
data = numpy.array([0])
while over:
    if starpoint > 5500000 :
        over = False
    tcp_inst.write(':WAV:STAR '+str(starpoint))
    tcp_inst.write(':WAV:STOP '+str(starpoint+step))
    starpoint = starpoint+step 
    print('1')
    data = numpy.append(data,tcp_inst.query_binary_values(':WAV:DATA?',datatype='h',container=numpy.array))


yincrement = tcp_inst.query_ascii_values(':WAVeform:YINCrement?')
yorigin = tcp_inst.query_ascii_values(':WAVeform:YORigin?')
yreference = tcp_inst.query_ascii_values(':WAVeform:YREFerence?')
dataf = (data-yorigin[0]-yreference[0])*yincrement[0]
#data = tcp_inst.query_binary_values(':WAV:DATA?')
plt.plot(dataf,linewidth=0.01)
plt.savefig('D:/data/photo.svg')
numpy.save('D:/data/photo.out',dataf)
