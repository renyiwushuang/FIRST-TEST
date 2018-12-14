# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 17:04:56 2018

@author: Administrator
"""

import pandas
import numpy



fid = 'data.xlsx'
df = pandas.read_excel(fid)
#df['Unnamed: 7']= 1

#data = df.drop([0,1,2,3,4])
#data.groupby('Unnamed: 5').sum().plot(kind='bar')
data = []
data = df['测试值']
mean = data.mean()
std = data.std()
getout = []
for data in data:
    a = abs(data-mean)
    getout.append(a)
print(len(getout))   
if max(getout)>(mean+3*std):
    b = getout.index(max(getout))
    del getout[b]
    print(1)
print(len(getout))    
 #print(getout)   