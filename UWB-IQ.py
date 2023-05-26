# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import pandas as pd
import h5py
import matplotlib.pyplot as plt
import numpy as np
file_addr = 'F:/work/uwb/DATA/FPGA_ADC_DATA/I1Q2-uwbsample-50us.h5'

f = h5py.File(file_addr, 'r')
'''
for key in f.keys():
    print(f[key].name)
for key in f["Waveforms"].keys():   
    print(key)
'''

data = f['Waveforms']['Channel 1']['Channel 1Data']
data_abs = np.abs(f['Waveforms']['Channel 1']['Channel 1Data'])#将幅度取模，消除负值抵消
data1 = data_abs[2243979:3545382]#截取一段preamble
data1_1 = []
for i in range(160):#采样时钟是20G，8ns周期对应160个样本点。按周期截取数据
    data1_1.append(data1[i:320000+i:160])

heatarray = np.array(data1_1)#获取热力图矩阵

plt.imshow(heatarray, cmap='coolwarm', origin='upper', aspect="auto")
plt.show()
'''
画出来的热力图偏转，是因为实际信号的频率为124.8MHz，对应周期为8.012ns，
当取160点是频偏最小，对一个点少一个点都会导致频偏增大，彩色部分会由斜线变到垂直


'''