# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:25:48 2019

@author: Administrator
"""

f = open('serialconfig.txt','w',encoding='utf-8')
s = 'hello world'


f.write(s)
f.write('\n')
f.write('happy end')
f.close()