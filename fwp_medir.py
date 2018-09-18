# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 12:48:15 2018

@author: Marcos
"""


import fwp_pyaudio as fwp
import wavemaker as wmaker
import matplotlib.pyplot as plt
import numpy as np
import os, rms

#%% Read and write in two channels

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
signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay)
signal_to_play = signalmaker.write_signal((seno1,cuadrada), periods_per_chunk=100)
#NOTE: to write two different signals in two channels use tuples: (wave1,wave2)

thesignal = fwp.play_callback_rec(signal_to_play, 
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
signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay) #Samplingrate dafault

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

#%% Calibrate playing

import fwp_pyaudio as fwp
import fwp_lab_instruments as ins
import fwp_save as sav
import matplotlib.pyplot as plt
import numpy as np
import os
import wavemaker as wmaker

amp_start = 1
amp_stop = 0
amp_step = 0.1

freq = 2000
n_per = 50
duration = n_per/freq

port = 'USB0::0x0699::0x0363::C108013::INSTR'

nchannelsplay = 1
samplerate = 44100
folder = 'Cal_Play'
after_record_do = fwp.AfterRecording(savewav = False, showplot = False,
                                     saveplot = False, savetext = True)

osci = ins.Osci(port=port)
seno = wmaker.Wave('sine', frequency=signal_freq)
signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay,
                              samplingrate=samplerate)

savedir = sav.new_dir(folder, os.getcwd())
makefile = lambda amp: os.path.join(savedir, '{}_{:.2f}'.format(folder, amp))

amplitude = np.arange(amp_start, amp_stop, amp_step)
amp_osci = []

signal_to_play = signalmaker.write_signal(seno, periods_per_chunk=100)

for amp in amplitude:
    
    signal_to_play = signalmaker.write_signal(amp*seno, 
                                              periods_per_chunk=10000, 
                                              display_warnings=False)
    after_record_do.filename = makefile(amp)
    
    fwp.just_play(signal_to_play, 
                  nchannelsplay=nchannelsplay,
                  after_recording=after_record_do)
    
    result, units = osci.measure('pk2', 1)
    
    amp_osci.append(result)

amp_osci = np.array(amp_osci)

plt.figure()
plt.plot(amplitude, amp_osci, 'o')
plt.xlabel("Factor de amplitud")
plt.ylabel("Amplitud real ({})".format(units))
plt.grid()
plt.show()

sav.saveplot('{}_Plot'.format(folder), savedir=savedir)
sav.savetext(np.transpose([amplitude, amp_osci]), 
             '{}_Data'.format(folder), savedir=savedir)

#%% Get a diode's IV curve

# PARAMETERS

resistance = 1e3 # ohms

amp = 1 # between 0 and 1
freq = 440 # hertz
n_per = 50
duration = n_per/freq

nchannelsplay = 1
nchannelsrec = 2
samplerate = 44100
folder = 'Diode_IV_Curve'
after_record_do = fwp.AfterRecording(savewav = False, showplot = False,
                                     saveplot = False, savetext = True)

# CODE --> ¡OJO! FALTA CALIBRACIÓN

signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay,
                              samplingrate=samplerate)

seno = wmaker.Wave('sine', frequency=signal_freq)
signal_to_play = signalmaker.write_signal(seno, 
                                          periods_per_chunk=10000, 
                                          display_warnings=False)

savedir = sav.new_dir(folder, os.getcwd())
filename = os.path.join(savedir, 
                        '{}_{:.0f}_Hz_{:.2f}'.format(folder, freq, amp))
after_record_do.filename(filename)

signal_rec = fwp.play_callback_rec(signal_to_play, 
                                   duration,
                                   nchannelsplay=nchannelsplay,
                                   nchannelsrec=nchannelsrec,
                                   after_recording=after_record_do)
chL = signal_rec[0]
chR = signal_rec[1]

V = chR - chL
I = chL/resistance

plt.figure()
plt.plot(V, I)
plt.xlabel("Voltaje V")
plt.ylabel("Corriente I")
plt.grid()

sav.saveplot('{}_Plot_{:.0f}_Hz_{:.2f}'.format(folder, freq, amp),
             savedir = savedir)
sav.savetext(np.transpose(np.array([V, I])),
             '{}_Data_{:.0f}_Hz_{:.2f}'.format(folder, freq, amp),
             savedir = savedir)
