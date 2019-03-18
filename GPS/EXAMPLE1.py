# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 17:45:38 2019

@author: Administrator
"""
# By Vamei

import numpy as np
import matplotlib.pyplot as plt

r1 = 26.56   # GPS radius
r2 = 6.371   # Earth radius

theta = np.linspace(0, 360, 361) / 180. * np.pi  # angles of plotting points

# Polar coordinate to Cartesian coordinate
end_x = r1*np.cos(55./180.*np.pi)
end_y = r1*np.sin(55./180.*np.pi)
x1 = [end_x, -end_x]
y1 = [end_y, -end_y]

x2 = r2*np.cos(theta)
y2 = r2*np.sin(theta)


fig = plt.figure()
ax = plt.subplot(111)
ax.set_aspect("equal")


plt.plot([])
plt.plot(x1, y1, color="red", label="GPS profile")
plt.plot(x2, y2, color="blue", label="Earth")
plt.plot([-r2, r2], [0, 0], color="green", label="equator")

plt.title("Earth and GPS orbit, unit: 1000 km")

plt.legend()

plt.show()