# -*- coding: utf-8 -*-
""" This module works as a function generator

It includes:
Defined functions for several waveforms incorporating a switcher to make choosing easier.
A frequency sweep function
A class for evaluating the multiple waveforms
"""
import numpy as np
from scipy.signal import sawtooth, square
    
def create_sine(time, freq):
    """ Creates sine wave 
    
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sine wave
    
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
        expected frequency of sine wave
    
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
    
def create_sawtooth_up(time, freq):
    """ Creates sawtooth waveform with positive slope
   
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sine wave

    Returns
    -------
    
    Evaluated sawtooth waveform with positive slope  and given frequency
    """
    
    wave = create_ramps(time ,freq, 1)
    return wave        

def create_sawtooth_down(time, freq):
   """ Creates sawtooth waveform with negative slope
   
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sine wave

    Returns
    -------
    
    Evaluated sawtooth waveform with negative slope and given frequency
    """

    wave = create_ramps(time, freq, 0)
    return wave        

def create_triangular(time, freq):
    """ Creates a triangular wave with symmetric ramps
   
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sine wave

    Returns
    -------
    
    Evaluated triangular waveform with given frequency
    """
    

    wave = create_ramps(time, freq, .5)
    return wave        
     
def create_square(time, freq):
    """ Creates a square wave. Uses square function from
    scypy signal module

    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    freq : int or float
        expected frequency of sine wave

    Returns
    -------
    
    Evaluated square waveform with given frequency
    """
    
    wave = square(2 * np.pi * time * freq)
    return wave
    
def create_custom(time, freq, custom_func):
    """ Allows used defined wavefom. Not yet implemented.
    """
    
    raise Exception('Not yet implemented.')
      
def given_waveform(input_waveform):
    """ Switcher to easily choose waveform
    
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
    }
    func = switcher.get(input_waveform,lambda: 'Invalid waveform.')
    return func
       

def function_creator(waveform, freq=400, duration=1, amp=1, samplig_freq=17000, *arg):
    """Creates desired waveform
    
    Parameters
    ----------
    waveform : str
        String from list declaring type of function to use.
    freq : float optional
        frequency of signal in Hz. Default: 400HZ
    duration : float optional
        Sample length in seconds. Default: 1 second
    amp : float optional
        Amplitude a s a fraction of maximum aplitude. Default: 1
    sampling_freq : int optional
        Sampling frequency in Hz.
        
    Returns
    -------
    Array with evaluated waveform from given type and designated parameters
    """
    
    time = np.arange(samplig_freq * duration)/samplig_freq
    func = given_waveform(waveform)
    wave = func(time, freq) * amp
    return wave
    
def function_generator(waveform, freq=400, duration=None, amp=1,
                       periods_per_chunk=1, samplig_freq=17000, *arg):
    """Creates desired waveform with a generator
    
    Parameters
    ----------
    waveform : str
        String from list declaring type of function to use.
    freq : float optional
        frequency of signal in Hz. Default: 400Hz.
    duration : float optional
        Sample length in seconds. If duration is None, it will yield
        samples indefinitely. Default: None.
    amp : float optional
        Amplitude a s a fraction of maximum aplitude. Default: 1.
    periods_per_chunk : int optional
        Amount of wave periods to include in each yield. Default: 1.
    sampling_freq : int optional
        Sampling frequency in Hz.
    
    Returns
    -------
    wave : array 
        Evaluated function of given waveform with a lenght of designated amount of periods
    """

    period = 1/freq
    time = np.arange(period * periods_per_chunk, step=1/samplig_freq) #time vector 1 period long
    func = given_waveform(waveform)
    wave = func(time, freq) * amp
    
    if duration is not None:
        for _ in range(duration//period): 
            yield wave
    else:
        while True: 
            yield wave


def frequency_sweep(freqs_to_sweep=np.arange(100,1000,10), amplitude=1, 
                   waveform='sine', duration_per_freq=1, 
                   silence_between_freq=0, sampling_freq=17000):
    """ Generator that yields selected waveform with a 
    different frecuency each time it is called
    
    Parameters
    ----------
    freqs_to_sweep : tuple or array-like
        If tuple: expects (start, stop, step) tuple and generates an array 
        using np.arrange. If array, size should be (n_freqs, ) and contain
        the frequency values to sweep in Hz. Default: sweeps from 100Hz to
        1000Hz every 10Hz.
    amp : float or array-like
        Amplitud of generated wave.  If array-like, length should be equal
        to ammount of frequency values to sweep. Default: 1.
    waveform : str
        Type of waveform to use. Can be 'sine', 'sawtoothup', 'sawtoothdown',
        'ramp', 'triangular', 'square' or 'custom'. Default: sine.
    duration_per_freq : float or array-like
        Duration of each frequency stretch in seconds. If array-like, length 
        should be equal to ammount of frequency values to sweep. 
        Default: 1 second.
    silence_between_freq : float or array-like
        Time to wait between each frequency in seconds. If array-like, length 
        should be equal to ammount of frequency values to sweep. 
        Default: 0 seconds.
        
    Returns
    ----------
    wave : array
    evaluated waveform of given parameters with a different frecuency each time
    the generator is called
    
    """
    
#    Crete frequency array, if necessary
    if isinstance(freqs_to_sweep,tuple):
        if not len(freqs_to_sweep)==3:
            raise ValueError('Tuple length must be 3 containing (start, stop, step).')
        freqs_to_sweep = np.arrange(*freqs_to_sweep) #Unpack freqs array
                                 
    N_freqs = len(freqs_to_sweep)#ammount of frequencies to sweep
    
    
#    Transform all variables that are not iterables to lists of correct length
    if isinstance(amplitude,float):
        amplitude = [amplitude] * N_freqs
        
    if isinstance(duration_per_freq,float):
        duration_per_freq = [duration_per_freq] * N_freqs
        
    if isinstance(silence_between_freq,float):
        silence_between_freq = [silence_between_freq] * N_freqs
    
    for freq, duration, amp, silence in zip(freqs_to_sweep,
                                            amplitude,
                                            duration_per_freq,
                                            silence_between_freq):
        wave = function_creator(waveform, freq, duration, amp, sampling_freq)
        
        yield wave
        
#%% Clase que genera ondas

class Wave:
    '''Generates an object with a two methods: evaluate(time) and generate (not implemented).
  
    Attributes
    ----------
    waveform : str {'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 'triangular', 'square', 'custom'} optional
        waveform type.  Default = 'sine'
    frequency : float
        wave frequency
    amplitude : float
        wave amplitud
        
    Methods
    ----------
    evaluate(time)
        returns evaluated function type
    generate()
        not yet implemented
    '''
    
    def __init__(self, waveform='sine', frequency=400, amplitude=1):
        self.frequency = frequency
        self.amplitude = amplitude
        self.waveform = given_waveform(waveform)
        
    def evaluate(self, time):
    """Takes in an array-like object to evaluate the funcion in.
    
    Parameters
    ----------
    time : array
        time vector in which to evaluate the funcion
    
    self : 
        
    Returns
    -------
    
    Evaluated waveform 
    """
          
        
        wave = self.waveform(time, self.frequency) * self.amplitude
        return wave
    
#    def generate(self, time, chunk_size):
        
