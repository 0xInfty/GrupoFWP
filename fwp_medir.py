# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 12:48:15 2018

@author: Marcos
"""


import fwp_pyaudio as fwp
import wavemaker as wmaker
import numpy as np
import os

#%% Read an write in two channels

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = True,
                                     saveplot = False, savetext = False)                                     
duration = 1
nchannelsrec = 1
nchannelsplay = 2
signal_freq = 500

#A square and a sine wave
seno = wmaker.Wave('sine', frequency=signal_freq)
cuadrada = wmaker.Wave('square',frequency=signal_freq)

signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay)
signal_to_play = signalmaker.write_signal((seno, cuadrada), periods_per_chunk=100)

signalrec = fwp.play_callback_rec(signal_to_play, 
                                  duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec,
                                  after_recording=after_record_do)

#%% Frequency sweep

freq_start = 50
freq_stop = 20000
freq_step = 50

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = False,
                                     saveplot = False, savetext = True) 

seno = wmaker.Wave('sine') #Sin frecuencia definida, total la cambio
signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay) #Samplingrate dafault

frequencies = np.arange(freq_start, freq_stop, freq_step)


signal_to_play = signalmaker.write_signal((seno, cuadrada), periods_per_chunk=100)

signalrec = fwp.play_callback_rec(signal_to_play, 
                                  duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec,
                                  after_recording=after_record_do)

duration = 3
nchannelsrec = 1
nchannelsplay = 1
samplerate = 44100

#%%
frequency = np.arange(frequency_interval, frequency_final, 
                      frequency_interval)
duration = np.array([100*samplerate/freq for freq in frequency])
savedir = os.getcwd() + '\Freq_Sweep'
filenames = ['Freq_Sweep_{}_Hz'.format(freq) for freq in frequency]

for i in range(len(duration)):
    if duration[i] < 0.2:
        duration[i] = 0.2

key = input('Beware! This will take at least {:.1f} seconds \
                 ({:.1f} hours). Continue? Y/N\n'.format(
                         sum(duration), 
                         sum(duration)/3600))
                         
key_decode = {'Y':True, 'N':False}
key = key_decode.get(key, True)

signalrms = []

if key:
    
    home = os.getcwd()
    os.chdir(savedir)
    signalplay = [fwp.make_signal(waveform, freq, duration) 
                 for freq in frequency]
    
    signalrms = []
    for i in range(len(frequency)):
        thesignal = fwp.play_callback_rec(fwp.encode(signalplay), 
                                          duration,
                                          nchannelsplay=nchannelsplay,
                                          nchannelsrec=nchannelsrec)
        thesignal = fwp.decode(thesignal, nchannelsrec)
        signalrms.append(rms.rms(thesignal))
        if savetext:
            fwp.savetext(thesignal, filenames[i])
    signalrms = np.array(signalrms)

    plt.figure()
    plt.plot(frequency, 10*np.log10(signalrms/max(signalrms)), 'b-')
    plt.ylabel('Decibels')
    plt.xlabel('Frequency (Hz)')
    plt.grid()
    plt.show()     
    
    if saveplot:
        fwp.saveplot('Plot')
    
    os.chdir(home)

