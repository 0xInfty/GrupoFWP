# -*- coding: utf-8 -*-
"""
Módulo PyAudio
@date: 05/09/2018
@author: Vall
"""

import pyaudio
import os
import numpy as np
import wave
import wavemaker as wmaker

#%%

def decode(in_data, channels):

    """Coverts a PyAudio byte stream into a Numpy array.
    
    This function converts a byte stream into a 2D numpy array with 
    shape (chunk_size, channels). Samples are interleaved, so for a 
    stereo stream with left channel of [L0, L1, L2, ...] and right 
    channel of [R0, R1, R2, ...], the output is ordered as 
    [L0, R0, L1, R1, ...]
    
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
    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    result = np.fromstring(in_data, dtype=np.float32)

    chunk_length = len(result) / channels
    assert chunk_length == int(chunk_length)

    result = np.reshape(result, (chunk_length, channels))
    return result

#%%

def encode(signal):
    import numpy as np

    """Converts a 2D numpy array into a byte stream for PyAudio.

    Signal should be a Numpy array with shape (chunk_size, channels).
    
    Variables
    ---------
    signal: Numpy array
        The data to be converted
    
    Returns
    -------
    out_data: PyAudio byte stream
        The converted data.
    
    """
    interleaved = signal.flatten()

    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    out_data = interleaved.astype(np.float32).tostring()
    return out_data

#%%

def make_buffer(waveform, frequency, amplitude=1,
                framesperbuffer=1024, samplerate=44100):
    """Makes a sort of audio buffer with a given waveform and frequency.
    
    This function returns one or several periods of a wave which 
    waveform is given by the 'waveform' string. The returned signal
    has a frequency given by 'frequency' and is intended to fill a 
    buffer whith 'framesperbuffer' frames, which should be read at a 
    'samplerate' sampling rate.
    
    Variables
    ---------
    waveform: string {'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 
    'triangular', 'square'}
        Signal's waveform.
    frequency: int, float
        Signal's frequency.
    amplitude: int, float {from 0 to 1}
        Signal's amplitude.
    framesperbuffer: int
        Audio buffer's number of frames.
    samplerate: int, float
        Audio sampling rate.
    
    Returns
    -------
    buffer: array
        Audio signal designed to fill an audio buffer.
    
    """
    
    duration = 1/frequency
    
    buffer = wmaker.function_creator(waveform, freq=frequency,
                                    duration=duration,
                                    amp=amplitude,
                                    samplig_freq=samplerate)

    m = 1
    while len(buffer) < framesperbuffer:
        m = m + 1
        buffer = wmaker.function_creator(waveform, freq=frequency,
                                        duration=m*duration,
                                        amp=amplitude,
                                        samplig_freq=samplerate)
        
    if len(buffer) / framesperbuffer == \
          int(len(buffer) / framesperbuffer):
              print("Entra bien en un buffer")
    
    return buffer

#%%

def make_signal(waveform, frequency, signalplayduration, 
               amplitude=1, samplerate=44100):
    """Makes a signal with given waveform, duration and frequency.
    
    This function makes an audio signal whith given waveform, duration, 
    frequency and amplitude, designed to be played at a given sampling 
    rate.
    
    Variables
    ---------
    waveform: string {'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 
    'triangular', 'square'}
        Signal's waveform.
    frequency: int, float
        Signal's frequency.
    signalplayduration: int, float.
        Signal's duration in seconds.
    amplitude=1: int, float {from 0 to 1}
        Signal's amplitude.
    samplerate=44100: int, float
        Signal's sampling rate.
    
    Returns
    -------
    signal: array
        Output signal.    
    
    """
    
    signal = wmaker.function_creator(waveform, freq=frequency, 
                                   duration=signalplayduration,
                                   amp=amplitude, 
                                   samplig_freq=samplerate)
    
    return signal

#%%

def play_callback(signalplay,
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32,
                  samplerate=44100):
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

def play_callback_rec(signalplay,
                      signalrecduration,
                      nchannelsplay=1,
                      nchannelsrec=1,
                      samplerate=44100):
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
    
    streamplay = play_callback(signalplay,
                               nchannelsplay=nchannelsplay,
                               formatplay=pyaudio.paFloat32,
                               rate=samplerate)
    
    streamrec = rec(nchannelsrec=nchannelsrec,
                    formatrec=pyaudio.paFloat32,
                    rate=samplerate)
    
    streamplay.start_stream()
    print("* Recording")
    streamrec.start_stream()
    signalrec = streamrec.read(int(samplerate * signalrecduration))
    print("* Done recording")

    streamrec.stop_stream()
    streamplay.stop_stream()
    
    streamrec.close()
    streamplay.close()
    
    return signalrec

#%%

def two_channel_play_callback_rec(signalplayleft, signalplayright,
                      signalrecduration,
                      samplerate=44000,
                      nchannelsplay=2,
                      nchannelsrec=2):
    
    samples = [np.transpose(signalplayleft), np.transpose(signalplayright)] # me armo una tupla que tenga en cada columna lo que quiero reproducir por cada canal
    samples = np.transpose(np.array(samples)) # la paso a array, y la traspongo para que este en el formato correcto de la funcion de encode
    signalplay = encode(samples)
    
    streamplay = play_callback(signalplay,
                               samplerate=samplerate,
                               nchannelsplay=nchannelsplay,
                               formatplay=pyaudio.paFloat32)
    
    streamrec = rec(samplerate=samplerate,
                    nchannelsrec=nchannelsrec,
                    formatrec=pyaudio.paFloat32)
    
    streamplay.start_stream()
    print("* Recording")
    streamrec.start_stream()
    signalrec = streamrec.read(int(samplerate * signalrecduration))
    print("* Done recording")

    streamrec.stop_stream()
    streamplay.stop_stream()
    
    streamrec.close()
    streamplay.close()
    
    result= decode(signalrec, 2)
    return result

#%%

def savetext(datanumpylike,
             filename,
             savedir=os.getcwd(),
             overwrite=False):
    """Takes some array-like data and saves it on a .txt file.
    
    This function takes some data and saves it on a .txt file on 
    savedir directory. If overwrite=False, it checks whether 
    'filename.txt' exists or not; if it already exists, it saves the 
    data as 'filename (2).txt'. If overwrite=True, it saves the data 
    on 'filename.txt' even if it already exists.
    
    Variables
    ---------
    datanumpylike: array, list
        The data to be saved.
    filename: string
        The name you wish the .txt file to have.
    savedir=os.getcwd: string
        The directory you wish to save the .txt file at.
    overwrite=False: bool
        A parameter which allows or not to overwrite a file.
    
    Return
    ------
    nothing
    
    Yield
    -----
    .txt file
    
    """
    
    home = os.getcwd()
    
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    
    os.chdir(savedir)
    
    if not overwrite:
        while os.path.isfile(filename+'.txt'):
            filename = filename + ' (2)'

    np.savetxt((filename+'.txt'), np.array(datanumpylike), 
               delimiter='\t', newline='\n')

    os.chdir(home)
    
    print('Archivo {}.txt guardado'.format(filename))
    
    return

#%%

def savewav(datapyaudio,
            filename,
            datanchannels=1,
            dataformat=pyaudio.paFloat32,
            samplerate=44100,
            savedir=os.getcwd(),
            overwrite=False):
    """Takes a PyAudio byte stream and saves it on a .wav file.
    
    Takes a PyAudio byte stream and saves it on a .wav file at savedir 
    directory. It specifies some parameters: number of audio channels, 
    format of the audio data, sampling rate of the data. If 
    overwrite=False, it checks whether 'filename.wav' exists or not; if 
    it already exists, then it saves it as 'filename (2).wav'. If 
    overwrite=True, it saves it as 'filename.wav' even if it already 
    exists.
    
    """
    
    home = os.getcwd()
    
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    
    os.chdir(savedir)
    
    if not overwrite:
        while os.path.isfile(filename+'.wav'):
            filename = filename + ' (2)'
    
    datalist = []
    datalist.append(datapyaudio)
    
    os.chdir(savedir)
    
    p = pyaudio.pyAudio()
    wf = wave.open((filename + '.wav'), 'wb')
    
    wf.setnchannels(datanchannels)
    wf.setsampwidth(p.get_sample_size(dataformat))
    wf.setframerate(samplerate)
    wf.writeframes(b''.join(datalist))
    
    wf.close()

    os.chdir(home)
    
    print('Archivo {}.wav guardado'.format(filename))
    
    return
