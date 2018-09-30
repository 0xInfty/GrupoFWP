# -*- coding: utf-8 -*-
"""
The 'fwp_pyaudio' module is for playing and recording via PyAudio.

This script requires that 'pyaudio' be installed within the Python
environment you are running this script in.

This module could be divided into different sections:
    (1) making streams ('play', 'play_callback', 'rec')
    (2) playing and recording ('play_rec', 'just_play', 'just_rec').
    (3) decoding, plotting and saving ('decode', 'signal_plot', 
    'AfterRecording').

It contains the following functions:

decode : 
    Coverts a PyAudio byte stream into a Numpy array.  
play :
    Returns a stream that plays on blocking mode.   
play_callback : 
    Takes a signal generator and returns a stream that plays it on callback.   
rec : 
	Returns a PyAudio stream that records a signal.	
play_rec :  
	Plays a signal and records another one at the same time.	
just_play : 
	Plays a signal.	
just_rec :
	Records a signal.	
signal_plot : 
	Takes an audio signal and plots it as a function of time.

It also includes the following class:

AfterRecording :
	Has paramaters to decide what actions to take after recording.
	
@date: 05/09/2018
@author: Vall
@coauthor: Marcos
"""

import fwp_save as sav
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import os

#%%

def decode(in_data, channels):
    
    """Converts a PyAudio byte stream into a Numpy array.
    
    This function converts a byte stream into a Numpy array. If 
    channels=1, it makes a 1D Numpy array. Otherwise, it returns a 2D 
    Numpy array with shape (chunk_size, channels). 
    
    Samples are interleaved, so for a stereo stream with left channel 
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the 
    output is ordered as [L0, R0, L1, R1, ...].
    
    Parameters
    ---------
    in_data : PyAudio byte array
        The data to be converted	
    channels : int
        The number of channels the audio has.
    
    Returns
    -------
    numpy array
        The converted data.
        
    """
    
    result = np.fromstring(in_data, dtype=np.float32)

    chunk_length = len(result) / channels
    assert chunk_length == int(chunk_length)

    if channels>1:
        result = np.reshape(result, (int(chunk_length), channels))
        
    return result


#%%

def play(nchannelsplay=1, 
         formatplay=pyaudio.paFloat32,
         samplerate=44100):
    
    """Returns a stream that plays on blocking mode.
    
    This function returns a PyAudio stream that plays in blocking mode.
    
    Parameters
    ---------
    nchannelsplay : int optional
        Number of channels it should be played at. Default: 1.	
    formatplay : PyAudio format. 
        Signal's format. Default: paFloat32	
    samplerate : int, float optional
        Sampling rate at which the signal should be played. Default: 44100
    
    Returns
    -------
    PyAudio stream object
        Object to be called to play the signal.
    """
   
    p = pyaudio.PyAudio()
    
    streamplay = p.open(format=formatplay,
                        channels=nchannelsplay,
                        rate=samplerate,
                        output=True)
    
    return streamplay

    
#%%

def play_callback(signalplaygen,
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32,
                  samplerate=44100, 
                  repeat=False):
    
    """Takes a generator and returns a stream that plays it on callback.
    
    This function takes a signal and returns a PyAudio stream that plays 
    it in non-blocking mode.
    
    Parameters
    ---------
    signalplay : array
        Signal to be played.	
    nchannelsplay : int optional
        Number of channels signal should be played at. Default: 1.	
    formatplay : PyAudio format optional
        Signal's format. Default=paFloat32.	
    samplerate : int, float optional
        Sampling rate at which the signal should be played. Default: 44100.	
    repeat=False : bool optional
        Decides wether the callback funtion should repeat the first
        it yields or keep yielding new arrays, if for some reason you
        should want that behaviour. Default: False.
    
    Returns
    -------
    PyAudio stream object
        Object to be called to play the signal.
    
    """
   
    p = pyaudio.PyAudio()
    
    if repeat:
        #retains behaviour of other play_callback_gen function
        signalplay = next(signalplaygen)
        def callback(in_data, frame_count, time_info, status):
             return (signalplay, pyaudio.paContinue)
            
    else: #Still needs checks to see if generator run out
        def callback(in_data, frame_count, time_info, status):
            try:
                signalplay = next(signalplaygen) 
                return (signalplay, pyaudio.paContinue)
                #If generator run out
                
            except StopIteration:
                return (None, pyaudio.paComplete)
                
            
    streamplay = p.open(format=formatplay,
                        channels=nchannelsplay,
                        rate=samplerate,
                        output=True,
                        stream_callback=callback)
    
    return streamplay

