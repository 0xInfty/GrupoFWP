# -*- coding: utf-8 -*-
"""
A module containing a main class (Pyauadiowave) that takes in Wave objects from
the wavemaker module and outputs a variety of signals from the given wave(s). It
also contains a helper class (SignalMaker) to pass to fwp_pyaudiowave playback
functions tu properly setup parameters.
"""

import numpy as np

#%% The class


class PyAudioWave:
    """ A class which takes in a wave object and formats it accordingly to the
    requirements of the pyaudio module for playing. It includes two simple 
    methods that return a signal formated to play or a signal formated to plot,
    respectively.
    
    
    Parameters
    ----------
    Pyaudio parameters required:
    samplingrate : int
        Sampling (or playback) rate.
    buffersize : int
        Writing buffer size
    nchannels : {1, 2}
        Number of channels.


    Attributes
    ----------
    sampling_rate : int or float
        Sampling rate for data adquisition
    buffer_size : int or float
        Buffer size por data adquisition
    nchannels : {1,2}
        number of channels used for recording and playing
    debugmode : bool
        if true, activates prints along the code to find bugs
        
    
    Methods (public)
    -------
        
    write_generator :
        Creates a generator to yield chunks of length buffer_size of the 
        generated wave for a total time equal to duration.
    
    plot_signal :
        Returns time and signal arrays ready to plot. If only one wave is
        given, output will be the same as write_signal, but will also return
        time. If a tuple of waves is given, output will be time and a list of
        the signal arrays.
    """
        
    def __init__(self, samplingrate=44100, buffersize=1024, nchannels=1, debugmode=False):
        
        self.sampling_rate = samplingrate
        self.buffer_size = buffersize
        self.nchannels = nchannels
        self.debugmode = debugmode

    def debugprint(self, printable):
        """
        if true, activates prints along the code to find bugs
        
        Parameters
        ----------
        printable : 
            a printable object to be printed along the code where desired
        
        Returns
        -------
        
            prints printable
        """
        
        if self.debugmode:
            print(printable)
            
#% Some secundary methods

    def create_time(self, wave, periods_per_chunk=1):
        """ Creates a time array for other functions tu use.
        
        Parameters
        ----------
        wave : Wave object
            Object created by wavemaker class with desired function
            
        periods_per_chunk : int or float optional
            Amount of periods to be sent to audio output. Default= 1.
            
        Returns
        -------
        numpy array
            Time array
        """
        
        period = 1/wave.frequency
        time = np.linspace(start = 0, stop = period * periods_per_chunk, 
                           num = period * periods_per_chunk * self.sampling_rate,
                           endpoint = False)
        return time
    
    
    def encode(self,signal):
        """
        Formats desired signal for pyaudio stream. Deals with one- and 
        two-channel signals.
        
        Parameters
        ----------
        signal : numpy array
            Signal to be played. Must be numpy array with shape (chunk_size, channels)
            
        Returns
        -------
        str
            Byte stream signal formatted as is needed by pyaudio to play  
        """
        
        if self.nchannels == 2:
            #Two channel signal requires some extra handling
            signal = np.transpose(np.array(signal))
        
        interleaved = signal.flatten()
        out_data = interleaved.astype(np.float32).tostring()
        return out_data
        
    def resolve_nchannels(self, wave, display_warnings):
        """
        Resolve wave or wave tuple for given channel ammount. Return a tuple.
        
        Parameters
        ----------
        wave : wave object
            Object created by wavemaker class with desired function
            
        display_warning : bool
            If True displays warnings regarding number of channels and wave incompatibilities
            
        Returns
        ----------

        tuple
            tuple containing wave object(s)
        """
        
        if self.nchannels == 1:
            #If user passed one wave objects and requested single-channel signal:
            if not isinstance(wave,tuple):
                if display_warnings: print('Requested a one channel signal but provided more than one wave. Will precede using the first wave.')
                return (wave,)
        
        else:
            # Ahora mismo hay un probema de diseño con escrir en dos canales
            # y loopear sobre un únic array, porque lo que se quiere escribir en
            # los dos canales pede no tener frecuencias compatibles y una de
            # ellas queda cortada en cada iteración. Para solucionarlo, habría 
            # que rehacer play_callback para que llame a algo que le de una señal
            # en cada iteración. Por ahora, devuelve los cachos cortados.
            
            #If user passed one wave object, but requested two-channel signal
            if not isinstance(wave,tuple): #should rewrite as warning
                if display_warnings: print('''Requested two channel signal, but only provided one wave object. Will write same signal in both channels.''')
                return (wave,wave)
          
            else: #should rewrite as warning
                if display_warnings: print('''Requested two channel signal. If frequencies are not compatible, second channel wave will be cut off.''')
    
        #If no correction was needed, return as input
        return wave
        
    def eval_wave(self, wave, time):
        """Simple method evaluating the given wave(s) according to channels.
              
        Parameters
        ----------
        wave : wave object
            Object created by wavemaker class with desired function
            
        time : numpy array
            Time in which to evaluate given waveform function
            
        Returns
        ----------
        numpy array
            Evaluated given wave
        """
        
        #Could also be implemented as [wave[i] for i in range(nchannels)]
        if self.nchannels == 1:
            #list is used to have an array of shape (1,N), instad of (N,)
            signal = np.array([np.transpose(wave[0].evaluate(time))])
        else:
            signal = np.array([np.transpose(w.evaluate(time)) for w in wave])
            
        return signal
    
    def yield_a_bit(self, signal):
        """Yield chunck of the given signal of lenght buffer_size. 
       
        Parameters
        ----------         
        signal : numpy array
            Signal to be played. Should be an array of shape (samples, nchannels).
            
        Yields
        ----------
        str
            Byte stream signal formatted as is needed by pyaudio to play 
        
        """
        #Since buffers_per_arrray might be smaller than 
        #len(signal)//self.buffer_size, I'll use the latter:
        self.debugprint('Entered yield_a_bit')
        for i in range(int(signal.shape[1]/self.buffer_size)):
            
