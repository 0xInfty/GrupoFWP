# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:49:50 2018

@author: Usuario
"""

def waveform(key):
    """Makes a function that will return a waveform given by 'key'.
    
This function defines a function that will return a period of a wave. \
Its waveform is chosen with the input 'key' which can take a limited \
number of values: 'sin' for a sine, 'tri' for a triangle wave. The \
returned function will take only one argument called 'n' which sets \
the digital resolution of the wave (n will be the number of values it \
takes in a period and will therefore be the number of intervals the \
period is divided into).

Variables:
>> key (str) [waveform]

Returns:
>> waveform (function) [returns a period of a wave, array of length n]

Raises:
- KeyError("Los posibles valores de key son: 'sin', 'tri'") if a wrong \
waveform key is given.

Beware:
- The returned waveform is normalized to 1 (its maximum amplitude is 1).
- The returned waveform is centered on 0 (it's a symmetric function \
whose minimum amplitude is -1).
    
    """
    
    def sin(n):
        
        from numpy import sin, pi, arange
        
        return sin(2*pi*arange(n)/n)
    
    
    def tri(n):
        
        from numpy import zeros, linspace
        
        out = zeros(n)
        
        out[0:n//2+1] = linspace(0,1,n//2+1)
        out[n//2:n] = linspace(1,0,n//2+1)[0:n//2]
        
        return out
    
    switcher = {'sin': sin, 'tri': tri}
    
    if key in switcher:       
        return switcher.get(key)
    
    else:
        raise KeyError("Los posibles valores de key son: 'sin', 'tri'.")
        return
