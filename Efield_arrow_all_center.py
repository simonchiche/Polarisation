# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 22:12:43 2020

@author: Simon
"""


import numpy as np
import matplotlib.pyplot as plt


x,y,Etot, Ex, Ey = np.loadtxt('gamma.txt', unpack = True)

x_center = 0
y_center = 0    
Etot_center = 0  #Variables qui vont contenir la osition et les valeurs du champ pour l'antenne la plus proche du centre
Ex_center = 0
Ey_center = 0
Dist_centre = 10000 # on va chercher la position de l'antenne la plus proche du centre

for i in range(len(x)):
        if((np.sqrt(x[i]**2 + y[i]**2))< Dist_centre): 
            
            Dist_centre = np.sqrt(x[i]**2 + y[i]**2) 
            x_center = x[i]
            y_center = y[i]
            Etot_center = Etot[i]  
            Ex_center = Ex[i]
            Ey_center = Ey[i]


Ex_charge_excess = Ex - Ex_center #Au centre on a seulement la contribution geomagnetique
Ey_charge_excess = Ey - Ey_center


fig, ax0 = plt.subplots()


#q1 = ax0.quiver(x, y, Ex, Ey,units='xy' ,scale=1) Trace la polarisation du champ total
q2 = ax0.quiver(x, y, 2*Ex_charge_excess, 2*Ey_charge_excess,units='xy' ,scale=1, color = 'orange') # Polarisation du charge excess



im0 = plt.scatter(x, y, s=1,c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.xlim(-1000,1000)
plt.ylim(-5000,5000)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images/Efield_charge_excess_only_center.png', dpi = 2000)
plt.show()

