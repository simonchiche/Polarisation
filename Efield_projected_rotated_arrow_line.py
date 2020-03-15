# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 20:24:32 2020

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

# On effectue la rotation

for i in range(len(x)):
    
    vcrossB_rotated[i] = np.cos(alpha)*vcrossB[i] + np.sin(alpha)*vcross_vcrossB[i]
    vcross_vcrossB_rotated[i] = -np.sin(alpha)*vcrossB[i] + np.cos(alpha)*vcross_vcrossB[i]
    
    EvcrossB_rotated[i] = np.cos(alpha)*EvcrossB[i] + np.sin(alpha)*Evcross_vcrossB[i]
    Evcross_vcrossB_rotated[i] = -np.sin(alpha)*EvcrossB[i] + np.cos(alpha)*Evcross_vcrossB[i]
    
# On centre l'asbcisse et l'ordonnée en 0

vcrossB_rotated = vcrossB_rotated + 1817.3
vcross_vcrossB_rotated = vcross_vcrossB_rotated - 2555

# On va tracer le champ le long de la ligne d'antenne suivant (v x B)

vcrossB_rotated_line = np.zeros(40)
Etot_line = np.zeros(40)

k = 0

for i in range(len(x)):
    if((i%4 == 0) & (i<160)):
        vcrossB_rotated_line[k] = vcrossB_rotated[i]        
        k = k + 1


vcrossB_rotated_line = np.sort(vcrossB_rotated_line)

for i in range(len(x)):
    for j in range(len(vcrossB_rotated_line)):
        if(vcrossB_rotated_line[j] == vcrossB_rotated[i]):
            Etot_line[j] = Etot[i]

plt.plot(vcrossB_rotated_line, Etot_line) # On trace le champ le long de la ligne d'antenne
plt.xlabel('v x b [m]')
plt.ylabel(r"$ Ep2p\ [\mu V/m]$")
plt.savefig('./images_Efield_projected_rotated/p2p_line_projected.png')


E_charge_excess = 12.158


# On veut maitenant déterminer la décomposition sur les axes x et y du charge excess, pour cela on part du principe que chaque flèche pointe vers le coeur de la gerbe

EvcrossB_charge_excess = np.zeros(176)
Evcross_vcrossB_charge_excess = np.zeros(176)
Dist_centre = 0 # variable qui va contenir la distance de chaque antenne au centre de la gerbe
scaling_factor = 0 # rapport entre le charge excess et la distance au centre

for i in range(len(x)):

    Dist_centre = np.sqrt(vcrossB_rotated[i]**2 + vcross_vcrossB_rotated[i]**2)
    scaling_factor = E_charge_excess/Dist_centre
    EvcrossB_charge_excess[i]= -vcrossB_rotated[i]*scaling_factor  # Conditions pour que le charge excess pointe vers le centre
    Evcross_vcrossB_charge_excess[i] = -vcross_vcrossB_rotated[i]*scaling_factor


# On en déduit les composantes du champ géomagnétique

EvcrossB_geo = np.zeros(176)
Evcross_vcrossB_geo = np.zeros(176)

EvcrossB_geo = EvcrossB_rotated - EvcrossB_charge_excess
Evcross_vcrossB_geo = Evcross_vcrossB_rotated - Evcross_vcrossB_charge_excess

    
fig, ax0 = plt.subplots()

q1 = ax0.quiver(vcrossB_rotated, vcross_vcrossB_rotated, EvcrossB_rotated/1.2, Evcross_vcrossB_rotated/1.2,units='xy' ,scale=1)
q2 = ax0.quiver(vcrossB_rotated, vcross_vcrossB_rotated, EvcrossB_charge_excess*7, Evcross_vcrossB_charge_excess*7
               ,units='xy' ,scale=1, color = 'orange') #charge excess
q3 = ax0.quiver(vcrossB_rotated, vcross_vcrossB_rotated, EvcrossB_geo/1.2, Evcross_vcrossB_geo/1.2,units='xy' ,scale=1, color = 'green') #champ geomagnétique


im0 = plt.scatter(vcrossB_rotated,vcross_vcrossB_rotated,s=1,c=Etot, cmap='bwr')

ax0.set_title("Electricf_p2p")
plt.xlabel("k x B [m]")
plt.ylabel("k x (k x B) [m]")
plt.xlim(-2900, 3000)
plt.ylim(-3100,3100)
cbar = fig.colorbar(im0,ax=ax0)
cbar.set_label(r"$ E\ [\mu V/m]$")
plt.savefig('./images_Efield_projected_rotated/Efield_projected_rotated_arrow_line.png', dpi = 2000)
plt.show()
