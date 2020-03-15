# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 20:14:58 2020

@author: Simon
"""

import numpy as np
import matplotlib.pyplot as plt


x,y,z, Etot, Ex, Ey, Ez = np.loadtxt('gamma_all.txt', unpack = True) #x, y, z : antenna positions

v = np.zeros(176)   # antenna positions in the reference frame (v, vcrossB, vcross_vcrossB) : shower reference frame
vcrossB = np.zeros(176)
vcross_vcrossB = np.zeros(176)

Ev = np.zeros(176)    # field in the shower reference frame
EvcrossB = np.zeros(176)
Evcross_vcrossB = np.zeros(176)

B = 1.065       # Constant to go from the ground reference frame to the shower reference frame
C = -0.217
D = -0.850
E = -0.12
F = 0.590
G = 0.554
H = -0.185
I = 0.906

# We compute the values of v, vcrossB, vcross_vcrossB

for i in range(len(x)):

    v[i] = B*y[i] + C*z[i]                  # positions des antennes dans le réferentiel de la gerbe
    vcrossB[i] = D*x[i] + E*y[i] + F*z[i]
    vcross_vcrossB[i] = G*x[i] + H*y[i] + I*z[i]

    Ev[i] = B*Ey[i] + C*Ez[i]                     # valeurs du champ dans le réferentiel de la gerbe
    EvcrossB[i] = D*Ex[i] + E*Ey[i] + F*Ez[i]
    Evcross_vcrossB[i] = G*Ex[i] + H*Ey[i] + I*Ez[i]

#la figure obtenue est inclinée, on veut la poviter d'un angle qui est l'angle entre la ligne selon laquelle est orientée le champ géo et l'horizontale
# On détermine dans un premier temps cet angle

l = np.sqrt(x[156]**2 + y[156]**2) # l longeur de la ligne selon laquelle est le champ geo
epsilon = 0.079  # correction à alpha déterminée à posteriori
alpha = np.arcsin(y[156]/l) + epsilon  # sin(alpha) = y/l

vcrossB_rotated = np.zeros(176)
vcross_vcrossB_rotated = np.zeros(176)

EvcrossB_rotated = np.zeros(176)
Evcross_vcrossB_rotated = np.zeros(176)

for i in range(len(x)):

    vcrossB_rotated[i] = np.cos(alpha)*vcrossB[i] + np.sin(alpha)*vcross_vcrossB[i]
    vcross_vcrossB_rotated[i] = -np.sin(alpha)*vcrossB[i] + np.cos(alpha)*vcross_vcrossB[i]

    EvcrossB_rotated[i] = np.cos(alpha)*EvcrossB[i] + np.sin(alpha)*Evcross_vcrossB[i]
    Evcross_vcrossB_rotated[i] = -np.sin(alpha)*EvcrossB[i] + np.cos(alpha)*Evcross_vcrossB[i]


fig, ax0 = plt.subplots()

q = ax0.quiver(vcrossB_rotated, vcross_vcrossB_rotated, EvcrossB_rotated, Evcross_vcrossB_rotated,units='xy' ,scale=1)

im0 = plt.scatter(vcrossB_rotated,vcross_vcrossB_rotated,s=1,c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("k x B [m]")
plt.ylabel("k x (k x B) [m]")
plt.xlim(-4900, 1000)
plt.ylim(-600,5600)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images_Efield_projected_rotated/Efield_projected_rotated_arrow.png', dpi = 2000)
plt.show()