#%%

def rec(nchannelsrec=1,
        formatrec=pyaudio.paFloat32,
        samplerate=44100):
    
    """Returns a PyAudio stream that records a signal.
    
    Creates a PyAudio stream that will allow to record a signal on a 
    certain format at a certain sampling rate.
    
    Parameters
    ---------
    nchannels : int optional
        Number of channels the signal should be recorded at.
        Default: 1.	
    formatrec : PyAudio format optional
        Format the signal should be recorded with. 
        Default=paFloat32.	
    samplerate: int, float optional
        Sampling rate at which the signal should be recorded. 
        Default: 44100.
    
    Returns
    -------
    PyAudio stream object
        Object to be called to record a signal.
    
    """
    
    p = pyaudio.PyAudio()

    streamrec = p.open(format=formatrec,
                       channels=nchannelsrec,
                       rate=samplerate,
                       input=True)
    
    return streamrec   

#%%

class AfterRecording:
    """Has paramaters to decide what actions to take after recording.
    
    Attributes
    ----------
    savewav : bool
        If True, the script will save a .wav with recorded signal.    
    showplot : bool
        If True, the script will produce a plot with output + recorded data.	
    saveplot : bool
        If True, the script will save a plot in pdf format of
        the output and recorded data.
    savetext : bool
        If True, the script will save a .txt with recorded signal .
    filename : str
        Name with which to save output files produced by the script.
    
    
    Methods
    ----------
    act
   	 it produces output files according to user preferences
	    determined by boolean values of parameters
    
    """
    
    def __init__(self, savewav=False, showplot=True, 
                 saveplot=False, savetext=False, 
                 filename=os.path.join(os.getcwd(),'Output')):
        
        self.savewav=savewav
        self.showplot=showplot
        self.saveplot=saveplot
        self.savetext=savetext
        self.filename=filename

	
    def act(self, signalrec, nchannelsrec, samplerate, filename=None):
	 
        """Decides what actions to take afeter recording.
         
        It deals with after recording actions according to 
    	 boolean values defined by user.
            
        Parameters
        ----------
        signalrec : array
            time vector in which to evaluate the funcion    
        nchannelsrec : int optional
    	      Number of channels it should be played at.
        samplerate : int, float
            Sampling rate at which the signal should be recorded. 
        filename : str
            Name with which to save output files produced by the script.
        """ 
		
        if filename is None:
            filename = self.filename
        
        if filename is None and any((self.saveplot, 
                                     self.savetext, 
                                     self.savewav)):
            print('filename required.')
            return
        
        if self.savewav:
            sav.savewav(signalrec, (filename+'.wav'),
                        data_nchannels=nchannelsrec,
                        data_samplerate=samplerate)
        
        signalrec = decode(signalrec, nchannelsrec)
        
        if self.showplot:
            signal_plot(signalrec)
            
            if self.saveplot:
                sav.saveplot((filename+'.pdf'))
        
        if self.savetext:
            sav.savetext(signalrec, (filename+'.txt'))


#%%

def play_rec(signal_setup, #1st column left
              recording_duration=None,
              nchannelsrec=1,
              after_recording=None,
              repeat=False):
    
    """Plays a signal and records another one at the same time.
    
    This function plays an audio signal with a certain number of 
    channels. At the same time, it records another signal with a given 
    number of channels. It runs for a given time. And it plays and 
    records using the same sampling rate and the same pyaudio.paFloat32 
    format.
    
    Parameters
    ---------
 	 signal_setup: SignalMaker instance form pyaudiowave module
        An object that includes generator that yields the signal to be 
        played and the playback parameters.
    recording_duration : int, float optional
        Signals' duration in seconds. Default: none.
    nchannelsrec : int optional
        Recorded signal's number of channels. Default: 1.
	 after_recording : AfterRecording class instance
		  paramaters to decide what actions to take after recording. By 
        default, it just plots.
	 repeat : bool optional
		  Decides wether the callback funtion should repeat the first
        array it yields or keep yielding new arrays, if for some
        reason you should want that behaviour. Default: False.
		
    
    Returns
    -------
    PyAudio byte stream
        Recorded signal.
    
    """
	
    if recording_duration is None:
        if signal_setup.duration is None:
            raise ValueError('Duration not defined. Either generator or recording duration must be specified.')
        else:
            recording_duration = signal_setup.duration
        
    samplerate = signal_setup.parent.sampling_rate
    streamplay = play_callback(signal_setup.generator,
                               nchannelsplay=signal_setup.parent.nchannels,
                               formatplay=pyaudio.paFloat32,
                               samplerate=samplerate,
                               repeat=repeat)
    
    streamrec = rec(nchannelsrec=nchannelsrec,
                    formatrec=pyaudio.paFloat32,
                    samplerate=samplerate)
    
    streamplay.start_stream()
    print("* Recording")
    streamrec.start_stream()
    signalrec = streamrec.read(int(samplerate * recording_duration))
    print("* Done recording")

    streamrec.stop_stream()
    streamplay.stop_stream()
    
    streamrec.close()
    streamplay.close()
    
    if after_recording is None:
        after_recording = AfterRecording()
    
    after_recording.act(signalrec, nchannelsrec, samplerate)
    
    return decode(signalrec, channels=nchannelsrec)

