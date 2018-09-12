# -*- coding: utf-8 -*-
"""
Script auxiliar módulo PyAudio
@date: 11/09/2018
@author: Vall
"""

import fwp_pyaudio as fwp
import numpy as np

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
