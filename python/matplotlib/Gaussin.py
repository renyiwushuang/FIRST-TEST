# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 13:06:10 2019

@author: Administrator
"""
import numpy as np

import matplotlib.pylab as plt 
t = np.arange(-10,10,0.1)
w = 10*np.exp(-t*t)
plt.plot(t,w)
plt.show()
