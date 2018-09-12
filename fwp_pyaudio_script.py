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

home = os.gethome()
os.chdir(home + '\Funciones')
from rms import rms
os.chdir(home)
del home

#%% Grabar en nchannelsrec y reproducir en nchannelsplay

duration = 3
nchannelsrec = 1
nchannelsplay = 2

waveform = 'sine'
frequency = [440, 220]#440

savewav = False
showplot = True
saveplot = False
savetext = False
filename = 'output'

if nchannelsplay > 1:
    signalplay = [fwp.make_signal(waveform, frequency[i], duration) 
                 for i in range(nchannelsplay)]
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

# HOUSTON, TENEMOS UN PROBLEMA: Ese barrido en particular me lleva 178 horas, jajajajaj. Puse 0.2 duración mínima porque ése es el silencio que vi al principio.

frequency_final = 40000
frequency_interval = 50
waveform = 'sine'
savetext = False
saveplot = True

duration = 3
nchannelsrec = 1
nchannelsplay = 1
samplerate = 44100

frequency = np.arange(frequency_interval, frequency_final, 
                      frequency_interval)
duration = np.array([100*samplerate/freq for freq in frequency])
savedir = os.getcwd() + '\Freq_Sweep'
filenames = ['Freq_Sweep_{}_Hz'.format(freq) for freq in frequency]

for i in range(len(duration)):
    if duration[i] < 0.2:
        duration[i] = 0.2

key = bool(input('Beware! This will take at least {:.1f} seconds \
                 ({:.1f} hours). Continue anyways?\n'.format(
                         sum(duration), 
                         sum(duration)/3600)))

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