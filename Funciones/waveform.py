# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:49:50 2018

@author: 0xInfty
"""

def waveform(key, n, freq = 440):
    """Makes a period of a wave of form 'key' on an array of lenght 'n'.
    
This function defines a period of a wave. Its waveform is chosen with \
the input 'key' which can take a limited number of values: 'sin' for \
a sine, 'tri' for a triangle wave, 'saw' for increasing linear, 'squ' \
for square wave and 'freq' for a sine with freq periods inside. Its \
digital resolution is given by the input 'n' which is the number of \
values it takes in a period and which is therefore the number of \
intervals the period is divided into.


Parameters
----------
key: str {'sin', 'tri', 'saw', 'freq', 'squ'}
    Waveform
n: int
    Resolution

    
Other parameters
----------------
freq: int, float
    Frequency for 'freq' key.


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

    import numpy as np

    if key == 'sin':
                
        out = np.sin(2*np.pi*np.arange(n)/n)

    elif key == 'tri':
                
        out = np.zeros(n)
        
        out[0:n//2+1] = np.linspace(0,1,n//2+1)
        out[n//2:n] = np.linspace(1,0,n//2+1)[0:n//2]
    
    elif key == 'freq':
        
        out = np.sin(2*np.pi*np.arange(n)*freq/n)
    
    elif key == 'squ':
    
        out = np.zeros(n)
        
        out[0:n//2+1] = np.ones(n//2+1)
        out[n//2:n] = -np.ones(n//2+1)
        
    elif key == 'saw':
        
        out = np.linspace(0,1,n)
        
    else:        

        raise KeyError("Los posibles valores de key son: 'sin', 'tri', \
        'saw', 'freq', 'squ'.")
    
    return out