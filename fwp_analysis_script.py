#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 19:23:44 2018

@author: Moni
@coauthor: Vall
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import os

#%% Playing calibration

# SOME CONFIGURATION

# Here I load data from a file
direc = os.path.join(os.getcwd(),'Measurements')
archivo = os.path.join(direc,
                       'Cal_Play_2000_Hz_2',
                       'Cal_Play_2000_Hz_Data.txt')
datos = np.loadtxt(archivo)
amplitude_factor = datos[:,0]
vpp_osc_left = datos[:,1]
vpp__osc_right = datos[:,2]

# DATA ANALYSIS

# First I divide data into two arrays
cut = 64

# The section [cut:] holds the increasing data to fit
amplitude_factor_lineal = amplitude_factor[cut:]
vpp_osc_left_lineal = vpp_osc_left[cut:]
vpp__osc_right_lineal = vpp__osc_right[cut:]

# The section [:cut] holds constant data to fit
amplitude_factor_constant = amplitude_factor[:cut]
vpp_osc_left_constant = vpp_osc_left[:cut]
vpp_osc_right_constant = vpp__osc_right[:cut]

# Now I plot the data to fit
plt.figure()
plt.plot(amplitude_factor_lineal, vpp_osc_left_lineal, 'r.')
plt.plot(amplitude_factor_lineal, vpp__osc_right_lineal, 'b.')

# Next I define the model's function I will use (a linear fit)
def playing_calibration(amp, m, b):
    """This function returns the linearly-calibrated played signal.
    
    Parameters
    ----------
    amp: int, float, list, np.array
        The Wave object played amplitude.
    m: int, float
        The slope of the linear fit.
    b: int, float
        The interecept of the linear fit.
    
    Returns
    -------
    vreal: type(amp)
        The calibrated played peak-to-peak amplitude in Volts, which 
        should match the oscilloscope's data.
        
    """
    
    vreal = amp * m + b
    
    return vreal

# Then I apply it to the first data (the increasing data)
p0=[0,4] # Optional initial guess for parameters
poptplayleftlineal, pcovplayleftlineal = curve_fit(
        playing_calibration,
        amplitude_factor_lineal,
        vpp_osc_left_lineal,
        p0=p0) 
poptplayrightlineal, pcovplayrightlineal = curve_fit(
        playing_calibration,
        amplitude_factor_lineal,
        vpp__osc_right_lineal,
        p0=p0)

# Next I apply it to the rest of the data (the constant data)
p1=[0,2]
p2=[0,1.5]
poptplayleftconstant, pcovplayleftconstant = curve_fit(
        playing_calibration,
        amplitude_factor_constant,
        vpp_osc_left_constant,
        p0=p1,
        sigma=vpp_osc_left_constant)
poptplayrightconstant, pcovplayrightconstant = curve_fit(
        playing_calibration,
        amplitude_factor_constant,
        vpp_osc_right_constant,
        p0=p2,
        sigma=vpp_osc_right_constant - np.mean(vpp_osc_right_constant))

# Now I plot it all at once (data and calibration)
plt.figure()
plt.plot(amplitude_factor, vpp_osc_left, 'r.')
plt.plot(amplitude_factor, vpp__osc_right, 'b.')
plt.plot(amplitude_factor_lineal,
         playing_calibration(amplitude_factor_lineal,
                             poptplayleftlineal[0],
                             poptplayleftlineal[1]),
         'r-')
plt.plot(amplitude_factor_lineal,
         playing_calibration(amplitude_factor_lineal,
                             poptplayrightlineal[0],
                             poptplayrightlineal[1]),
         'b-')
plt.plot(amplitude_factor_constant,
         playing_calibration(amplitude_factor_constant,
                             poptplayleftconstant[0],
                             poptplayleftconstant[1]),
         'r-')
plt.plot(amplitude_factor_constant,
         playing_calibration(amplitude_factor_constant,
                             poptplayrightconstant[0],
                             poptplayrightconstant[1]),
         'b-')

# These are the final parameters for the increasing data
slope_play_left_lineal=poptplayleftlineal[0]
origin_play_left_lineal=poptplayleftlineal[1]
slope_play_right_lineal=poptplayrightlineal[0]
origin_play_right_lineal=poptplayrightlineal[1]

# These are the final parameters for the constant data
slope_play_left_constant=poptplayleftconstant[0]
origin_play_left_constant=poptplayleftconstant[1]
slope_play_right_constant=poptplayrightconstant[0]
origin_play_right_constant=poptplayrightconstant[1]


#%% Playing calibration's functions

def playing_calibration_left(amplitudefactor):
    """This function returns calibrated played data for left channel.
    
    Parameters
    ----------
    amplitudefactor: int, float
        The Wave object's factor of amplitude (no units).
    
    Returns
    -------
    vreal: int, float
        The calibrated played peak-to-peak amplitude in Volts.
    
    """
    
    if amplitudefactor<0.4:
        vreal = amplitudefactor * slope_play_left_lineal
        vreal = vreal + origin_play_left_lineal
    else:
        vreal = amplitudefactor * slope_play_left_constant
        vreal = vreal + origin_play_left_constant
    
    return vreal

