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
        
        
    else:
         flag = 1
print(df['测试项'][1],'剔除坏值完成')        
es = 0  
if len(data)%2==0 :
      for i in range(0,int(len(data)/2-1)):
          s = data[i]-data[i+int(len(data)/2)]
          es = s+es
      print('样本数量为偶数')
          #print('s is',s)
          #print(es)
else:
    for i in range(0,int(len(data)/2)):
          s = data[i]-data[i+int(len(data)/2+2)]
          es = s+es
    print('样本数量为奇数')
if abs(es)>1 :
    print('存在线性累积误差')
else:
    print('不存在线性累积误差')
    
          #print('s is',s)

          #print(es)
v =data-mean
ab = 0
for   i in range(0,len(data)-2):
    ab = ab + v[i]*v[i+1]
if abs(ab)-std*std*(len(data)-1)**0.5>0 :
    print('存在周期性系统误差')
else:
    print('不存在周期性系统误差')
      
#print(len(data))    
 #print(getout)   