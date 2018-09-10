# -*- coding: utf-8 -*-
"""
Función Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

import pyaudio
import os
import numpy as np
import wave

#%%

def savetext(datanumpylike,
             filename,
             savedir=os.getcwd(),
             overwrite=False):
    
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

def decode(in_data, channels):

    """
    Convert a byte stream into a 2D numpy array with 
    shape (chunk_size, channels)

    Samples are interleaved, so for a stereo stream with left channel 
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output 
    is ordered as [L0, R0, L1, R1, ...]
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

    """
    Convert a 2D numpy array into a byte stream for PyAudio

    Signal should be a numpy array with shape (chunk_size, channels)
    """
    interleaved = signal.flatten()

    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    out_data = interleaved.astype(np.float32).tostring()
    return out_data

#%%

def play_callback(signalplay, 
                  samplerate=44000, 
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32):
   
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

def rec(samplerate=44000,
        nchannelsrec=1,
        formatrec=pyaudio.paFloat32):
    
    p = pyaudio.PyAudio()

    streamrec = p.open(format=formatrec,
                       channels=nchannelsrec,
                       rate=samplerate,
                       input=True)
    
    return streamrec
    
#%%

def savewav(datapyaudio,
            filename,
            datasamplerate=44000,
            datanchannels=1,
            dataformat=pyaudio.paFloat32,
            savedir=os.getcwd(),
            overwrite=False):
    
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
    wf.setframerate(datasamplerate)
    wf.writeframes(b''.join(datalist))
    
    wf.close()

    os.chdir(home)
    
    print('Archivo {}.wav guardado'.format(filename))
    
    return

#%%

def play_callback_rec(signalplay,
                      signalrecduration,
                      samplerate=44000,
                      nchannelsplay=1,
                      nchannelsrec=1):
    
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
    
    return signalrec
    
    #%%

def two_channel_play_callback_rec(signalplayleft, signalplayright,
                      signalrecduration,
                      samplerate=44000,
                      nchannelsplay=2,
                      nchannelsrec=2):
    samplestuple = [np.transpose(signalplayleft), np.transpose(signalplayright)] # me armo una tupla que tenga en cada columna lo que quiero reproducir por cada canal
    samplesarray=np.transpose(np.array(samplestuple)) # la paso a array, y la traspongo para que este en el formato correcto de la funcion de encode
    signalplay=encode(samplesarray)
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
    
