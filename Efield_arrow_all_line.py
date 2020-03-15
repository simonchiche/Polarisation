# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 10:40:44 2020

@author: Simon
"""


import numpy as np
import matplotlib.pyplot as plt


x,y,Etot, Ex, Ey = np.loadtxt('gamma.txt', unpack = True)

# on va tracer les valeurs du champ total le long d'une ligne d'antenne

x_line = np.zeros(40)
y_line = np.zeros(40)
z_line = np.zeros(40)  # Tableaux qui vont contenir les positions et valeurs du champ le long de la ligne
Ex_line = np.zeros(40)
Ey_line = np.zeros(40)
Etot_line = np.zeros(40)

k = 0

for i in range(len(x)):
        if(((i+3)%4==0) & (i<160)): # Condition pour que l'antenne  appartienne à la ligne et ne soit pas une cross check
            x_line[k] = x[i]
            Ex_line[k] = Ex[i]
            Ey_line[k] = Ey[i]

            k = k + 1

#On veut definir un tableau qui contient les valeurs de l'abscisse qui suit la ligne des antennes

u_line = np.zeros(40) # abscisse le long de la ligne
u_line[0] = 0

x_line = np.sort(x_line) # On trie les valeurs de x

# On obtient les valeurs de y et Etot triées correspondants aux valeurs de x triées

for i in range(len(x)):
    for j in range(len(x_line)):
        if(x_line[j] == x[i]):
            y_line[j] = y[i]
            Etot_line[j] = Etot[i]


# On construit les valeurs de l'abscisse le long de la ligne d'antenne

for j in range(39):

    u_line[j+1] = u_line[j] + np.sqrt((x_line[j]-x_line[j+1])**2 + (y_line[j] - y_line[j+1])**2)

plt.plot(u_line, Etot_line) # On trace le champ le long de la ligne d'antenne
plt.xlabel('d (m)')
plt.ylabel(r"$ Ep2p\ [\mu V/m]$")
plt.savefig('./images/p2p_line.png')


E_charge_excess = 17.08 # lue graphiquement : différence entre les 2 pics


# On veut maitenant déterminer la décomposition sur les axes x et y du charge excess, pour cela on part du principe que chaque flèche pointe vers le coeur de la gerbe

Ex_charge_excess = np.zeros(176)
Ey_charge_excess = np.zeros(176)
Dist_centre = 0 # variable qui va contenir la distance de chaque antenne au centre de la gerbe
scaling_factor = 0 # rapport entre le charge excess et la distance au centre

for i in range(len(x)):

    Dist_centre = np.sqrt(x[i]**2 + y[i]**2)
    scaling_factor = E_charge_excess/Dist_centre
    Ex_charge_excess[i]= -x[i]*scaling_factor  # Conditions pour que le charge excess pointe vers le centre
    Ey_charge_excess[i] = -y[i]*scaling_factor


# On en déduit les composantes du champ géomagnétique

Ex_geo = np.zeros(176)
Ey_geo = np.zeros(176)

Ex_geo = Ex - Ex_charge_excess
Ey_geo = Ey - Ey_charge_excess




fig, ax0 = plt.subplots()


q1 = ax0.quiver(x, y, Ex, Ey,units='xy' ,scale=1) #champ total
q2 = ax0.quiver(x, y, Ex_charge_excess*5, Ey_charge_excess*5,units='xy' ,scale=1, color = 'orange') #charge excess
q3 = ax0.quiver(x, y, Ex_geo, Ey_geo,units='xy' ,scale=1, color = 'green') #champ geomagnétique



im0 = plt.scatter(x, y, s=1, c=Etot, cmap='bwr')

plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.xlim(-2000,2000)
plt.ylim(-4000,4000)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images/Efield_charge_excess_only_line.png', dpi = 2000)
plt.show()
