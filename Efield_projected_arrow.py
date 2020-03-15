# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 03:36:16 2020

@author: Simon
"""


import numpy as np
import matplotlib.pyplot as plt


x,y,z, Etot, Ex, Ey, Ez = np.loadtxt('gamma_all.txt', unpack = True) #x, y, z : antenna positions

v = np.zeros(176)              # antenna positions in the reference frame (v, vcrossB, vcross_vcrossB) : shower reference frame
vcrossB = np.zeros(176)
vcross_vcrossB = np.zeros(176)

Ev = np.zeros(176)         # field in the shower reference frame
EvcrossB = np.zeros(176)
Evcross_vcrossB = np.zeros(176)

B = 1.065      # Constant to go from the ground reference frame to the shower reference frame
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
    

fig, ax0 = plt.subplots()

q = ax0.quiver(vcrossB, vcross_vcrossB, EvcrossB, Evcross_vcrossB,units='xy' ,scale=1) # Total polarisation


im0 = plt.scatter(vcrossB,vcross_vcrossB,s=1,c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("k x B [m]")
plt.ylabel("k x (k x B) [m]")
plt.xlim(-1200, 4200)
plt.ylim(-1000,6000)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images/Efield_projected_arrow.png', dpi = 2000)
plt.show()

