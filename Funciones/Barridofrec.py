# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:40:46 2018

@author: mfar
"""
import numpy as np
def barrido_en_frecuencias(freq_ini, freq_fin, totalnumber):
    frecuenciasparabarrer=np.linspace(freq_ini, freq_fin, totalnumber)
    from play_record import  play_record
    import matplotlib.pyplot as plt
    rms_frec=np.zeros(len(frecuenciasparabarrer))
    for i in range(len(frecuenciasparabarrer)):
        s_0, recording=play_record(freq=frecuenciasparabarrer[i])
        rms_s0=np.sqrt(np.mean((s_0)**2))
        rms_recording=np.sqrt(np.mean((np.array(recording))**2))
        rms_frec[i]=rms_recording/rms_s0
    plt.figure()
    #plt.plot(samples[2000:3000],'bo')
    plt.plot(frecuenciasparabarrer,10*np.log10(rms_frec),'b-')
    plt.ylabel('bandwith')
    plt.grid()
    plt.show()