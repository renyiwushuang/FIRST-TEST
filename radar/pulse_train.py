# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 12:50:24 2018

@author: Administrator
"""

import numpy as np

def pulse_train(tau,pri,p_peak):
    '''pulse_train 计算占空因子、平均发射功率、脉冲能量和脉冲重复频率
    参数  定义  单位
    tau  脉冲宽度  s
    pri  PRI  s
    p_peak  峰值功率  W
    返回结果
    dt  占空因子
    pav  平均发射功率  W
    ep  脉冲能量  J
    prf  PRF  Hz
    ru  无模糊距离  km
    '''
    c = 3.0e+8;
    dt = tau/pri
    prf = 1/pri
    pav = p_peak*dt
    ep = p_peak*tau
    ru = 1.0e-3*c*pri/2.0
    a = [dt,prf,pav,ep,ru]    
    result = np.array(a)
    return result
s = pulse_train(1.5e-5,1.0e4,1.0e4)
print(s)
ss = pulse_train(1.5e-5,1.5e4,1.0e4)
print(ss)