# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:20:44 2024

@author: E002012

The former IEC TR 62380 [40] is used in this document as the basis for a model for reliability prediction of electronics components.

lambda = lambda_die + lambda_package + lambda_overstress  unit=1e-9/h
"""
import  numpy as np 

##      input parameter
lambda1 = 2.71e-4
N = 31727044
alpha = 10
lambda2 = 20
pi_t_i = np.array([0.44,0.49,2.74])
tao_i = np.array([0.1,0.8,0.1])

pi_alpha = 0.06*np.power(21.5-16, 1.68)
D = np.power(79.25, 0.5)
lambda3 = 0.048*np.power(D, 1.68)
cycle = np.array([670,1340,30])
pi_n_i = np.power(cycle, 0.76)
delta_T_i = np.array([31.5,21.5,10])


pi_I = 1
lambda_EOS = 40
##      calculation of lambda_die
lambda_die = (lambda1*N*np.power(np.e, -0.35*alpha) + lambda2) *  np.sum(tao_i*pi_t_i)
print("lambda_die=",lambda_die)

##      calculation of lambda_package
lambda_package = 2.75e-3*pi_alpha*lambda3*np.sum(np.power(delta_T_i, 0.68)*pi_n_i)
print("lambda_package=",lambda_package)

##      calculation of lambda_overstress
lambda_overstress = pi_I*lambda_EOS
print("lambda_overstress=",lambda_overstress)

## lambda_total
lambda_total = (lambda_die + lambda_package + lambda_overstress) * 1e-9
MTTF = 1/lambda_total
print("lambda_total=",lambda_total)
print("MTTF=",MTTF)