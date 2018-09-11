# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:40:46 2018

@author: mfar
"""
import numpy as np

def freq_sweep(freq_ini, freq_fin, totalnumber, \
                           savetxt=False):
    
    from play_record import play_record
    from pyaudio import paFloat32
    import matplotlib.pyplot as plt
    import rms as rms
    
    freqs = np.linspace(freq_ini, freq_fin, totalnumber)
    rms_freq = np.zeros(totalnumber)
    
    i = 0
    for freq in freqs:
        s_0, recording = play_record(
                1,
                mode='txt', 
                form='freq',
                savetxt=False,
                showplot=False,
                buffer={'freq': freq},
                audio={'ch_play': 1, 'ch_rec': 1,
                       'ft_play': paFloat32, 'ft_rec': paFloat32}
                )
        rms_s0 = rms(s_0)
        rms_recording = rms(recording)
        rms_freq[i] = rms_recording/rms_s0
        i = i + 1
    
    rms_dec = 10*np.log10(rms_freq)
    
    plt.figure()
    #plt.plot(samples[2000:3000],'bo')
    plt.plot(freqs, rms_dec, 'b-')
    plt.ylabel('bandwith')
    plt.grid()
    plt.show()
    
    if savetxt:
        import os
        from new_name import new_name
        fname = 'barrido_freq'
        fname = new_name(fname, '.txt', os.getcwd())
        np.savetxt(
            (fname+'.txt'),
            np.transpose(np.array([freqs, rms_freq, rms_dec])),
            delimiter='\t',
            newline='\n',
            )
    
    return freqs, rms_freq, rms_dec