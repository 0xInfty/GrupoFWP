# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 14:58:16 2018

@author: Marcos
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from smooth import smooth
#%% Diodo! 

direc = os.path.join(os.getcwd(),'Measurements', 'Diode_IV_400_Hz_1.00')
archivo = os.path.join(direc, 'Diode_IV_400_Hz_1.00.txt')
datos = np.loadtxt(archivo)
datos = datos[20000:25000, :]
chR, chL = np.split(datos, 2, axis=1)
#plt.plot(chR, chL)
#plt.plot(chR)
R = 1e3
r2 = 5.75e6
r1 = 1e6

V0 = (r1 + r2)*chR/r1
I = chL / R
V = V0 + chL

plt.figure()
plt.plot(V, I)

plt.figure()
plt.plot(chR, chL)

#%% Opamp

file = 'inversor_div-11-3.txt' #circuito inverson con un divisor de tensión por 11/3 en la lectura
datos = np.loadtxt(file)
datos = datos[15000:20000, :]

chR, chL = np.split(datos, 2, axis=1)
chR = smooth(chR.flatten())
chL = smooth(chL.flatten())

plt.plot(chR,label='R')
plt.plot(chL,label='L')
