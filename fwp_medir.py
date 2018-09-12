# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 12:48:15 2018

@author: Marcos
"""

import fwp_pyaudio as fwp
import wavemaker as wmaker

#%%

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = True,
                                     saveplot = False, savetext = False)                                     
duration = 3
nchannelsrec = 2
nchannelsplay = 2
signal_freq = 500

#A square and a sine wave
seno = wmaker.Wave('sine', frequency=signal_freq)
cuadrada = wmaker.Wave('square',frequency=signal_freq)

signalmaker = fwp.PyAudioWave(nchannels=nchannelsplay)
signal_to_play = signalmaker.write_signal((seno,cuadrada), periods_per_chunk=10)

signalrec = fwp.play_callback_rec(signal_to_play, 
                                  duration,
                                  nchannelsplay=nchannelsplay,
                                  nchannelsrec=nchannelsrec,
                                  after_recording=after_record_do)