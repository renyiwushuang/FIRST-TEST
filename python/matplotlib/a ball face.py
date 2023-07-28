# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 10:12:21 2018

@author: Administrator
"""

import matplotlib
import numpy


center = [1,2,3]
radius = 10


u = numpy.linspace(0,2*numpy.pi,100)
v = numpy.linspace(0,numpy.pi,100)
x = radius*numpy.outer(numpy.cos(u),numpy.sin(v)+center[0])
y = radius*numpy.outer(numpy.sin(u),numpy.sin(v)+center[1])
z = radius*numpy.outer(numpy.ones(numpy.size(u)),numpy.cos(v)+center[2])


fig = matplotlib.figure()
ax = fig.add_subplot(121,projection = '3d')



 