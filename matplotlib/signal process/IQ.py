# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:16:16 2023

@author: E002012
"""

import scipy.io as scio
# import scipy.fft as fft
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def snr_dB(inputdata):
    fre_offset = 25
    max_index = np.argmax(abs(inputdata))
    fftpower = np.square(abs(inputdata))
    sigpower = sum(abs(fftpower)[max_index-fre_offset:max_index+fre_offset])
    noisepower = sum(abs(fftpower)[10:max_index-fre_offset]) + sum(abs(fftpower)[max_index+fre_offset:len(fftdata)])
    snr = sigpower / noisepower
    snr_dB = 10*np.log10(snr)
    return snr_dB



0dataFile = 'F:\\work\\uwb\\测试\\UWB_matlab_mcu\\yjz\\data20230802\\#12_integer_NI8.02GHz_att30_10dBm_agc0_RX3.mat'
data = scio.loadmat(dataFile)
iq_pre = data['iq_data'].T[0]#[0:4095]
iq_data = iq_pre - np.mean(iq_pre)
i_data = iq_data.real
q_data = iq_data.imag
# plt.plot(iq_data.real, marker='o', markersize=8)
# plt.plot(iq_data.imag, marker='x', markersize=8)

fftdata = np.fft.fft(iq_data)
fftdata_i = np.fft.fft(i_data)
fftdata_q = np.fft.fft(q_data)


# snr_1 = 
snr = snr_dB(fftdata)
snr_i = snr_dB(fftdata_i)
snr_q = snr_dB(fftdata_q)
print('snr=',snr)
print('snr_i=',snr_i)
print('snr_q=',snr_q)
# # t = np.arange(0, 1, 0.001)
# signal = np.sin(2*np.pi*5*t)
# fftdata = np.fft.fft(signal)
# plt.plot(fre, fftdata)

sample_rate = 998.4e6
fre = np.fft.fftfreq(len(fftdata), d=1/sample_rate)
plt.plot(abs(fftdata))
plt.plot(abs(fftdata))

counts_i = pd.Series(iq_pre.real).value_counts()
counts_q = pd.Series(iq_pre.imag).value_counts()

figbar, axbar = plt.subplots()
axbar.bar(counts_i.index, counts_i[0], width=1, edgecolor="white", linewidth=0.7)
figbar.show()


plt.show()


fig,axs = plt.subplots(2, 1)
fig.suptitle(dataFile)
axs[0].plot(iq_data.real, 'r', label = 'i')
axs[0].plot(iq_data.imag, 'b', label = 'q')
axs[0].grid()
axs[0].legend()
axs[0].set_title('Waveform')
axs[1].plot(fre, abs(fftdata_q),'gray', label = 'q')
axs[1].plot(fre, abs(fftdata_i),'green', label = 'i')
axs[1].set_title('FFT')
axs[1].grid()
axs[1].legend()