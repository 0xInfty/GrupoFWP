# -*- coding: utf-8 -*-
""" This module works as a function generator

It includes:
Defined functions for several waveforms incorporating a switcher to make choosing easier.
A class for evaluating the multiple waveforms
A class for calculating fourier partial sums and evaluating it.
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
    #dutycycle not implemented due to bug
    wave = square(2 * np.pi * time * freq)
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
    
    #to be able to handle time vectors and scalars
    if hasattr(time, '__len__'):
        time= np.array(time)
        wave = np.zeros(time.shape)
    else:
        wave = 0
        
    for f, a in zip(freq, amp):
        wave += create_sine(time, f) * a
    #Normalize it:
    wave /= sum(amp) 

    return wave
      
def given_waveform(input_waveform):
    """ Switcher to easily choose waveform.
    
    If the given waveform is not in the list, it raises a ValueError and a list
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

    func = switcher.get(input_waveform, wrong_input_build(list(switcher.keys())))
    return func

def wrong_input_build(input_list):
    def wrong_input(*args):
        msg = 'Given waveform is invalid. Choose from following list:{}'.format(input_list)
        raise ValueError(msg)
    return wrong_input

#%% Clase que genera ondas

class Wave:
    '''Generates an object with a single method: evaluate(time).
  
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
        ''' See class atributes.
        
        If wave is 'custom', the custom function should be passed to *args.
        '''
        
        self._frequency = frequency
        self.amplitude = amplitude
        self.waveform = given_waveform(waveform)
        self.extra_args = args
        
    @property
    def frequency(self):
        '''Frequency getter: returns frequency of wave. 
        
        If frequency is an iterable, as it be in a sum or a 
        custom function, returns first value. Used to have 
        backwards compatibility wen sum and custom were added.'''
        
        if isinstance(self._frequency, (list, tuple, np.ndarray)):
            return self._frequency[0]
        else:
            return self._frequency
        
    @frequency.setter
    def frequency(self, value):
        '''Frequency setter: sets value as self._frequency.'''
        self._frequency = value    
        
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
            wave = self.waveform(time, self._frequency, self.amplitude)
        else:
            wave = self.waveform(time, self._frequency, *args, self.extra_args) * self.amplitude
        return wave


#%% Fourier series classfor wave generator

def fourier_switcher(input_waveform):
    """ Switcher to easily choose waveform.
    
    If the given waveform is not in the list, it raises a ValueError and a list
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
            'square': square_series,
            'triangular': triangular_series,
            'sawtooth': sawtooth_series,
            'custom': custom_series}
    func = switcher.get(input_waveform, wrong_input_build(list(switcher.keys())))
    return func

def square_series(order, freq, *args):
    """ Creates parameters for a square series
    
    If the given waveform is not in the list, it raises a ValueError and a list
    containing the accepted inputs.
    
    Parameters
    ----------
    order : int
        order up to which to calculate fourier partial sum 
    frequency : float
        fundamental frequency of generated fourier wave
   
    Returns
    -------
    amps, freqs
        amplitude and frequency vectors used in calculation of partial sum
    """
    
    amps = [1/n for n in range(1, 2*order+1, 2)]
    freqs = np.arange(1, 2*order+1, 2) * freq
    return amps, freqs
        
def sawtooth_series(order, freq, *args):
    """ Creates parameters for a sawtooth series
    
    If the given waveform is not in the list, it raises a ValueError and a list
    containing the accepted inputs.
    
    Parameters
    ----------
    order : int
        order up to which to calculate fourier partial sum 
    frequency : float
        fundamental frequency of generated fourier wave
   
    Returns
    -------
    amps, freqs
        amplitude and frequency vectors used in calculation of partial sum
    """
    
    amps = [1/n for n in range(1, order+1)]
    freqs = np.arange(1, order+1) * freq
    return amps, freqs
    
def triangular_series(order, freq, *args):
    """ Creates parameters for a triangluar series
    
    If the given waveform is not in the list, it raises a ValueError and a list
    containing the accepted inputs.
    
    Parameters
    ----------
    order : int
        order up to which to calculate fourier partial sum 
    frequency : float
        fundamental frequency of generated fourier wave
   
    Returns
    -------
    amps, freqs
        amplitude and frequency vectors used in calculation of partial sum
    """
    
    amps = [(-1)**((n-1)*.5)/n**2 for n in range(1, 2*order+1, 2)]
    freqs = np.arange(1, 2*order+1, 2) * freq
    return amps, freqs
    
def custom_series(order, freq, amp, *args):
    """ Creates parameters for a custom fourier series
    
    If the given waveform is not in the list, it raises a ValueError and a list
    containing the accepted inputs.
    
    Parameters
    ----------
    order : dummy
        is redefined inside implementatoin. Kept for compatibility.
    frequency : float
        fundamental frequency of generated fourier wave
    amp: tuple
        tuple containing amplitude vectors of cosine and sine terms for the
        custom fourier series
   
    Returns
    -------
    amps, freqs
        amplitude tple (passed directly from input) and frequency vector used
        in calculation of partial sum
    """
    
    order = len(amp[0])
    amps = amp
    freqs = np.arange(1, order+1) * freq
    return amps, freqs
    
class Fourier:
    '''Generates an object with a single method: evaluate(time).
  
    Attributes
    ----------
    waveform : str {'sawtooth',  'triangular', 'square', 'custom'} 
        waveform type.
    wave : Wave object 
        Wave instance containgng a sum object that implements the fourier
        series up to given order.
    custom : bool
        desides wether user has requested custom series or not
        
    Methods
    ----------
    evaluate(time)
        returns evaluated fourier partial sum

    '''
    def __init__(self, waveform='square', frequency=400, order=5, *args):
        """Initializes class instance. 
               
        Parameters
        ----------
        waveform : str {'sawtooth',  'triangular', 'square', 'custom'} (Optional)
            waveform type. Default: 'square'
        frequency : float (Optional)
            fundamental frequency of the constructed wave in Hz. Default: 400
        order : int (optional)
            order of the constructed fourier series, i.e. the series will
            be calculated up to the nth non zero term, with n=order.
        args : tuple (optional)
            if waveform is 'custom', a tuple of length 2, each element 
            containing the amplitudes of the cosine and sine terms, 
            respectively. Order will be ignored and will be assumed to be
            equal to len(amplitudes[0]).
            
        Returns
        -------
        
        Evaluated fourier partial sum 
        """          
        
        self.waveform_maker = fourier_switcher(waveform)
        self._order = order #doesn't call setup_props becaouse there's no frequency defined yet
        self.setup_props(frequency)
        self.extra_args = args
        
        self.custom = waveform=='custom'
    
    
    def setup_props(self, freq):
        '''Sets up frequencyes, amplitudes and wave attributes for given freq.'''
        
        self.amplitudes, self._frequencies =  self.waveform_maker(self.order, freq)
        self.wave = Wave('sum', self._frequencies, self.amplitudes)

        
    @property
    def frequency(self):
        '''Frequency getter: returns fundamental frequency of wave.'''
        
        return self._frequencies[0]
        
    @frequency.setter
    def frequency(self, value):
        '''Frequency setter: calculates the frequency vector for given
        fundamental frequency and order. Redefine Wave accordingly.'''
        
        self.setup_props(value)
        
    @property
    def order(self):
        '''Order getter: returns order of the last nonzero term in partial sum.'''
        
        return self._order
        
    @order.setter
    def order(self, value):
        '''Order setter: Calculates new appropiate frequency and amplitude
        vectors for given order value. Redefine Wave accordingly.'''
        
        self._order = value
        self.setup_props(self.frequency)
        
    def evaluate(self, time):
        """Takes in an array-like object to evaluate the funcion in.
        
        Parameters
        ----------
        time : array
            time vector in which to evaluate the funcion
            
        Returns
        -------
        
        Evaluated waveform 
        """          
        
        if self.custom:
            #missing support for custom phases
            
            #cosine series:
            self.wave.amplitude = self.amplitudes[0]
            wave = self.wave.evaluate(time + np.pi *.5) * .5
            
            #sine series:
            self.wave.amplitude = self.amplitudes[1]
            wave += self.wave.evaluate(time) * .5
            
            return wave
            
        else:
            return self.wave.evaluate(time)