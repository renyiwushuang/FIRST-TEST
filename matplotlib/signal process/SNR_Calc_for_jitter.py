# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:27:07 2023

@author: E002012
"""
import numpy as np



Lq = 2**6 # ADC fullscale
fc = 8e9 # center frequency
js = 0.8e-12 # rms jitter

snr_adc = 6.02 * 6 + 1.72
snrjq = 10*np.log10(3*Lq*Lq/(2 + 3*np.square(2*np.pi*fc*Lq*js)))
print(snrjq, snr_adc)