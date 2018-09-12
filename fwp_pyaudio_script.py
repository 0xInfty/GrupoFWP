# -*- coding: utf-8 -*-
"""
Script auxiliar módulo PyAudio
@date: 11/09/2018
@author: Vall
"""

import fwp_pyaudio as fwp
import numpy as np
import matplotlib.pyplot as plt
import os

home = os.getcwd()
os.chdir(home + '\Funciones')
from rms import rms
os.chdir(home)
del home

#%% Grabar en nchannelsrec y reproducir en nchannelsplay

duration = 3
nchannelsrec = 1
nchannelsplay = 1

waveform = 'sine'
frequency = 440#[440, 220]

savewav = False
showplot = True
saveplot = False
savetext = False
filename = 'output'

if nchannelsplay > 1:
    signalplay = [fwp.make_signal(waveform, freq, duration) 
                 for freq in frequency]
    signalplay = np.transpose(np.array(signalplay))
else:
    signalplay = fwp.make_signal(waveform, frequency, duration)

signalrec = fwp.play_callback_rec(fwp.encode(signalplay), 
                                  duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec)

if savewav:
    fwp.savewav(signalrec, filename, datanchannels=nchannelsrec)

signalrec = fwp.decode(signalrec, nchannelsrec)

if showplot:
    fwp.signal_plot(signalrec)
    
    if saveplot:
        fwp.saveplot(filename)

if savetext:
    fwp.savetext(signalrec, filename)

#%% Barrido en frecuencias y gráfico de fase

frequency_start = 400
frequency_final = 40000
frequency_interval = 50
waveform = 'sine'
savetext = True
saveplot = True

nchannelsrec = 1
nchannelsplay = 1
samplerate = 44100

frequency = np.arange(frequency_start, frequency_final, 
                      frequency_interval)
duration = np.array([100/freq for freq in frequency])
savedir = os.getcwd() + '\Freq_Sweep'
filenames = ['Freq_Sweep_{}_Hz'.format(freq) for freq in frequency]

for i in range(len(duration)):
    if duration[i] < 0.2:
        duration[i] = 0.2
    
home = os.getcwd()
signalplay = [fwp.make_signal(waveform, freq, dur) 
             for freq, dur in zip(frequency,duration)]

signalrms = []
for si, dur, fnam, i in zip(signalplay, duration,filenames,range(len(frequency))):
    print('Frequency {} of {}'.format(i ,len(frequency)))
    thesignal = fwp.play_callback_rec(fwp.encode(si), 
                                      dur,
                                      nchannelsplay=nchannelsplay,
                                      nchannelsrec=nchannelsrec)
    thesignal = fwp.decode(thesignal, nchannelsrec)
    signalrms.append(rms(thesignal))
    if savetext:
        fwp.savetext(np.transpose([si, thesignal]), 
                     fnam, savedir=savedir)
signalrms = np.array(signalrms)

plt.figure()
plt.plot(frequency, 10*np.log10(signalrms/max(signalrms)), 'b-o')
plt.ylabel('Decibels')
plt.xlabel('Frequency (Hz)')
plt.grid()
plt.show()

if saveplot:
    fwp.saveplot('Plot')
    
#%% Otra opción

"""
frequency_final = 20000
frequency_interval = 100
periods_per_frequency = 50
waveform = 'sine'
savetext = False
saveplot = True
samplerate = 44100
deadpoints = 100

frequency = np.arange(frequency_start, frequency_final, 
                      frequency_interval)
duration = np.array([periods_per_frequency/freq + deadpoints 
                     for freq in frequency]) #in seconds

signals = tuple(np.concatenate(
        (fwp.make_buffer(
                'sine',
                freq,
                m=periods_per_frequency,
                fullbuffer=False),np.zeros(deadpoints)))
        for freq in frequency)
signals = np.concatenate((signals))

nchannelsrec = 1
nchannelsplay = 1
samplerate = 44100
duration = len(signals)/samplerate

signalrec = fwp.play_callback_rec(fwp.encode(signals), duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec)

if savewav:
    fwp.savewav(signalrec, filename, datanchannels=nchannelsrec)

signalrec = fwp.decode(signalrec, nchannelsrec)

if showplot:
    fwp.signal_plot(signalrec)
    
    if saveplot:
        fwp.saveplot(filename)

if savetext:
    fwp.savetext(signalrec, filename)
    
    os.chdir(home)
"""