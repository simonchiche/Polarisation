# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:43:23 2020

@author: Simon
"""

import numpy as np
import matplotlib.pyplot as plt


x,y,Etot, Ex, Ey = np.loadtxt('gamma.txt', unpack = True) # x = x_antenna, y = y_antenna


fig, ax0 = plt.subplots()

q = ax0.quiver(x, y, Ex, Ey,units='xy' ,scale=1) # flèches traçant Ex et Ey

im0 = plt.scatter(x,y,s=1,c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.xlim(-1000, 1000)
plt.ylim(-5000,5000)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('Efield_arrow.png', dpi = 2000)
plt.show()

    
