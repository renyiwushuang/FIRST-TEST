# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:37:03 2019

@author: Administrator
"""

import openpyxl as xl
import os
import pandas as pd

def getERPnumber() :
    data = pd.read_excel('库存物料编码.xls')
    list1 = []
    for i in  range(0,data.shape[0],1):
        tup = tup = (data['规格型号'][i],str(data['存货编码'][i]))
        list1.append(tup)
    dict1 = dict(list1)
    
    return dict1
    
   


filepath = r'E:\YJZ\work\BOM更新\1555648712021'
savepath = filepath +r'\output'
os.chdir(filepath)

erpnumber = getERPnumber() 
wb = xl.load_workbook('Penguin_tag_v06.05_merge_20190418.xlsx')
sheet = wb[wb.sheetnames[0]]
col = 0
for i in range(1,10,1) :
    if sheet.cell(row=8,column=i).value=='commentname' :
        col =  i
        break    
print(col)
maxcol= sheet.max_column+1
for i in range(9,sheet.max_row,1):
    print(sheet.cell(row=i,column=col).value)
    print(sheet.cell(row=i,column=col).value in erpnumber.keys())
    if  sheet.cell(row=i,column=col).value in erpnumber.keys() :
        sheet.cell(row=i,column=maxcol).value=erpnumber[sheet.cell(row=i,column=col).value]
    else: 
        sheet.cell(row=i,column=maxcol).value='NA'

wb.save('13.xlsx')
        