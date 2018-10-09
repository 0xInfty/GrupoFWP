#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 19:23:44 2018

@author: Moni
@coauthor: Vall
"""

import fwp_analysis as anly
import fwp_format as fmt
import fwp_save as sav
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

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
print("Left lineal")
print("m = {}".format(fmt.error_value(
        poptplayleftlineal[0],
        np.sqrt(pcovplayleftlineal[0,0]),
        units='Vpp')))
print("b = {}".format(fmt.error_value(
        poptplayleftlineal[1],
        np.sqrt(pcovplayleftlineal[1,1]),
        string_scale=False)))
print("Right lineal")
print("m = {}".format(fmt.error_value(
        poptplayrightlineal[0],
        np.sqrt(pcovplayrightlineal[0,0]),
        units='Vpp')))
print("b = {}".format(fmt.error_value(
        poptplayrightlineal[1],
        np.sqrt(pcovplayrightlineal[1,1]),
        string_scale=False)))


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
print("Left constant")
print("m = {}".format(fmt.error_value(
        poptplayleftconstant[0],
        np.sqrt(pcovplayleftconstant[0,0]),
        units='Vpp')))
print("b = {}".format(fmt.error_value(
        poptplayleftconstant[1],
        np.sqrt(pcovplayleftconstant[1,1]),
        string_scale=False)))
print("Right constant")
print("m = {}".format(fmt.error_value(
        poptplayrightconstant[0],
        np.sqrt(pcovplayrightconstant[0,0]),
        units='Vpp')))
print("b = {}".format(fmt.error_value(
        poptplayrightconstant[1],
        np.sqrt(pcovplayrightconstant[1,1]),
        string_scale=False)))

# Now I plot it all at once (data and calibration)
plt.figure()
plt.plot(amplitude_factor, vpp_osc_left, 'ro', label="Izquierda")
plt.plot(amplitude_factor, vpp__osc_right, 'bo', label="Derecha")
plt.plot(amplitude_factor_lineal,
         playing_calibration(amplitude_factor_lineal,
                             poptplayleftlineal[0],
                             poptplayleftlineal[1]),
         'k-',
         label="Fit Izquierda")
plt.plot(amplitude_factor_lineal,
         playing_calibration(amplitude_factor_lineal,
                             poptplayrightlineal[0],
                             poptplayrightlineal[1]),
         'k-',
         label="Fit derecha")
plt.plot(amplitude_factor_constant,
         playing_calibration(amplitude_factor_constant,
                             poptplayleftconstant[0],
                             poptplayleftconstant[1]),
         'k-')
plt.plot(amplitude_factor_constant,
         playing_calibration(amplitude_factor_constant,
                             poptplayrightconstant[0],
                             poptplayrightconstant[1]),
         'k-')
plt.title("Calibración de reproducción")
plt.xlabel("Factor de amplitud")
plt.ylabel("Amplitud real (Vpp)")
plt.legend()
fmt.plot_style(plt.gcf().number, dimensions=[1.15,1.05,1,1])
sav.saveplot(os.path.join(direc, 'Cal_Play_Plot.pdf'), overwrite=True)

# This are the final parameters, which I save
cal_play_data = np.array([[poptplayleftlineal[0], # Slope lineal left
                           poptplayleftlineal[1],  # Origin lineal left
                           poptplayleftconstant[0], # Slope const left
                           poptplayleftconstant[1]], # Origin const left
                          [poptplayrightlineal[0],
                           poptplayrightlineal[1],
                           poptplayrightconstant[0],
                           poptplayrightconstant[1]]])
         
sav.savetext(cal_play_data.T,
             os.path.join(os.getcwd(), 'Cal_Play_Data.txt'),
             overwrite = True)

#%% Recording calibration

# SOME CONFIGURATION

# Here I load data from file
direc = os.path.join(os.getcwd(), 'Measurements')
archivo = os.path.join(direc,
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

print("Left")
print("m = {}".format(fmt.error_value(
        poptleft[0],
        np.sqrt(pcovleft[0,0]),
        units='/Vpp', 
        legend=True)))
print("b = {}".format(fmt.error_value(
        poptleft[1],
        np.sqrt(pcovleft[1,1]),
        string_scale=False, 
        legend=True)))
print("Right")
print("m = {}".format(fmt.error_value(
        poptright[0],
        np.sqrt(pcovright[0,0]),
        units='/Vpp', 
        legend=True)))
print("b = {}".format(fmt.error_value(
        poptright[1],
        np.sqrt(pcovright[1,1]),
        string_scale=False, 
        legend=True)))

# Then I plot it all toghether (data and calibration)
plt.figure()
plt.subplot(211)
plt.title("Calibración de grabación")
plt.ylabel('Amplitud left (pp)')
plt.plot(vpp_gen_func, vpp_left, 'ro', label="Izquierda")
plt.plot(vpp_gen_func_lineal, 
         recording_calibration(vpp_gen_func_lineal, 
                               poptleft[0], 
                               poptleft[1]),
         'k-',
         label="Fit Izquierda")
plt.legend(loc='lower right')
plt.subplot(212)
plt.xlabel('Amplitud real (Vpp)')
plt.ylabel('Amplitud right (pp)')
plt.plot(vpp_gen_func, vpp_right, 'bo', label="Derecha")
plt.plot(vpp_gen_func_lineal,
         recording_calibration(vpp_gen_func_lineal,
                               poptright[0],
                               poptright[1]),
         'k-',
         label="Fit Derecha")
plt.legend(loc='lower right')
fmt.plot_style(plt.gcf().number)
sav.saveplot(os.path.join(direc, 'Cal_Rec_Plot.pdf'), overwrite=True)

# These are the final parameters for the data, which I save
rec_cal_data = np.array([[poptleft[0], poptleft[1]], # Left
                         [poptright[0], poptright[1]]]).T # Right
sav.savetext(rec_cal_data,
             os.path.join(os.getcwd(), 'Cal_Rec_Data.txt'),
             overwrite = True)

#%% Diode's IV Curve Data Calibration

import fwp_pyaudio_cal as cal

# SOME CONFIGURATION

direc = os.path.join(os.getcwd(),
                     'Measurements',
                     'Diode_IV_400_Hz_1.00')
archivo = os.path.join(direc, 'Diode_IV_400_Hz_1.00.txt')
datos = np.loadtxt(archivo)
datos = datos[20000:25000, :]

chR, chL = np.split(datos, 2, axis=1)
R = 1e3
r2 = 5.75e3 #206e3
r1 = 1e6

# DATA CALIBRATION

#V0 = (r1 + r2)*recording_calibration_right(chR)/r1
#I = recording_calibration_left(chL) / R
#V = V0 + recording_calibration_left(chL)

V0 = (r1 + r2)*cal.signal_rec_cal_right(chR)/r1
I = cal.signal_rec_cal_left(chL) / R
V = V0 + cal.signal_rec_cal_left(chL)

plt.figure()
plt.plot(V, I,'.')

cal_datos = np.column_stack((V,I))
sav.savetext(cal_datos,
             os.path.join(os.getcwd(),
                     'Measurements',
                     'Datos_IV_Diodo_Cal.txt'),
             overwrite=True)

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
plt.xlabel("Voltaje [V]")
plt.ylabel("Corriente[A]")
plt.legend(["Ajuste","Datos"])
plt.grid()
plt.savefig('diodofeo.pdf')
plt.show()
print(r"n = {} y I0 = {}".format(popt[0],popt[1]))

#%% Inverting amplifier

import fwp_pyaudio_cal as cal

direc = os.path.join(os.getcwd(),
                     'Measurements',
                     'Inv_Amp_x1')
file = os.path.join(direc, 'Inv_Amp_x1.txt')
datos = np.loadtxt(file)

# First I drop the initial silence of the measurement
datos = datos[int(len(datos)*2/5):]

# Then I calibrate it
datos[:,0] = (22+15) * cal.signal_rec_cal_left(datos[:,0]) / 15
datos[:,1] = (22+15) * cal.signal_rec_cal_right(datos[:,1]) / 15

# Now I would like to see the actual amplification
rsq, m, b = anly.linear_fit(datos[:,0], -datos[:,1],
                            mb_units=('','V'),
                            mb_string_scale=(True,True),
                            text_position=(0.02, 0.7))
plt.show()
fmt.plot_style(plt.gcf().number, dimensions=[1.15,1.05,1,1])
plt.xlabel("Señal de entrada (V)")
plt.ylabel("Señal de salida (V)")
sav.saveplot(os.path.join(direc, 'Amplification.pdf'), overwrite=True)

#%% Inverting amplifier Freq_Sweep

import fwp_pyaudio_cal as cal

rIN0 = 39
rIN = 3.768e3
rIN2 = 4.7e3
rOUT = 10
rMIC = 10e3

amp = (rIN+rIN2)/rIN0
ampMIC2 = (15+22)/15
ampMIC1 = (rMIC+rOUT)/rOUT

samplerate = 44100
freq_start = 100
freq_end = 20e3
freq_step = 100
frequencies = np.arange(freq_start, freq_end, freq_step)
          
name = 'Amp_Freq_{}_{}_Ohms'.format(rIN, rMIC)
savedir = os.path.join(os.getcwd(),
                       'Measurements',
                       name)
filename = os.path.join(savedir, name)
makefile = lambda freq: '{}_{:.2f}_Hz.txt'.format(filename, freq)

rms = []
for freq in frequencies:
    
    print(freq, "Hz")
    
    data = np.loadtxt(makefile(freq))
    data[:,0] = cal.signal_rec_cal_left(data[:,0])*ampMIC1
    data[:,1] = cal.signal_rec_cal_right(data[:,1])*ampMIC2
    data = data[int(2*len(data[:,0])/5):,:]
    ndata = len(data)
    rms.append(anly.rms(data[:,0]), anly.rms[data[:,1]])
    
rms = np.array(rms)
decibels = 10*np.log10(rms[:,1]/rms[:,0])
alldata = np.array([frequencies, rms[:,0], rms[:,1], decibels]).T

plt.figure()
plt.plot(data[:,0], data[:,3],'o-')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Decibeles (dB)')
plt.title('Ancho de banda G = {:.2f}'.format(amp))
fmt.plot_style(plt.gcf().number, dimensions=[1.4,1.05,1,1])
sav.saveplot(os.path.join(savedir, 'Amp_Freq_Plot.pdf'), overwrite=True)
sav.savetext(alldata, os.path.join(savedir, 'Amp_Freq_Data.txt'))
