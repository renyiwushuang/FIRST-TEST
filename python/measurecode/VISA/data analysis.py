# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:05:10 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
import numpy
import collections


addr = r'E:\YJZ\work\EH100602A12\测试数据\动态功耗测试\ZGB\photo.out'
data = numpy.loadtxt(addr)
print(data)
plt.plot(data,linewidth=0.02)
dict1 = collections.Counter(data)
list1= sorted(dict1.items(),key=lambda x:x[1])
zero = list1[-1][0]      #基线确定
numpy.save(addr,data)
data2 = numpy.load(addr+'.npy')