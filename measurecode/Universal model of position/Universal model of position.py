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
    if where == '办公室' :
        if fre == 2400 :
            NIL = 30
    return NIL
    

def NILf(fre, where):
    if where =='办公室' :
        if fre == 2400 :
            NILf = 14
    
    return NILf
    



   
fre = 2400
where = '办公室'
d = 40.0
floor = 0
NILf =  NILf(fre,where)
NILspace = NILspace(fre,where)




Lt = Ltotal(Lo(fre),Lspace(d,NILspace),Lf(floor,NILf))
print(Lt)
