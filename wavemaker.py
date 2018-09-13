# -*- coding: utf-8 -*-
"""
Crea funciones
"""
import numpy as np
from scipy.signal import sawtooth, square
    
def create_sine(time, freq):
    """ Creates sine wave """
    wave =np.sin(2 * np.pi * time * freq)
    return wave        
    
def create_ramps(time, freq, type_of_ramp=1):
    """ Creates ascending and descending sawtooth wave,
    or a tringle wave, depending on the value of type_of_ramp.
    Used by create_sawtooth_up, create_sawtooth_down and 
    create_triangular."""

    wave = sawtooth(2 * np.pi * time * freq, type_of_ramp)
    return wave
    
def create_sawtooth_up(time, freq):
    """ Creates a sawtooth wave with ascending ramps"""
    wave = create_ramps(time ,freq, 1)
    return wave        

def create_sawtooth_down(time, freq):
    """ Creates a sawtooth wave with descending ramps"""
    wave = create_ramps(time, freq, 0)
    return wave        

def create_triangular(time, freq):
    """ Creates a triangular wave with symmetric ramps"""
    wave = create_ramps(time, freq, .5)
    return wave        
     
def create_square(time, freq):
    wave = square(2 * np.pi * time * freq)
    return wave
    
def create_custom(time, freq, custom_func):
    raise Exception('Not yet implemented.')
      
def given_waveform(input_waveform):
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
    """
    waveform: str
        String from list declaring type of function to use.
    freq: float
        frequency of signal in Hz. Default: 400HZ
    duration: float
        Sample length in seconds. Default: 1 second
    amp: float
        Amplitude a s a fraction of maximum aplitude. Default: 1
    sampling_freq: int
        Sampling frequency in Hz.
    """
    time = np.arange(samplig_freq * duration)/samplig_freq
    func = given_waveform(waveform)
    wave = func(time, freq) * amp
    return wave
    
def function_generator(waveform, freq=400, duration=None, amp=1,
                       periods_per_chunk=1, samplig_freq=17000, *arg):
    """
    waveform: str
        String from list declaring type of function to use.
    freq: float
        frequency of signal in Hz. Default: 400Hz.
    duration: float
        Sample length in seconds. If duration is None, it will yield
        samples indefinitely. Default: None.
    amp: float
        Amplitude a s a fraction of maximum aplitude. Default: 1.
    periods_per_chunk: int
        Amount of wave periods to include in each yield. Default: 1.
    sampling_freq: int
        Sampling frequency in Hz.
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
    """
    freqs_to_sweep: tuple or array-like
        If tuple: expects (start, stop, step) tuple and generates an array 
        using np.arrange. If array, size should be (n_freqs, ) and contain
        the frequency values to sweep in Hz. Default: sweeps from 100Hz to
        1000Hz every 10Hz.
    amp: float or array-like
        Amplitud of generated wave.  If array-like, length should be equal
        to ammount of frequency values to sweep. Default: 1.
    waveform: str
        Type of waveform to use. Can be 'sine', 'sawtoothup', 'sawtoothdown',
        'ramp', 'triangular', 'square' or 'custom'. Default: sine.
    duration_per_freq: float or array-like
        Duration of each frequency stretch in seconds. If array-like, length 
        should be equal to ammount of frequency values to sweep. 
        Default: 1 second.
    silence_between_freq: float or array-like
        Time to wait between each frequency in seconds. If array-like, length 
        should be equal to ammount of frequency values to sweep. 
        Default: 0 seconds.
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
    Has three atributes: waveform, frequency and amplitude. Waveform can be
    'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 'triangular', 'square' or 
    'custom'. Default: sine.'''
    
    def __init__(self, waveform='sine', frequency=400, amplitude=1):
        self.frequency = frequency
        self.amplitude = amplitude
        self.waveform = given_waveform(waveform)
        
    def evaluate(self, time):
        '''Takes in an array-like object to evaluate the funcion in.'''
        wave = self.waveform(time, self.frequency) * self.amplitude
        return wave
    
#    def generate(self, time, chunk_size):
        
