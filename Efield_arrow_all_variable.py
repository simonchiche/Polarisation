# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 20:08:36 2020

@author: Simon
"""


import numpy as np
import matplotlib.pyplot as plt


x,y,Etot, Ex, Ey = np.loadtxt('gamma.txt', unpack = True)

# on va calculer les composantes du champ géimagnétique en additionnant le champ total des antennes symétriques par rapport au centre

Ex_geo = np.zeros(176)
Ey_geo = np.zeros(176)


for i in range(len(x)):  

    if(i < 160):

        for j in range(len(x)):
            if ((i != j) & (j<160) & (np.abs(x[i]) == np.abs(x[j]))): # Condition pour repérer 2 antennes symétriques
            
                Ex_geo[i] = (Ex[i] + Ex[j])/2.0
                Ey_geo[i] = (Ey[i] + Ey[j])/2.0
        


Ex_charge_excess = Ex - Ex_geo # Charge excess déterminépar la différence entre le champ total et le champ geo
Ey_charge_excess = Ey - Ey_geo

for i in range(16):
    Ex_charge_excess[i+160] = 0 # Les valeurs ne calculées ne prennent pas en compte les cross check antenna (i>=160)
    Ey_charge_excess[i+160] = 0


fig, ax0 = plt.subplots()


#q1 = ax0.quiver(x, y, Ex, Ey,units='xy' ,scale=1) #champ total
q2 = ax0.quiver(x, y, Ex_charge_excess*7, Ey_charge_excess*7,units='xy' ,scale=1, color = 'orange') #charge excess / facyeur 7 pour la visibilité
#q3 = ax0.quiver(x, y, Ex_geo, Ey_geo,units='xy' ,scale=1, color = 'green') #champ geomagnétique



im0 = plt.scatter(x, y, s=1, c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.xlim(-2000,2000)
plt.ylim(-4000,4000)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images/Efield_charge_excess_only_variable.png', dpi = 2000)
plt.show()
