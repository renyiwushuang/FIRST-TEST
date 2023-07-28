# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:00:25 2019

@author: Administrator
"""

def blowing_rate(*arg):
    '''风量计算
    Tp是排风温度 单位℃
    Tj是进风温度  单位℃
    airc是空气比热  单位kj/kg℃
    airp是空气密度   单位 kg/m3
    PD 是设备散热量   单位 KW
    返回所需风量      单位 CFM
    '''
    Tp = arg[0]
    Tj= arg[1]
    PD = arg[2]
    return  PD/(((Tp-Tj)*1.09)*0.028)