#%%

def just_play(signal_setup, exceptions = True):
    
    """Plays a signal.
    
    This function plays an audio signal with a certain number of 
    channels and a certain sampling rate, with pyaudio.paFloat32 format.
    
    Parameters
    ---------
    signal_setup: SignalMaker instance form pyaudiowave module
        An object that includes generator that yields the signal to be 
        played and the playback parameters.
    exceptions : bool (Optional)
        Decides if exceptions should be raised or not when duration is not
        given, to avoid playing forever.
    """
        
    streamplay = play(nchannelsplay=signal_setup.parent.nchannels,
                      formatplay=pyaudio.paFloat32,
                      samplerate=signal_setup.parent.sampling_rate)
    
    if exceptions:
        if signal_setup.duration is None:
            raise ValueError('Duration not given. Would play forever (not good).')
    
    print("* Playing")
    for data in signal_setup.generator:
        streamplay.write(data)
    
    streamplay.stop_stream()
    print("* Done playing")
    streamplay.close()

#%%

def just_rec(recording_duration, #1st column left
             nchannelsrec=1,
             samplerate=44100,
             after_recording=None):
    
    """Records a signal.
    
    This function records an audio signal with a certain number of 
    channels and a certain sampling rate, with pyaudio.paFloat32 format.
    
    Parameters
    ---------
    recording_duration : int, float
        Duration of the recording, in seconds.
    nchannelsrec : int optional
        Recorded signal's number of channels. Default: 1.
    samplerate : int, float optional
        Signals' sampling rate. Default 44100
	 after_recording : AfterRecording class instance
		  paramaters to decide what actions to take after recording. By 
        default, it just plots.
		
    Returns
    -------
    PyAudio byte stream
        Recorded signal.
    
    """

    streamrec = rec(nchannelsrec=nchannelsrec,
                    formatrec=pyaudio.paFloat32,
                    samplerate=samplerate)
    
    print("* Recording")
    streamrec.start_stream()
    signalrec = streamrec.read(int(samplerate * recording_duration))
    print("* Done recording")

    streamrec.stop_stream()
    streamrec.close()
    
    if after_recording is None:
        after_recording = AfterRecording()
    
    after_recording.act(signalrec, nchannelsrec, samplerate)
    
    return signalrec

#%%

def signal_plot(signal, samplerate=44100, 
                plotunits=None, plotlegend=None):
    
    """Takes an audio signal and plots it as a function of time.
    
    It takes an audio signal recorded at a certain samplerate and plots 
    it as a function of time. The signal's units can be specified. The 
    signals' channels' names can also be specified if there's more than 
    one.
    
    Parameters
    ---------
    signal : array, list
        Signal to be plotted (could have more than 1 column).
    samplerate : int, float optional
        Signal's sampling rate. Default: 44100.
    plotunits : None or string optional
        Signal's units as they would appear in Y-axis. Default: none.
    plotlegend : None or list of strings optional
        Signals' channels' names if there's more than one channel. 
		Default: none.
    
    """
    
    try:
        n = len(signal[:,0])
        m = len(signal[0,:])
    except:
        n = len(signal)
        m = 1
    
    time = np.linspace(0, (n-1)/samplerate, n)
    
    plt.figure()
    plt.plot(time, signal)
    plt.grid()
    plt.xlabel('Tiempo (s)')
    if plotunits is not None:
        plt.ylabel('Señal ({})'.format(plotunits))
    else:
        plt.ylabel('Señal')
    if m != 1:
        if plotlegend is not None:
            plt.legend(plotlegend)
        else:
            plt.legend(['Izquierda','Derecha'])
