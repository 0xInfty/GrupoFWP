# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:49:50 2018

@author: 0xInfty
"""

import numpy as np
from scipy.signal import sawtooth, square

def waveform(key, n, m=1):
    """Makes a period of a wave of form 'key' on an array of lenght 'n'.
    
This function defines a period of a wave. Its waveform is chosen with \
the input 'key' which can take a limited number of values: 'sin' for \
a sine, 'tri' for a triangle wave, 'saw' for increasing linear and \
'squ' for square wave. Its digital resolution is given by the input \
'n' which is the number of values it takes in a period and which is \
therefore the number of intervals the period is divided into.


Parameters
----------
key: str {'sin', 'tri', 'saw', 'squ'}
    Waveform
n: int
    Resolution


Returns
-------
wave: array
    Period of a wave, array of length n


Raises
------
- KeyError("Los posibles valores de key son: 'sin', 'tri', 'saw', \
'freq', 'squ'") if a wrong waveform key is given.

           
Warnings
--------
- The returned waveform is normalized to 1 (its maximum amplitude is 1).
- The returned waveform is centered on 0 (it's a symmetric function \
whose minimum amplitude is -1).
    
    """

    if key == 'sine':
                
        out = np.sin(2*np.pi*np.arange(n)*m/n)

    elif key == 'tri':
                
        out = sawtooth(2*np.pi*np.arange(n)*m/n, 0.5)
    
    elif key == 'squ':
    
        out = square(2*np.pi*np.arange(n)*m/n)
        
    elif key == 'saw+':
        
        out = sawtooth(2*np.pi*np.arange(n)*m/n, 1)
        
    elif key == 'saw-':
        
        out = sawtooth(2*np.pi*np.arange(n)*m/n, 0)
        
    else:        

        raise KeyError("Los posibles valores de key son: 'sine', 'tri', \
        'saw+', 'saw-', 'freq', 'squ'.")
    
    return out