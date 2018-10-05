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




#%% Calibration play


direc = os.path.join(os.getcwd(),'..','Measurements')
archivo = os.path.join(direc, 'Cal_Play_2000_Hz_Data.txt')
datos = np.loadtxt(archivo)
amplitude_factor = datos[:,0]
vpp_osc_left = datos[:,1]
vpp__osc_right = datos[:,2]

cut=64

amplitude_factor_lineal = amplitude_factor[cut:len(amplitude_factor)]
vpp_osc_left_lineal = vpp_osc_left[cut:len(vpp_osc_left)]
vpp__osc_right_lineal = vpp__osc_right[cut:len(vpp__osc_right )]

amplitude_factor_constant = amplitude_factor[0:cut]
vpp_osc_left_constant = vpp_osc_left[0:cut]
vpp_osc_right_constant = vpp__osc_right[0:cut]

plt.figure()
plt.plot(amplitude_factor_lineal, vpp_osc_left_lineal,'r.')
plt.plot(amplitude_factor_lineal, vpp__osc_right_lineal,'b.')


def playing_calibration(amp, m, b):
    vreal = amp * m + b
    return vreal

p0=[0,4]
poptplayleftlineal, pcovplayleftlineal = curve_fit(playing_calibration, amplitude_factor_lineal, vpp_osc_left_lineal,p0=p0)
poptplayrightlineal, pcovplayrightlineal = curve_fit(playing_calibration, amplitude_factor_lineal, vpp__osc_right_lineal,p0=p0)

p1=[0,2]
p2=[0,1.5]
poptplayleftconstant, pcovplayleftconstant = curve_fit(playing_calibration, amplitude_factor_constant, vpp_osc_left_constant,p0=p1, sigma=vpp_osc_left_constant)
poptplayrightconstant, pcovplayrightconstant = curve_fit(playing_calibration, amplitude_factor_constant, vpp_osc_right_constant,p0=p2,  sigma=vpp_osc_right_constant)



plt.figure()
plt.plot(amplitude_factor,vpp_osc_left,'r.')
plt.plot(amplitude_factor, vpp__osc_right,'b.')
plt.plot(amplitude_factor_lineal, playing_calibration(amplitude_factor_lineal, poptplayleftlineal[0], poptplayleftlineal[1]),'r-')
plt.plot(amplitude_factor_lineal, playing_calibration(amplitude_factor_lineal, poptplayrightlineal[0], poptplayrightlineal[1]),'b-')
plt.plot(amplitude_factor_constant, playing_calibration(amplitude_factor_constant, poptplayleftconstant[0], poptplayleftconstant[1]),'r-')
plt.plot(amplitude_factor_constant, playing_calibration(amplitude_factor_constant, poptplayrightconstant[0], poptplayrightconstant[1]),'b-')



slope_play_left_lineal=poptplayleftlineal[0]
origin_play_left_lineal=poptplayleftlineal[1]
slope_play_right_lineal=poptplayrightlineal[0]
origin_play_right_lineal=poptplayrightlineal[1]


slope_play_left_constant=poptplayleftconstant[0]
origin_play_left_constant=poptplayleftconstant[1]
slope_play_right_constant=poptplayrightconstant[0]
origin_play_right_constant=poptplayrightconstant[1]


#%% Calibration play curves


def left_calibration(amplitudefactor):
    if amplitudefactor<0.4:
        vreal = amplitudefactor * slope_play_left_lineal + origin_play_left_lineal
        return vreal
    else:
        vreal = amplitudefactor * slope_play_left_constant + origin_play_left_constant
        return vreal

def right_calibration(amplitudefactor):
    if amplitudefactor<0.4:
        vreal = amplitudefactor * slope_play_right_lineal + origin_play_right_lineal
        return vreal
    else:
        vreal = amplitudefactor * slope_play_right_constant + origin_play_right_constant
        return vreal
    



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


#%% Calibration record curves


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
archivo = os.path.join(direc,'..', 'datos.txt')
datos= np.loadtxt(archivo)
Vcompleto=datos[:,0]
Icompleto=datos[:,1]
V=datos[10:80,0]
I=datos[10:80,1]
#plt.plot(V, I,'r.')
IV0=[]
for i in range(len(I)-1):
    if V[i]<0 and V[i+1]>0 or V[i]>0 and V[i+1]<0:
        IV0.append(I[i])
        
c=abs(np.mean(IV0))
b=np.zeros(len(I))
for i in range(len(I)):
    b[i]=(I[i]+c)


def diode_function(V, n, Io):
    kt = 300 * 1.38e-23
    q = 1.60e-19
    I_final = Io * (np.exp( (q * V) / (n * kt) ) - 1)
    return np.abs(I_final)

p0 = [2, 0]
popt, pcov = curve_fit(diode_function, V, b ,p0=p0)
plt.plot(V, diode_function(V, popt[0],popt[1]),'b-')
plt.plot(V,b,'r.')
#plt.plot(I)
#plt.plot(V)