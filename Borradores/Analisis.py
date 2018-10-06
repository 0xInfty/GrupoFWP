# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 14:58:16 2018

@author: Marcos
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from smooth import smooth
from scipy.fftpack import fft
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
completa = os.path.join('Measurements', file)
datos = np.loadtxt(completa)
datos = datos[15000:20000, :]
sr = 42100

chR, chL = np.split(datos, 2, axis=1)
chR = smooth(chR.flatten())
chL = smooth(chL.flatten())

chR /= max(chR)
chL /= max(chL)

fL = fft(chL)
fR = fft(chR)

N = len(fL)

frecs = np.linspace(0.0, 1.0/(2.0/sr), N//2)

freqR = frecs[np.argmax(2.0/N * np.abs(fR[0:N//2]))]
freqL = frecs[np.argmax(2.0/N * np.abs(fL[0:N//2]))]

#plt.plot(frecs, 2.0/N * np.abs(fL[0:N//2]), label ='L')
#plt.plot(frecs, 2.0/N * np.abs(fR[0:N//2]), label='R')
#plt.legend()

tiempo = np.arange(0, len(chR)/sr, 1/sr)

plt.plot(tiempo, chR,label='R: freq={:.0f} Hz, mean={:.2e}'.format(freqR, np.mean(chR)))
plt.plot(tiempo, chL,label='L: freq={:.0f} Hz, mean={:.2e}'.format(freqL, np.mean(chL)))
plt.legend()
