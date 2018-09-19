# -*- coding: utf-8 -*-
"""
The 'fwp_pyaudio' module is to play and record using PyAudio.

This module could be divided into several pieces:
    (1) encoding and decoding ('decode', 'encode').
    (2) making streams ('play', 'play_callback', 'play_callback_gen', 
    'rec').
    (3) playing and recording ('play_callback_rec', 
    'play_callback_rec_gen', 'just_play', 'just_rec', 'signal_plot').
    (4) plotting and saving ('signal_plot', 'AfterRecording').

decode: function
    Coverts a PyAudio byte stream into a Numpy array.
encode: function
    Converts a Numpy array into a byte stream for PyAudio.
play: function
    Returns a stream that plays on blocking mode.
play_callback: function
    Takes a signal and returns a stream that plays it on callback.
play_callback_gen: function
    Takes a generator and returns a stream that plays it on callback.
rec: function
	Returns a PyAudio stream that records a signal.
AfterRecording: class
	Has paramaters to decide what actions to take after recording.
play_callback_rec: function
	Plays a signal and records another one at the same time.
play_callback_rec_gen: function
	Plays a signal and records another one at the same time.
just_play: function
	Plays a signal.
just_rec: function
	Records a signal.
signal_plot: function
	Takes an audio signal and plots it as a function of time.

@date: 05/09/2018
@author: Vall + Marcos
"""

import fwp_save as sav
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import os

#%%

def decode(in_data, channels):
    
    """Coverts a PyAudio byte stream into a Numpy array.
    
    This function converts a byte stream into a Numpy array. If 
    channels=1, it makes a 1D Numpy array. Otherwise, it returns a 2D 
    Numpy array with shape (chunk_size, channels). 
    
    Samples are interleaved, so for a stereo stream with left channel 
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the 
    output is ordered as [L0, R0, L1, R1, ...].
    
    Variables
    ---------
    in_data: PyAudio byte array
        The data to be converted
    channels: int
        The number of channels the audio has.
    
    Returns
    -------
    result: Numpy array
        The converted data.
        
    """
    
    result = np.fromstring(in_data, dtype=np.float32)

    chunk_length = len(result) / channels
    assert chunk_length == int(chunk_length)

    if channels>1:
        result = np.reshape(result, (int(chunk_length), channels))
        
    return result

#%%

def encode(signal):

    """Converts a Numpy array into a byte stream for PyAudio.

    Signal can be a 1D Numpy array if it has 1 channel. And it should be
    a 2D Numpy array with shape (chunk_size, channels) if it has more 
    than 1 channel.
    
    Variables
    ---------
    signal: Numpy array
        The data to be converted
    
    Returns
    -------
    out_data: PyAudio byte stream
        The converted data.
    
    """
    
    #If array was Nx1, reshape it to N/2x2
    try:
        len(signal[:,0])
    except IndexError:
        signal = np.reshape(signal, (-1,2))
    
    interleaved = signal.flatten()

    out_data = interleaved.astype(np.float32).tostring()
    return out_data

#%%

def play(nchannelsplay=1, 
         formatplay=pyaudio.paFloat32,
         samplerate=44100):
    
    """Returns a stream that plays on blocking mode.
    
    This function returns a PyAudio stream that plays in blocking mode.
    
    Variables
    ---------
    signalplay: array
        Signal to be played.
    nchannelsplay: int
        Number of channels it should be played at.
    formatplay: PyAudio format.
        Signal's format.
    samplerate=44100: int, float
        Sampling rate at which the signal should be played.
    
    Returns
    -------
    streamplay: PyAudio stream object
        Object to be called to play the signal.
    
    """
   
    p = pyaudio.PyAudio()
    
    streamplay = p.open(format=formatplay,
                        channels=nchannelsplay,
                        rate=samplerate,
                        output=True)
    
    return streamplay

    
#%%

def play_callback(signalplay,
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32,
                  samplerate=44100, 
                  repeat=True):
    
    """Takes a signal and returns a stream that plays it on callback.
    
    This function takes a signal and returns a PyAudio stream that plays 
    it in non-blocking mode.
    
    Variables
    ---------
    signalplay: array
        Signal to be played.
    nchannelsplay: int
        Number of channels it should be played at.
    formatplay: PyAudio format.
        Signal's format.
    samplerate=44100: int, float
        Sampling rate at which the signal should be played.
    
    Returns
    -------
    streamplay: PyAudio stream object
        Object to be called to play the signal.
    
    """
   
    p = pyaudio.PyAudio()
    
    def callback(in_data, frame_count, time_info, status):
         return (signalplay, pyaudio.paContinue)
            

            
    streamplay = p.open(format=formatplay,
                        channels=nchannelsplay,
                        rate=samplerate,
                        output=True,
                        stream_callback=callback)
                        
    return streamplay

#%%

