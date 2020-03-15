# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 22:56:23 2020

@author: Simon
"""


import numpy as np
import matplotlib.pyplot as plt


x,y,Etot, Ex, Ey = np.loadtxt('gamma.txt', unpack = True)

# on va moyenner les champs du premier cercle d'antenne pour n'avoir que la contribution geomagnétique

x_center = np.zeros(8) # 8 bras soit 8 antennes au centre
y_center = np.zeros(8)
z_center = np.zeros(8)  # Positions et valeur du champ pour les antennes du premier cercle central
Ex_center = np.zeros(8)
Ey_center = np.zeros(8)
Etot_center = np.zeros(8)

k = 0

for i in range(len(x)):
        if((np.abs(x[i])<=110.0) & (np.abs(y[i])<=500)): # si l'antenne appartient au premier cercle, on la garde
            x_center[k] = x[i]
            y_center[k] = y[i]
            Ex_center[k] = Ex[i]
            Ey_center[k] = Ey[i]
            Etot_center[k] = Etot[i]
           
            k = k + 1


Ex_geo = np.sum(Ex_center)/8.0 # La somme des contributions donne 8 fois la valeur du champ geomagnétique
Ey_geo = np.sum(Ey_center)/8.0

Ex_charge_excess = Ex - Ex_geo #charge excess total donné par la différence entre le champ total et le champ geo
Ey_charge_excess = Ey - Ey_geo


fig, ax0 = plt.subplots()


#q1 = ax0.quiver(x, y, Ex, Ey,units='xy' ,scale=1) #champ total
q2 = ax0.quiver(x, y, 2*Ex_charge_excess, 2*Ey_charge_excess,units='xy' ,scale=1, color = 'orange') #charge excess



im0 = plt.scatter(x, y, s=1, c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.xlim(-1000,1000)
plt.ylim(-5000,5000)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images/Efield_charge_excess_only_circle.png', dpi = 2000)
plt.show()
