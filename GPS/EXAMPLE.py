# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:36:07 2019

@author: Administrator
"""
# By Vamei

import numpy as np
import matplotlib.pyplot as plt

r1 = 26.56   # GPS radius
r2 = 6.371   # Earth radius

theta = np.linspace(0, 360, 361) / 180. * np.pi  # angles of plotting points

# Polar coordinate to Cartesian coordinate
x1 = r1*np.cos(theta)
y1 = r1*np.sin(theta)

x2 = r2*np.cos(theta)
y2 = r2*np.sin(theta)

fig = plt.figure()
ax = plt.subplot(111)
ax.set_aspect("equal")

plt.plot(x1, y1, color="red", label="GPS")
plt.plot(x2, y2, color="blue", label="Earth")

plt.title("Earth and GPS orbit, unit: 1000 km")

plt.legend()

plt.show()