def play_callback_gen(signalplaygen,
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32,
                  samplerate=44100, 
                  repeat=False):
    
    """Takes a generator and returns a stream that plays it on callback.
    
    This function takes a signal and returns a PyAudio stream that plays 
    it in non-blocking mode.
    
    Variables
    ---------
    signalplay: array
        Signal to be played.
    nchannelsplay: int
        Number of channels it should be played at.
    formatplay: PyAudio format.
        Signal's format.
    samplerate=44100: int, float
        Sampling rate at which the signal should be played.
    
    Returns
    -------
    streamplay: PyAudio stream object
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
            signalplay = next(signalplaygen) 
            return (signalplay, pyaudio.paContinue)
            
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
    
    Variables
    ---------
    nchannels=1: int
        Number of channels the signal should be recorded at.
    formatrec=pyaudio.paFloat32: PyAudio format
        Format the signal should be recorded with.
    samplerate=44100: int, float
        Sampling rate at which the signal should be recorded.
    
    Returns
    -------
    streamrec: PyAudio stream object
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
    
    '''Has paramaters to decide what actions to take after recording.'''
    
    def __init__(self, savewav=False, showplot=True, 
                 saveplot=False, savetext=False, 
                 filename=os.path.join(os.getcwd(),'Output')):
        
        self.savewav=savewav
        self.showplot=showplot
        self.saveplot=saveplot
        self.savetext=savetext
        self.filename=filename

    def act(self, signalrec, nchannelsrec, samplerate, filename=None):
        
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

def play_callback_rec(signalplay, #1st column left
                      recording_duration=None,
                      nchannelsplay=1,
                      nchannelsrec=1,
                      samplerate=44100,
                      after_recording=None):
    
    """Plays a signal and records another one at the same time.
    
    This function plays an audio signal with a certain number of 
    channels. At the same time, it records another signal with a given 
    number of channels. It runs for a given time. And it plays and 
    records using the same sampling rate and the same pyaudio.paFloat32 
    format.
    
    Variables
    ---------
    stramplay: PyAudio stream
        The signal to be played.
    signalrecduration: int, float.
        Signals' duration in seconds.
    nchannelsplay: int
        Played signal's number of channels.
    nchannelsrec: int
        Recorded signal's number of channels.
    samplerate: int, float
        Signals' sampling rate.
    
    Returns
    -------
    signalrec: PyAudio byte stream
        Recorded signal.
    
    """
    
    if recording_duration is None:
        recording_duration = len(signalplay)/samplerate
        
    streamplay = play_callback(signalplay,
                               nchannelsplay=nchannelsplay,
                               formatplay=pyaudio.paFloat32,
                               samplerate=samplerate)
    
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
    
    return signalrec

#%%

def play_callback_rec_gen(signalplay_gen, #1st column left
                      recording_duration=None,
                      nchannelsplay=1,
                      nchannelsrec=1,
                      samplerate=44100,
                      after_recording=None):
    
    """Plays a signal and records another one at the same time.
    
    This function plays an audio signal with a certain number of 
    channels. At the same time, it records another signal with a given 
    number of channels. It runs for a given time. And it plays and 
    records using the same sampling rate and the same pyaudio.paFloat32 
    format.
    
    Variables
    ---------
    stramplay: PyAudio stream
        The signal to be played.
    signalrecduration: int, float.
        Signals' duration in seconds.
    nchannelsplay: int
        Played signal's number of channels.
    nchannelsrec: int
        Recorded signal's number of channels.
    samplerate: int, float
        Signals' sampling rate.
    
    Returns
    -------
    signalrec: PyAudio byte stream
        Recorded signal.
    
    """
    if recording_duration is None:
        if not signalplay_gen.duration is None:
            recording_duration = signalplay_gen.duration
        else:
            raise TypeError('Duration not defined. Either generator or recording duration must be specified.')
                
        
    streamplay = play_callback_gen(signalplay_gen,
                               nchannelsplay=nchannelsplay,
                               formatplay=pyaudio.paFloat32,
                               samplerate=samplerate)
    
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
    
    return signalrec

#%%

def just_play(signalplay, #1st column left
              nchannelsplay=1,
              samplerate=44100):
    
    """Plays a signal.
    
    This function plays an audio signal with a certain number of 
    channels and a certain sampling rate, with pyaudio.paFloat32 format.
    
    Variables
    ---------
    signalplay: PyAudio stream
        The signal to be played.
    nchannelsplay: int
        Played signal's number of channels.
    samplerate: int, float
        Signals' sampling rate.
    
    Returns
    -------
    nothing
    
    """
        
    streamplay = play(nchannelsplay=nchannelsplay,
                      formatplay=pyaudio.paFloat32,
                      samplerate=samplerate)
    
    print("* Playing")
    streamplay.write(signalplay)
    
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
    
    Variables
    ---------
    duration: int, float
        Duration of the recording, in seconds.
    nchannelsrec: int
        Recorded signal's number of channels.
    samplerate: int, float
        Signals' sampling rate.
    
    Returns
    -------
    signalrec: PyAudio byte stream
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
    
    Variables
    ---------
    signal: array, list
        Signal to be plotted (could have more than 1 column).
    samplerate=44100: int, float
        Signal's sampling rate.
    plotunits=None: None or string
        Signal's units as they would appear in Y-axis.
    plotlegend=None: None or list of strings.
        Signals' channels' names if there's more than one channel.
    
    Returns
    -------
    nothing        
    
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
