# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 01:09:34 2018

@author: Marcos
"""

import wavemaker
import matplotlib.pyplot as plt
import numpy as np

#%% Create some waves and plot them.

#Create three wave objects: two different sines and a tirangular wave
seno1 = wavemaker.Wave('sine', frequency=4)
seno2 = wavemaker.Wave('sine', frequency=3, amplitude=1.3)
triang = wavemaker.Wave('triangular',frequency=3)

#Plot them all together
time = np.arange(0,1,.01)
for w in (seno1,seno2,triang):
    plt.plot(time,w.evaluate(time))
    
#%% Formating them to play with pyaudio

#The variblaes named sound_[something] are formated such that they can be input
# into a pyaudio stream to play, assuming correct number of channels.

#Some parameters:
samplerate = 44100
buffersize = 1024
    
# An input maker with given parameters and one channel
InputMaker = wavemaker.PyAudioWave(samplerate, buffersize, nchannels=1)
sound_1ch = InputMaker.write_signal(triang,8) #8 full periods of the wave

#To create a two channel input instead of creating a nwe obect, we can change
# InputMaker's channel atribute:
InputMaker.nchannels = 2
sound_2ch = InputMaker.write_signal(seno1,11) #seno1 in both channels
sound_2ch_2 = InputMaker.write_signal((seno1,seno2),11) #different signals in each channel

#Get plotable stuff
time, sound_2ch_plot = InputMaker.plot_signal((seno1,seno2),11)
for signal in sound_2ch_plot:
    plt.plot(time, signal)

plt.figure()
time, sound_1ch_plot = InputMaker.plot_signal(triang,11)
plt.plot(time, sound_1ch_plot)
    

    
