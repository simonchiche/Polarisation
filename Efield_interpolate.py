# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:58:27 2020

@author: Simon
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

xi,yi,zi, Ex, Ey = np.loadtxt('gamma.txt', unpack = True) #x = x_antenna, y = y_antenna, z = Etot


fig, ax0 = plt.subplots()

x = np.linspace(-1000, 1000, 1000) #espace couvert par les antennes autour de l'anneau cernekov
y = np.linspace(-5000, 5000, 10000) # espace couvert par les antenes autour de l'anneau cerenkov

X, Y = np.meshgrid(x, y) #grille qui pave l'espace

grid_z0 = griddata((xi,yi), zi, (X,Y), method = 'nearest') # valeurs interpolees du champ total


im0 = plt.imshow(grid_z0.T, extent=(-4000,4000,-4000,4000), origin='lower') # on plot le resultat
fig.colorbar(im0,ax=ax0)
plt.title('Efield_interpolate')
plt.xlabel('x[m]')
plt.ylabel('y[m]')
plt.savefig('Efield_interpolate.png', dpi = 2000)
plt.show()

