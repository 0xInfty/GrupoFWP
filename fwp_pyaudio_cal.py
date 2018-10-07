# -*- coding: utf-8 -*-
"""
The 'fwp_pyaudio_cal' module generates calibration functions for playing 
and recording with PyAudio. It takes its data from 'Cal_Play_Data.txt' 
and 'Cal_Rec_Data' from 'GrupoFWP/'. It must be lunched from 'GrupoFWP'.

It contains...
play_cal_left : function
    Takes desired left Vpp amplitude and returns Wave amplitude factor.
play_cal_right : function
    Takes desired right Vpp amplitude and returns Wave amplitude factor.
play_rec_left : function
    Takes recorded left peak-to-peak amplitude and returns Vpp.
play_rec_right : function
    Takes recorded right peak-to-peak amplitude and returns Vpp.
signal_play_rec_left : function
    Takes recorded left signal and returns calibrated signal.
signal_play_rec_right : function
    Takes recorded right signal and returns calibrated signal.

@author: Vall
"""

import os
import numpy as np

#%% Playing calibration

archivo = os.path.join(os.getcwd(), 'Cal_Play_Data.txt')
cal_play_data = np.loadtxt(archivo)

#%% Playing calibration functions

def play_cal_left(vreal):
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
    
    if vreal < 0.4 * cal_play_data[0,0] + cal_play_data[1,0]:
        slope = 1 / cal_play_data[0,0]
        origin = -cal_play_data[1,0] / cal_play_data[0,0]
    else:
        amplitudefactor = False
        print("¡Ojo! No llega a este voltaje (máx: {:.2f})".format(
                0.4 * cal_play_data[0,0] + cal_play_data[1,0]))
    
    amplitudefactor = slope * vreal + origin
    
    return amplitudefactor

def play_cal_right(vreal):
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
    
    if vreal < 0.4 * cal_play_data[0,1] + cal_play_data[1,1]:
        slope = 1 / cal_play_data[0,1]
        origin = -cal_play_data[1,1] / cal_play_data[0,1]
    else:
        amplitudefactor = False
        print("¡Ojo! No llega a este voltaje (máx: {:.2f})".format(
                0.4 * cal_play_data[0,1] + cal_play_data[1,1]))
    
    amplitudefactor = slope * vreal + origin
    
    return amplitudefactor


#%% Inverse playing calibration's functions

def inv_play_cal_left(amplitudefactor):
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
        vreal = amplitudefactor * cal_play_data[0,0]
        vreal = vreal + cal_play_data[1,0]
    else:
        vreal = amplitudefactor * cal_play_data[2,0]
        vreal = vreal + cal_play_data[3,0]
    
    return vreal

def inv_play_cal_right(amplitudefactor):
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
        vreal = amplitudefactor * cal_play_data[0,1]
        vreal = vreal + cal_play_data[1,1]
    else:
        vreal = amplitudefactor * cal_play_data[2,1]
        vreal = vreal + cal_play_data[3,1]
        
    return vreal

#%% Recording calibration

archivo = os.path.join(os.getcwd(), 'Cal_Rec_Data.txt')
rec_cal_data = np.loadtxt(archivo)

#%% Record calibration's functions

def rec_cal_left(vleft):
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
    
    vreal = vleft / rec_cal_data[0,0] 
    vreal = vreal - (rec_cal_data[1,0]/rec_cal_data[0,0])
    
    return vreal

def rec_cal_right(vright):
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
    
    vreal = vright / rec_cal_data[0,1] 
    vreal = vreal - (rec_cal_data[1,1]/rec_cal_data[0,1])
    
    return vreal

def signal_rec_cal_left(noncal_signal):
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
    cal_amplitude = rec_cal_left(noncal_amplitude)
    cal_signal = cal_amplitude * noncal_signal / noncal_amplitude
    
    return cal_signal

def signal_rec_cal_right(noncal_signal):
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
    cal_amplitude = rec_cal_right(noncal_amplitude)
    cal_signal = cal_amplitude * noncal_signal / noncal_amplitude
    
    return cal_signal