def playing_calibration_right(amplitudefactor):
    """This function returns calibrated played data for right channel.
    
    Parameters
    ----------
    amplitudefactor: int, float
        The Wave object's factor of amplitude (no units).
    
    Returns
    -------
    vreal: int, float
        The calibrated played peak-to-peak amplitude in Volts.
    
    """
    
    if amplitudefactor<0.4:
        vreal = amplitudefactor * slope_play_right_lineal
        vreal = vreal + origin_play_right_lineal
    else:
        vreal = amplitudefactor * slope_play_right_constant
        vreal = vreal + origin_play_right_constant
        
    return vreal

def inv_playing_calibration_left(vreal):
    """This function returns the left non-calibrated data amplitude.
    
    Parameters
    ----------
    vreal: int, float
        The calibrated played peak-to-peak amplitude in Volts.
    
    Returns
    -------
    amplitudefactor: int, float
        The Wave object's factor of amplitude (no units).
    
    """
    
    if vreal < 0.4 * slope_play_left_lineal + origin_play_left_lineal:
        slope = 1/slope_play_left_lineal
        origin = -origin_play_left_lineal / slope_play_left_lineal
    else:
        amplitudefactor = False
        print("¡Ojo! No llega a este voltaje (máx: {:.2f})".format(
                0.4 * slope_play_left_lineal + origin_play_left_lineal))
    
    amplitudefactor = slope * vreal + origin
    
    return amplitudefactor

def inv_playing_calibration_right(vreal):
    """This function returns the right non-calibrated data amplitude.
    
    Parameters
    ----------
    vreal: int, float
        The calibrated played peak-to-peak amplitude in Volts.
    
    Returns
    -------
    amplitudefactor: int, float
        The Wave object's factor of amplitude (no units).
    
    """
    
    if vreal < 0.4 * slope_play_right_lineal + origin_play_right_lineal:
        slope = 1/slope_play_right_lineal
        origin = - origin_play_right_lineal/slope_play_right_lineal
        amplitudefactor = slope * vreal + origin
    else:
        amplitudefactor = False
        print("¡Ojo! No llega a este voltaje (máx: {:.2f})".format(
            0.4 * slope_play_right_lineal + origin_play_right_lineal))
    
    return amplitudefactor

#%% Recording calibration

# SOME CONFIGURATION

# Here I load data from file
direc = os.getcwd()
archivo = os.path.join(direc,
                       'Measurements',
                       'Cal_Rec_2000_Hz_4',
                       'Cal_Rec_2000_Hz_Data.txt')
datos = np.loadtxt(archivo)
vpp_gen_func = datos[:,0]
vpp_left = datos[:,1]
vpp_right = datos[:,2]

# First I take only a part of the data
vpp_gen_func_lineal = vpp_gen_func[40:90]
vpp_left_lineal = vpp_left[40:90]
vpp_right_lineal = vpp_right[40:90]

# Now I plot the data to fit
plt.figure()
plt.plot(vpp_gen_func_lineal, vpp_left_lineal,'r.')
plt.plot(vpp_gen_func_lineal, vpp_right_lineal,'b.')

# Next I define the model's function I will use (a linear fit)
def recording_calibration(vgen, m, b):
    """This function returns the linearly-calibrated recorded signal.
    
    Parameters
    ----------
    amp: int, float, list, np.array
        The generator's peak-to-peak amplitude in Volts.
    m: int, float
        The slope of the linear fit.
    b: int, float
        The interecept of the linear fit.
    
    Returns
    -------
    vreal: type(amp)
        The calibrated played peak-to-peak amplitude in volts, which 
        should match the recorded data's.
        
    """
    
    vreal = vgen * m + b
    
    return vreal


# Now I make the fit
p0=[1.875,0] # Initial guess for parameters
poptleft, pcovleft = curve_fit(
        recording_calibration, 
        vpp_gen_func_lineal, 
        vpp_left_lineal,
        p0=p0,
        sigma=vpp_gen_func_lineal - p0[0]*vpp_left_lineal)
poptright, pcovright = curve_fit(
        recording_calibration, 
        vpp_gen_func_lineal, 
        vpp_right_lineal,
        p0=p0,
        sigma=vpp_gen_func_lineal - p0[0]*vpp_right_lineal)

# Then I plot it all toghether (data and calibration)
plt.figure()
plt.plot(vpp_gen_func, vpp_left,'r.')
plt.plot(vpp_gen_func, vpp_right,'b.')
plt.plot(vpp_gen_func_lineal, recording_calibration(vpp_gen_func_lineal, poptleft[0], poptleft[1]),'r-')
plt.plot(vpp_gen_func_lineal, recording_calibration(vpp_gen_func_lineal, poptright[0], poptright[1]),'b-')

