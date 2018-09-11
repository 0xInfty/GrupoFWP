# -*- coding: utf-8 -*-
"""
RMS function

@author: 0xInfty
"""

def rms(data):
    """Takes a list or array and returns RMS value.


Variables
---------
data: array or list
    Data to be analized.


Returns
-------
float
    RMS value of analized data.
    
    """
    
    import numpy as np
    
    return np.sqrt(np.mean((np.array(data))**2))