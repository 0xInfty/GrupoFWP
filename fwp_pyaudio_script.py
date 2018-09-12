# -*- coding: utf-8 -*-
"""
Script auxiliar módulo PyAudio
@date: 11/09/2018
@author: Vall
"""

import fwp_pyaudio as fwp

#%% Grabar y reproducir en un sólo canal

duration = 3
nchannelsrec = 1

waveform = 'sine'
frequency = 440

saveplot = False
savetext = False
savewav = False
filename = 'output'

signalplay = fwp.make_signal(waveform, frequency, duration)

signalrec = fwp.play_callback_rec(signalplay, duration, 
                                  nchannelsrec=nchannelsrec)

signalrec = fwp.decode(signalrec, nchannelsrec)

fwp.signal_plot(signalrec)

if saveplot:
    fwp.saveplot(filename)

if savetext:
    fwp.savetext(filename)

if savewav:
    fwp.savewav(filename)