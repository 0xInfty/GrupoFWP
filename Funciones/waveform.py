# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:49:50 2018

@author: 0xInfty
"""

def waveform(key, n):
    """Makes a period of a wave of form 'key' on an array of lenght 'n'.
    
This function defines a period of a wave. Its waveform is chosen with \
the input 'key' which can take a limited number of values: 'sin' for \
a sine, 'tri' for a triangle wave. Its digital resolution is given by \
the input 'n' which is the number of values it takes in a period and \
which is therefore the number of intervals the period is divided into.

Variables:
>> key (str) [waveform]
>> n (int) [resolution]

Returns:
>> wave (array) [period of a wave, array of length n]

Raises:
- KeyError("Los posibles valores de key son: 'sin', 'tri'") if a wrong \
waveform key is given.

Beware:
- The returned waveform is normalized to 1 (its maximum amplitude is 1).
- The returned waveform is centered on 0 (it's a symmetric function \
whose minimum amplitude is -1).
    
    """

    if key == 'sin':
        
        from numpy import sin, pi, arange
        
        return sin(2*pi*arange(n)/n)

    elif key == 'tri':
        
        from numpy import zeros, linspace
        
        out = zeros(n)
        
        out[0:n//2+1] = linspace(0,1,n//2+1)
        out[n//2:n] = linspace(1,0,n//2+1)[0:n//2]
        
        return out

    else:        

        raise KeyError("Los posibles valores de key son: 'sin', 'tri'.")
        return