# These are the final parameters for the data
slope_left=poptleft[0]
origin_left=poptleft[1]
slope_right=poptright[0]
origin_right=poptright[1]

#%% Calibration record curves

def recording_calibration_left(vleft):
    """Returns the left calibrated recorded signal's amplitude.
    
    Parameters
    ----------
    vleft: int, float
        The recorded non-calibrated peak-to-peak amplitude in Volts.
    
    Returns
    -------
    vreal: int, float
        The recorded calibrated peak-to-peak amplitude in Volts.
    
    """
    
    vreal = vleft / slope_left - (origin_left/slope_left)
    
    return vreal

def recording_calibration_right(vright):
    """Returns the right calibrated recorded signal's amplitude.
    
    Parameters
    ----------
    vleft: int, float
        The recorded non-calibrated peak-to-peak amplitude in Volts.
    
    Returns
    -------
    vreal: int, float
        The recorded calibrated peak-to-peak amplitude in Volts.
    
    """
    
    vreal = vright /slope_right - origin_right/slope_right
    
    return vreal

def signal_recording_calibration_left(noncal_signal):
    """Returns the left calibrated recorded signal.
    
    Parameters
    ----------
    noncal_signal: list, np.array
        The non-calibrated left recorded signal.
    
    Returns
    -------
    cal_signal: list, np.array
        The calibrated left recorded signal.
    
    """
    
    
    noncal_amplitude = max(noncal_signal) - min(noncal_signal)
    cal_amplitude = recording_calibration_left(noncal_amplitude)
    cal_signal = cal_amplitude * noncal_signal / noncal_amplitude
    
    return cal_signal

def signal_recording_calibration_right(noncal_signal):
    """Returns the right calibrated recorded signal.
    
    Parameters
    ----------
    noncal_signal: list, np.array
        The non-calibrated right recorded signal.
    
    Returns
    -------
    cal_signal: list, np.array
        The calibrated right recorded signal.
    
    """
    
    noncal_amplitude = max(noncal_signal) - min(noncal_signal)
    cal_amplitude = recording_calibration_right(noncal_amplitude)
    cal_signal = cal_amplitude * noncal_signal / noncal_amplitude
    
    return cal_signal
    
#%% Diode's IV Curve Data Calibration

# SOME CONFIGURATION

direc = os.path.join(os.getcwd(),
                     'Measurements',
                     'Diode_IV_400_Hz_1.00')
archivo = os.path.join(direc, 'Diode_IV_400_Hz_1.00.txt')
datos = np.loadtxt(archivo)
datos = datos[20000:25000, :]

chR, chL = np.split(datos, 2, axis=1)
R = 1e3
r2 = 206e3
r1 = 1e6

# DATA CALIBRATION

#V0 = (r1 + r2)*recording_calibration_right(chR)/r1
#I = recording_calibration_left(chL) / R
#V = V0 + recording_calibration_left(chL)

V0 = (r1 + r2)*signal_recording_calibration_right(chR)/r1
I = signal_recording_calibration_left(chL) / R
V = V0 + signal_recording_calibration_left(chL)

plt.figure()
plt.plot(V, I,'.')

cal_datos = np.column_stack((V,I))
np.savetxt(os.path.join(os.getcwd(),
                     'Measurements',
                     'Datos_IV_Diodo_Cal.txt'),
           cal_datos)

#%% Calibration diode

# DATA CONFIGURATION

direc = os.getcwd()
archivo = os.path.join(os.getcwd(),
                       'Measurements',
                       'Datos_IV_Diodo_Cal.txt')
datos = np.loadtxt(archivo)

# DATA ANALYSIS

Vcompleto = datos[:,0]
Icompleto = datos[:,1]
#V = datos[10:80,0]
#I = datos[10:80,1]
V = Vcompleto
I = Icompleto

IV0 = []
for i in range(len(I)-1):
    if V[i] < 0 and V[i+1] > 0 or V[i] > 0 and V[i+1] < 0:
        IV0.append(I[i])
        
c = abs(np.mean(IV0))
b = np.zeros(len(I))
for i in range(len(I)):
    b[i] = (I[i] + c)

def diode_function(V, n, Io):
    """This is the diode IV curve's model.
    
    Parameters
    ----------
    V: int, float, list, np.array
        Voltage in Volts.
    n: int
    
    I0: int, float
        Limiting current.
    
    Returns
    -------
    I_final: int, float, list, np.array
        Resultant current.
    
    """
    
    kt = 300 * 1.38e-23
    q = 1.60e-19
    I_final = Io * (np.exp( (q * V) / (n * kt) ) - 1)
    
    return I_final

p0 = [2, 0.1]
popt, pcov = curve_fit(diode_function, V, b, p0=p0)

plt.figure()
plt.plot(V, diode_function(V, popt[0], popt[1]),'b-')
plt.plot(V, b, 'r.')

print(r"n = {} y I0 = {}".format(popt[0],popt[1]))

#%% Inverting amplifier


