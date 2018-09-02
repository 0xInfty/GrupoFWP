# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:49:50 2018

@author: Usuario
"""

def waveform(key):

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
        return switcher.get(key, lambda: "Invalid keyword")
    
    else:
        raise KeyError("Los posibles valores de key son: 'sin', 'tri'.")
        return
