# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:27:07 2023

@author: E002012
"""
import numpy as np



Lq = 64 # ADC fullscale
fc = 7.9782e9 # center frequency
js = 12e-12 # rms jitter


snrjq = 10*np.log10(3*Lq*Lq/(2 + 3*np.square(2*np.pi*fc*js)))
print(snrjq)