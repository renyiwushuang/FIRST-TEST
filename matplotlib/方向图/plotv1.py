# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:11:05 2019

@author: Administrator
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpt
import os

filepath = 'E:\\YJZ\\github\\AutoMeasure\\measurecode\\test\\antenna\\2\\'
savepath = 'E:\\YJZ\\github\\AutoMeasure\\measurecode\\test\\antenna\\save\\'

os.chdir(filepath)

for file in os.listdir():
    [fname,exname] = os.path.splitext(file)
    rawdata = pd.read_excel(file) 
    data = rawdata[6:]
    columheaders = list(data.columns.values)
    for i in np.arange(1, 14):
        plt.figure(dpi=160)
        ax1 = plt.subplot(111, projection='polar')    
        ax1.plot(data[columheaders[0]]*(np.pi/180), data[columheaders[2*i]])
        plt.tick_params(labelsize=5)
        plt.yticks(np.arange(-46,-16,3))
        ax1.grid(True)
        plt.savefig(savepath + fname + rawdata[columheaders[2*i+1]][3] + '.jpg')
        plt.show()