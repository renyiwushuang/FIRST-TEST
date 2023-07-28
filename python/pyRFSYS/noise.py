# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 16:14:17 2019

@author: Administrator
"""
import constant as cons


def res_noisev(*arg):
    '''电阻均方根噪声电压计算
    T是绝对温度 单位K
    B是带宽  单位 Hz
    R是电阻  单位欧姆
    '''
    T = arg[0]
    B = arg[1]
    R = arg[2]
    return 4*cons.k*T*R*B


    