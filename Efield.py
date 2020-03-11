# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 00:23:01 2020

@author: Simon
"""

import numpy as np
import matplotlib.pyplot as plt


x,y,z, Ex, Ey = np.loadtxt('gamma.txt', unpack = True) #x = x_antenna, y = y_antenna, z = Etot
fig, ax0 = plt.subplots()


im0 = plt.scatter(x,y,s=1,c=z, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
cbar = fig.colorbar(im0,ax=ax0)
plt.savefig('Efield.png', dpi = 2000)

    
    


