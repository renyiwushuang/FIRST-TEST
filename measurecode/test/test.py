# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 17:04:56 2018

@author: Administrator
"""

import pandas
import numpy



fid = 'A05-P.xlsx'
df = pandas.read_excel(fid)
#df['Unnamed: 7']= 1

#data = df.drop([0,1,2,3,4])
#data.groupby('Unnamed: 5').sum().plot(kind='bar')
data = []
data = df['测试值'].copy()
#data[0]=0
flag = 0
while flag==0:
    
    mean = data.mean()
    std = data.std()
    getout = []
    a = []
    
    
    for datas in data:
        #print(4)
        a = abs(datas-mean)
        #print(5)
        getout.append(a)
    
    if max(getout)>(3*std):
        b = getout.index(max(getout))
        
        data = data.drop(b)      
        data = data.reset_index()
        data = data['测试值']
        print(data)
        
    else:
         flag = 1
  
        
#print(len(data))    
 #print(getout)   