# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:31:53 2019

@author: Administrator
"""

from bs4 import BeautifulSoup
f = open('serialconfig.html','r',encoding='utf-8')
ff = f.read()
soup = BeautifulSoup(ff,'lxml')
