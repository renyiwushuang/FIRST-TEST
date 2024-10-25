# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:47:24 2023

@author: E002012
"""
import numpy as np
'''
SNR VS JITTER
'''
fs= 1e9
jitter = 2e-12
snr = -20*np.log10(2*np.pi*fs*jitter)