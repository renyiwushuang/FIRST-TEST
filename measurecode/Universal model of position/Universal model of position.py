# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:58:54 2019

@author: Administrator
"""

import math

def Ltotal(Lo,Lspace,Lf):
    return (Lo+Lspace+Lf)
    
def Lo(fre):
    return 20*math.log10(fre)-28
    
def Lspace(d,N):
   
    return math.log10(d)*N

def Lf(floor,IL):
    return floor*IL
def NILspace(fre,where):
    for data in NLspaceData():
        if data[0] == where :
            flag = 0
            for  frequency in data[1]:
                if frequency[0] == fre:
                    NIL = frequency[1]
                    flag = 1
            if flag == 0 :
                print('no fre match')
            
                    
    return NIL
    

def NILf(fre, where):
    if where =='办公室' :
        if fre == 2400 :
            NILf1 = 14
    else:
        NILf1=0
    return NILf1
    
def NLspaceData():
    return [('居民楼',((1900,28),(2400,28),(5200,28))),
            ('办公室',((800,22.5),(900,33),(1250,32),(1900,30),(2100,25.5),(2200,20.7),(2400,30),(2625,44),(3500,27),(4000,28),(4700,19.8),
                    (5200,31))),
            ('商业楼',((900,20),(1250,22),(1900,22),(2100,20),(4000,22))),
            ('工厂',((2100,21.1),(2625,33))),
            ('走廊',((2100,17)))]


   
fre = 3500
where = '办公室'
d = 20.0
floor = 0
NILf =  NILf(fre,where)
NILspace = NILspace(fre,where)




Lt = Ltotal(Lo(fre),Lspace(d,NILspace),Lf(floor,NILf))
print('总插损是 %f' %Lt)
