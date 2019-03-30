# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:45:41 2019

@author: Administrator
"""
import math
import constant

def buildin_potential(*arg):
    '''
    本函数计算PN结内建电压
    NA 是 n型掺杂浓度 单位 atoms/cm3
    ND 是 n型掺杂浓度 单位 atoms/cm3
    ni 是 本征半导体载流子浓度 单位 atoms/cm3
    T 是温度 单位K
    (constant.k*T/constant.q)*math.log(NA*ND/(ni**2))
    '''
    NA = arg[0]
    ND = arg[1]
    ni = arg[2]         #300K时硅的本征载流子浓度约为1.5e10
    T = arg[3]
    
    return     (constant.k*T/constant.q)*math.log(NA*ND/(ni**2))

def penetration_depletion_p(*arg) :
    '''
    本函数计算p型掺杂区的耗尽层深度 单位cm NA ND倒这写就可计算n型掺杂的深度
    u0 是内建电压    单位V
    Vr 是外加的反向电压     单位V
    NA 是 n型掺杂浓度 单位 atoms/cm3
    ND 是 n型掺杂浓度 单位 atoms/cm3
    er 是介电常数
    '''
    NA = arg[0]
    ND = arg[1]
    Vr = arg[2]
    u0 = arg[3]
    er = arg[4]
    return math.sqrt(2*er*(u0+Vr)/(constant.q*NA(1+NA/ND)))

if __name__ == '__main__' :
    print(buildin_potential(1e15,1e16,1.5e10,300))