#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 19:23:44 2018

@author: flusher
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import os




#%% Calibration record


direc = os.getcwd()
archivo = os.path.join(direc, 'Cal_Rec_2000_Hz_Data.txt')
datos = np.loadtxt(archivo)
vpp_gen_func = datos[:,0]
vpp_left = datos[:,1]
vpp_right = datos[:,2]


vpp_gen_func_lineal = vpp_gen_func[40:90]
vpp_left_lineal = vpp_left[40:90]
vpp_right_lineal = vpp_right[40:90]

plt.figure()
plt.plot(vpp_gen_func_lineal, vpp_left_lineal,'r.')
plt.plot(vpp_gen_func_lineal, vpp_right_lineal,'b.')


def recording_calibration(vgen, m, b):
    vreal = vgen * m + b
    return vreal

p0=[2,0]
poptleft, pcovleft = curve_fit(recording_calibration, vpp_gen_func_lineal, vpp_left_lineal,p0=p0)
poptright, pcovright = curve_fit(recording_calibration, vpp_gen_func_lineal, vpp_right_lineal,p0=p0)




plt.figure()
plt.plot(vpp_gen_func, vpp_left,'r.')
plt.plot(vpp_gen_func, vpp_right,'b.')
plt.plot(vpp_gen_func_lineal, recording_calibration(vpp_gen_func_lineal, poptleft[0], poptleft[1]),'r-')
plt.plot(vpp_gen_func_lineal, recording_calibration(vpp_gen_func_lineal, poptright[0], poptright[1]),'b-')



slope_left=poptleft[0]
origin_left=poptleft[1]
slope_right=poptright[0]
origin_right=poptright[1]


#%% Calibration curves


def left_calibration(vleft):
    vreal = vleft / slope_left - (origin_left/slope_left)
    return vreal


def right_calibration(vright):
    vreal = vright /slope_right - origin_right/slope_right
    return vreal


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

V0 = (r1 + r2)*right_calibration(chR)/r1
I = left_calibration(chL) / R
V = V0 + left_calibration(chL)

plt.figure()
plt.plot(V, I,'r.')

#plt.figure()
#plt.plot(chR, chL,'k.')


datossss=np.column_stack((V,I))
np.savetxt('datos.txt',datossss)

#%% Calibration diode


direc = os.getcwd()
archivo = os.path.join(direc, 'datos.txt')
datos= np.loadtxt(archivo)
V=datos[20:100,0]
I=datos[20:100,1]
#plt.plot(V, I,'r.')

b=np.zeros(len(I))
for i in range(len(I)):
    b[i]=I[i]*1000000


def diode_function(V, n, Io):
    kt = 300 * 1.38e-23
    q = 1.60e-19
    I_final = Io * (np.exp( (q * V) / (n * kt) ) - 1)
    return np.abs(I_final)

p0 = [20, -3.80741e-05]
popt, pcov = curve_fit(diode_function, V, I,p0=p0)
plt.plot(V, diode_function(V, popt[0],popt[1]),'b-')
plt.plot(V,I,'r.')
#plt.plot(I)