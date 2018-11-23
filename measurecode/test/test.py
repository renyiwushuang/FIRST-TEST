# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 17:04:56 2018

@author: Administrator
"""

import pandas
import numpy


fid = 'Penguin_Htag_v08.02_实验样板BOM_20181122.xlsx'
df = pandas.read_excel(fid)
df['Unnamed: 7']= 1
