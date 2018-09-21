# -*- coding: utf-8 -*-
""" This module works as a function generator

It includes:
Defined functions for several waveforms incorporating a switcher to make choosing easier.
A frequency sweep function
A class for evaluating the multiple waveforms
"""
import numpy as np
from scipy.signal import sawtooth, square
    
def create_sine(time, freq, *args):
    """ Creates sine wave 
    
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sine wave
    
    args : dummy 
        used to give compatibility with other functions
    
    Returns
    -------
    
    Evaluated sine wave of given frequency
    """
    
    wave =np.sin(2 * np.pi * time * freq)
    return wave        
    
def create_ramps(time, freq, type_of_ramp=1):
    """ Creates ascending and descending sawtooth wave,
    or a tringle wave, depending on the value of type_of_ramp,
    using the function 'sawtooth' from scypy signal module.
    Used by create_sawtooth_up, create_sawtooth_down and 
    create_triangular.
    
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of created wave
    
    type_of_ramp : {0, 1, 2}
        0 returns a sawtooth waveform with positive slope
        1 returns a sawtooth waveform with negative slope
        0 returns a triangle waveform
    
    Returns
    -------
    
    Evaluated sawtooth or triangle wave of given frequency
    """
    
    wave = sawtooth(2 * np.pi * time * freq, type_of_ramp)
    return wave
    
def create_sawtooth_up(time, freq, *args):
    """ Creates sawtooth waveform with positive slope
   
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sawtooth wave

    args : dummy 
        used to give compatibility with other functions

    Returns
    -------
    
    Evaluated sawtooth waveform with positive slope  and given frequency
    """
    
    wave = create_ramps(time ,freq, 1)
    return wave        

def create_sawtooth_down(time, freq, *args):
    """ Creates sawtooth waveform with negative slope
   
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sawtooth wave
        
    args : dummy 
        used to give compatibility with other functions

    Returns
    -------
    
    Evaluated sawtooth waveform with negative slope and given frequency
    """

    wave = create_ramps(time, freq, 0)
    return wave        

def create_triangular(time, freq, *args):
    """ Creates a triangular wave with symmetric ramps
   
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of triangular wave
        
    args : dummy 
        used to give compatibility with other functions

    Returns
    -------
    
    Evaluated triangular waveform with given frequency
    """
    

    wave = create_ramps(time, freq, .5)
    return wave        
     
def create_square(time, freq, dutycycle = .5, *args):
    """ Creates a square wave. Uses square function from
    scypy signal module

    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of square wave
        
    dutycycle=.5 : scalar or numpy array
        Duty cycle. Default is 0.5 (50% duty cycle). If 
        an array, causes wave shape to change over time,
        and must be the same length as time.
        
    args : dummy 
        used to give compatibility with other functions

    Returns
    -------
    
    Evaluated square waveform with given frequency
    """
    
    wave = square(2 * np.pi * time * freq, dutycycle)
    return wave
    
def create_custom(time, freq, *args):
    """ Creates a wave from given custom function. 
    
    Useful to get compatibility between the custom function provided and other
    modules like PyAudioWave.

    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of custom wave
        
    args : (*params, custom_func)
        *params should contain the parameters that will be passed to the custom
        function provided
        
    Returns
    -------
    
    Evaluated square waveform with given frequency
    """
    #last argument is the function, the rest are parameters
    *params, custom_func = args
    wave = custom_func(time, freq, *params)
    return wave

def create_sum(time, freq, amp, *args):
    """ Creates an arbitraty sum of sine waves.

    It uses the frequencies in freq and either uniform
    amplitude if amp is None, or the given amplitudes if
    amp is array-like. Output comes out normalized.
    
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : array-like
        expected frequency of sine wave
       
    amp : None or array-like 
        if None, amplitude of all summed waves is equal. If
        array-like, it should be same length as freq.
        
    args : dummy 
        used to give compatibility with other functions

    Returns
    -------
    
    Evaluated square waveform with given frequency
    """
    
    if len(amp)==0:
        #If am wasn't given, it is an empty tuple
        amp = np.ones(len(freq))
    
    if len(freq) != len(amp):
        raise ValueError('Amplitud and frequency arrays should e the same leght!')
    
    wave = np.zeros(time.shape)
    for f, a in zip(freq, amp):
        wave += create_sine(time, f) * a
    #Normalize it:
    wave /= sum(amp) 

    return wave
      
def given_waveform(input_waveform):
    """ Switcher to easily choose waveform.
    
    If the given waveform is not in the list, it raises a TypeError and a list
    containing the accepted inputs.
    
    Parameters
    ----------
    input_waveform : string
        name of desired function to generate
   
    Returns
    -------
    Chosen waveform function
    """
    
    switcher = {
        'sine': create_sine,
        'sawtoothup': create_sawtooth_up,
        'sawtoothdown': create_sawtooth_down  ,          
        'ramp': create_sawtooth_up, #redirects to sawtoothup
        'sawtooth': create_sawtooth_up, #redirects to sawtoothup
        'triangular': create_triangular,
        'square': create_square,
        'custom': create_custom,
        'sum': create_sum
    }
    func = switcher.get(input_waveform, wrong_input)
    return func
       
def wrong_input(*args):
    raise TypeError('''Given waveform is invalid. Choose from following list:
        sine, triangular, ramp, sawtooth, sawtoothup, sawtoothdown, square, custom''')

        
#%% Clase que genera ondas

class Wave:
    '''Generates an object with a two methods: evaluate(time).
  
    Attributes
    ----------
    waveform : str {'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 'triangular', 'square', 'custom'} optional
        waveform type. If 'custom', function should acept inputs
        (time, frequency, *args). Default = 'sine'
    frequency : float (optional)
        wave frequency
    amplitude : float (optional)
        wave amplitud
        
    Methods
    ----------
    evaluate(time)
        returns evaluated function type

    '''
    
    def __init__(self, waveform='sine', frequency=400, amplitude=1, *args):
        self.frequency = frequency
        self.amplitude = amplitude
        self.waveform = given_waveform(waveform)
        self.extraargs = args
        
    def evaluate(self, time, *args):
        """Takes in an array-like object to evaluate the funcion in.
        
        Parameters
        ----------
        time : array
            time vector in which to evaluate the funcion
        args : tuple (optional)
            extra arguments to be passed to evaluated function
            
        Returns
        -------
        
        Evaluated waveform 
        """          

        if isinstance(self.amplitude, (list, tuple, np.ndarray)):
            #for sums 
            wave = self.waveform(time, self.frequency, self.amplitude)
        else:
            wave = self.waveform(time, self.frequency, *args, self.extraargs) * self.amplitude
        return wave