#            self.debugprint('Engaged its for loop. Iteration {} of {}'.format(i, int(signal.shape[1]/self.buffer_size)))
            yield self.encode(signal[:,self.buffer_size * i:self.buffer_size * (i+1)])
    
#% The actual useful methods
    
    def write_generator(self, wave, duration=None, buffers_per_array=100, display_warnings=False):
        """Creates a generator to yield chunks of length buffer_size of the 
        generated wave for a total time equal to duration. If duration is
        None, it will generate samples forever.
        
        
        Parameters
        ----------
        wave : wave object
            Object created by wavemaker class with desired function
            
        duration : int or float optional
            Desired time lenght of signal in seconds. Default: none.
            
        buffers_per_array : int optional
            How many buffer sized "blocks" should be fitted in the 
            array. Default: 100.
            
        display_warning : bool
            If True displays warnings regarding number of channels
            and wave incompatibilities. Default= False.
          
            
        Yields
        ----------
        str
            Byte stream signal formatted as is needed by pyaudio to play 
        
        """
        
        wave = self.resolve_nchannels(wave, display_warnings)
        self.debugprint('Wave tuple lentgh: {}'.format(len(wave)))
        
        #Get whole number of periods bigger than given buffer_size
        required_periods = self.buffer_size * wave[0].frequency // self.sampling_rate + 1
        
        #Create a time vector just greater than buffers_per_array*buffer_size
        time = self.create_time(wave[0],
                                periods_per_chunk = required_periods * buffers_per_array)
        self.debugprint('Time length: {}'.format(len(time)))

        signal = self.eval_wave(wave, time)
        self.debugprint('Signal = {}'.format(signal))
        self.debugprint('Signal shape: {}'.format(signal.shape))
#        yield signal
        
        yield_signal = signal
        
        #Handle different duration values:
        
        if duration is None:
            self.debugprint('Mode engaged: Indefinitely')
            # Yield samples indefinitely
            while True:
                
                yield from self.yield_a_bit(yield_signal)
                
                last_place = yield_signal.shape[1]//self.buffer_size
                yield_signal = np.concatenate((yield_signal[:,last_place:],signal), axis=1)
                        
        elif duration < signal.shape[1] / self.sampling_rate:
            self.debugprint('Mode engaged: Short')
            total_length = duration * self.sampling_rate
            yield from self.yield_a_bit(signal[:,:total_length])
            yield self.encode(signal[:,total_length:]) #yield last bit
            
        else: 
            self.debugprint('Mode engaged: Long')
            
            iterations = duration * wave[0].frequency // (required_periods * buffers_per_array)
            self.debugprint('Number of full iterations to run: {}'.format(iterations))
            
            for _ in range(int(iterations)):
                
                yield from self.yield_a_bit(yield_signal)
                
                last_place = int(yield_signal.shape[1]/self.buffer_size)
                self.debugprint(''' Array sizes:
                    yield_signal[:,last_place:]: {}
                    signal: {}'''.format(
                    yield_signal[:,last_place:].shape, signal.shape))
                yield_signal = np.concatenate((yield_signal[:,last_place:],signal), axis=1)
            #Missing line to get exact duration
                
               
    def plot_signal(self, wave, periods_per_chunk=1):
        """ Returns time and signal arrays ready to plot. If only one wave is
        given, output will be the same as write_signal, but will also return
        time. If a tuple of waves is given, output will be time and a list of
        the signal arrays.
        
        
        Parameters
        ----------
        wave : wave object
            Object created by wavemaker class with desired function
            
       periods_per_chunk : int or float optional
            Amount of periods to be sent to audio output. Default: 1.
          
            
        Returns
        ----------
        2D numpy array
            array constituted by time, and signal (evaluated waveform)
        
        """
        
        if not isinstance(wave,tuple):
            time = self.create_time(wave, periods_per_chunk)
            
            return time, wave.evaluate(time)
      
        else: 
            time = self.create_time(wave[0], periods_per_chunk)
            signal_list = [w.evaluate(time) for w in wave]
            
            return time, signal_list

    def generator_setup(self, wave, duration=None, buffers_per_array=100, display_warnings=False):
        si = SignalMaker(wave, duration, self)
        si.generator = self.write_generator( wave, duration, buffers_per_array, display_warnings)
        return si
        
        
class SignalMaker(PyAudioWave):
    '''A secondary class with no methods used to pass a signal generator to the player.'''
    
    def __init__(self, wave, duration, parent):
        self.wave = wave
        self.duration = duration
        self.parent = parent
        
#%% example to try everything out
            
#import wavemaker
##%%
#seno1 = wavemaker.Wave('sine', frequency=4)
#seno2 = wavemaker.Wave('sine', frequency=3, amplitude=1.3)
#triang = wavemaker.Wave('triangular',frequency=3)
#
##Some parameters:
#samplerate = 44100
#buffersize = 1024
#    
## An input maker with given parameters and one channel
#InputMaker = PyAudioWave(samplerate, buffersize, debugmode=True)
#
#
#InputMaker.nchannels = 1
#sound_gen = InputMaker.write_generator((seno1, triang), duration=10, buffers_per_array=20)
#
##%%
#k = 0
#for s in sound_gen:
#    print(k)
#    k +=1
##    if k>20:
##        break
