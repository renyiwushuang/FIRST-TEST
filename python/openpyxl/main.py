# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:32:52 2019

@author: Administrator
"""

import openpyxl as xl
import os
import pandas as pd



def createdir(*arg):
    workpath = arg[0]
    os.chdir(workpath)
    if not os.path.exists :
        os.mkdir('output')
    else:
        print('文件已存在')
    return

def getERPnumber() :
    data = pd.read_excel('库存物料编码.xls')
    list1 = []
    for i in  range(0,data.shape[0],1):
        tup = tup = (data['规格型号'][i],str(data['存货编码'][i]))
        list1.append(tup)
    dict1 = dict(list1)
    return dict1
    
workpath = r'E:\YJZ\work\BOM更新\1555648712021'
os.chdir(workpath)
erpnumber = getERPnumber()    