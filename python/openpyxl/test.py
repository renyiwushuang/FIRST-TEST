# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:37:03 2019

@author: Administrator
"""

import openpyxl as xl
import os
import pandas as pd

def getERPnumber() :
    data = pd.read_excel(r'E:\YJZ\work\BOM更新\1555648712021\库存物料编码.xls')
    list1 = []
    for i in  range(0,data.shape[0],1):
        tup = tup = (data['规格型号'][i],str(data['存货编码'][i]))
        list1.append(tup)
    dict1 = dict(list1)
    
    return dict1
def xlstoxlsx (path) :
   
    os.chdir(os.path.dirname(path))
    portion = os.path.splitext(path)
    print(portion[1])
    if portion[1]=='.xls' :
        newname = portion[0].split('\\')[-1]+'.xlsx'
        os.rename(path.split('\\')[-1],newname)
        print(newname)
        return newname
    
def convertwork(path,outpath,erpnumber):
   wb = xl.load_workbook(path)
   sheet = wb[wb.sheetnames[0]]
   col = 0
   row = 0
   for i in range(1,10,1) :
       if sheet.cell(row=i,column=1).value=='Designator' :
           row =  i
           break    
   print(row)
   for i in range(1,10,1) :
       if sheet.cell(row=row,column=i).value=='commentname' :
           col =  i
           break    
   print(col)
   maxcol= sheet.max_column+1
   for i in range(row,sheet.max_row+1,1):
       #print(sheet.cell(row=i,column=col).value)
       #print(sheet.cell(row=i,column=col).value in erpnumber.keys())
       if  sheet.cell(row=i,column=col).value in erpnumber.keys() :
           sheet.cell(row=i,column=maxcol).value=erpnumber[sheet.cell(row=i,column=col).value]
       else: 
           sheet.cell(row=i,column=maxcol).value='NA'

   wb.save(outpath+'\\'+path.split('\\')[-1]) 
#erpnumber = getERPnumber() 
filepath = r'E:\YJZ\work\BOM更新\1555648712021\EH100602A13-P_安全帽增强型定位标签_产品整机BOM_20190424.xlsx'
outpath = r'E:\YJZ\work\BOM更新'
#convertwork(filepath,outpath,getERPnumber())

#wb = xl.load_workbook(filepath)
#sheet = wb[wb.sheetnames[0]]


        