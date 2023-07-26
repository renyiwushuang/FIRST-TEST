# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:16:16 2023

@author: E002012
"""

import scipy.io as scio
# import scipy.fft as fft
import matplotlib.pyplot as plt
import numpy as np

dataFile = 'F:/work/uwb/测试/yjzM2片内ADC数据/data20230726/#12NI8.1GHz_att40_-45dBm_agc6_RX3.mat'
data = scio.loadmat(dataFile)
iq_pre = data['iq_data'].T[0][0:4096]
iq_data = iq_pre - np.mean(iq_pre)
# plt.plot(iq_data.real, marker='o', markersize=8)
# plt.plot(iq_data.imag, marker='x', markersize=8)

fftdata = np.fft.fft(iq_data)



# t = np.arange(0, 1, 0.001)
# signal = np.sin(2*np.pi*5*t)
# fftdata = np.fft.fft(signal)
# plt.plot(fftdata)

sample_rate = 899.4e6
fre_offset = 1
fre = np.fft.fftfreq(len(fftdata), d=1/sample_rate)
plt.plot(abs(fftdata))
max_index = np.argmax(abs(fftdata))
fftpower = np.square(abs(fftdata))
sigpower = sum(abs(fftpower)[max_index-fre_offset:max_index+fre_offset])
noisepower = sum(abs(fftpower)[10:max_index-fre_offset]) + sum(abs(fftpower)[max_index+fre_offset:len(fftdata)])
snr = sigpower / noisepower
snr_dB = 10*np.log10(snr)
print(snr_dB)