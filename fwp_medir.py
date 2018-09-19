# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 12:48:15 2018

@author: Marcos
"""


import fwp_pyaudio as fwp
import pyaudiowave as paw
import wavemaker as wmaker
import matplotlib.pyplot as plt
import numpy as np
import os, rms

#%% Read an write in two channels

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = True,
                                     saveplot = False, savetext = False)                                     
duration = 1
nchannelsrec = 2
nchannelsplay = 2
signal_freq = 2000

#A square and a sine wave
seno1 = wmaker.Wave('sine', frequency=signal_freq)
seno2 = wmaker.Wave('sine',frequency=signal_freq*2)
cuadrada = wmaker.Wave('square',frequency=signal_freq)

#Create signal to play
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay)
signal_to_play = signalmaker.write_signal((seno1,cuadrada), periods_per_chunk=100)
#NOTE: to write two different signals in two channels use tuples: (wave1,wave2)

thesignal = fwp.play_callback_rec(signal_to_play, 
                                  duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec,
                                  after_recording=after_record_do)


#%% Read an write in two channels using generators to avoid signal cutoff

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = True,
                                     saveplot = False, savetext = False)                                     
duration = 1
nchannelsrec = 2
nchannelsplay = 2
signal_freq = 2000

#A square and a sine wave
seno1 = wmaker.Wave('sine', frequency=signal_freq)
seno2 = wmaker.Wave('sine',frequency=signal_freq*2)
cuadrada = wmaker.Wave('square',frequency=signal_freq)

#Create signal to play
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay)
signal_to_play = signalmaker.write_signal((seno1,cuadrada), periods_per_chunk=100)
#NOTE: to write two different signals in two channels use tuples: (wave1,wave2)

thesignal = fwp.play_callback_rec_gen(signal_to_play, 
                                  duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec,
                                  after_recording=after_record_do)

#%% Frequency sweep

freq_start = 50
freq_stop = 22000
freq_step = 50

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = False,
                                     saveplot = False, savetext = True) 
nchannelsrec = 1
nchannelsplay = 2 #Cause of cable issues

#Defino la unda cono un seno con la frecuencia defaut porque después la voy a 
#cambiar de todas formas. Amplitud default.
seno = wmaker.Wave('sine')
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay) #Samplingrate dafault

#Frequencies and durations
frequencies = np.arange(freq_start, freq_stop, freq_step)
durations = np.array([100/freq for freq in frequencies]) #100 periodos por frecuencia

#If non existent, create directory to save to
savedir = 'FreqSweep'
if not os.path.isdir(savedir):
    os.mkdir(savedir)
makefile = lambda freq: os.path.join(savedir,'Freq_Sweep_{}_Hz'.format(freq))

signalrms = []

for freq, dur in zip(frequencies, durations):
    
    #Set up stuff for this frequency
    seno.frequency = freq
    signal_to_play = signalmaker.write_signal(seno, periods_per_chunk=10000, 
                                              display_warnings=False)
    after_record_do.filename = makefile(freq)
    
    #play, record and process
    thesignal = fwp.play_callback_rec(signal_to_play, 
                                  recording_duration=dur,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec,
                                  after_recording=after_record_do)
    
    thesignal = fwp.decode(thesignal, nchannelsrec)
    signalrms.append(rms.rms(thesignal))

signalrms = np.array(signalrms)

plt.figure()
plt.plot(frequencies, 10*np.log10(signalrms/max(signalrms)), 'b-')
plt.ylabel('Decibels')
plt.xlabel('Frequency (Hz)')
plt.grid()
plt.show() 

