# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 10:33:41 2019

@author: Administrator
"""

import numpy

def res1(*arg):
    A = arg[0]
    return numpy.linalg.inv(A)
    
if __name__ == '__main__'  :
    inpu = numpy.array( [[2,2],
                         [2,1]])
    goo = res(inpu)
            