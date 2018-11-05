# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.0,2.0,0.01)
s = 1+np.sin(2*np.pi*t)


fig,ax = plt.subplots()
ax.plot(t,s)

ax.set(xlabel='time(s)',ylabel='voltage(mV)',title='About as simple as is geys,folks')
ax.grid()
fig.savefig('sin.png')
fig.savefig('sin.jpg')
plt.show()
