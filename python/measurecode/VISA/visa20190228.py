# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 18:21:01 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:28:16 2019

@author: Administrator
"""
import matplotlib.pyplot as plt
import visa
import numpy

visa_dll = 'c:/windows/system32/visa32.dll'
tcp_addr = 'TCPIP::169.254.250.113::inst0::INSTR'
rm = visa.ResourceManager(visa_dll)
tcp_inst = rm.open_resource(tcp_addr)
print(tcp_inst.query('*IDN?'))
print(tcp_inst.query(':TRIGger:STATus?'))

i= 0
while i <3 :
    if tcp_inst.query(':TRIGger:STATus?') == 'STOP\n' :
        tcp_inst.write(':STOP')
        tcp_inst.write(':WAV:SOUR CHAN2')
        tcp_inst.write(':WAV:MODE RAW')
        tcp_inst.write(':WAV:FORM WORD')


        over = True

        starpoint = 1
        step = 100000
        data = numpy.array([0])

        while over:
            if starpoint > 1000000 :
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
        plt.savefig('D:/'+str(i)+'temp.svg')
        
        i=i+1
        tcp_inst.write(':SINGLe')

print('happy end')        
'''tcp_inst.write(':WAV:STAR 201')
tcp_inst.write(':WAV:STOP 400')

print('2')1100012

#data1 = tcp_inst.query_binary_values(':WAV:DATA?',datatype='h')
#plt.plot(data1)'''


