# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 20:30:01 2023

@author: E002012
"""

import numpy as np
import matplotlib.pyplot as plt


zetaBW = np.arange(0, 0.1, 0.01) #zetaBW is bandwidth efficiency
y = (np.exp2(zetaBW) - 1) / zetaBW # y is the signal energy per bit

fig, ax = plt.subplots()
ax.plot(zetaBW, y)
plt.show()