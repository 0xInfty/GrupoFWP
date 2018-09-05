# -*- coding: utf-8 -*-
"""
Función Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

import os
from pyaudio import paInt16, paFloat32

def play_record(
    T, # duración en seg de la grabación
    form = 'freq',
    mode = 'txt',
    savetxt = True,
    showplot = True,
    dT = 1, # duración en seg del buffer
    dt = 0.005, # duración en seg de un frame del buffer
    #n = 200 # cantidad de frames en un buffer = chunk
    freq = 440, # frecuencia del modo 'freq'
    sr = 44000, # sample rate
    ch = 2, # cantidad de canales tanto de input como de output
    ft = paInt16, # formato de input
    fname = 'output',
    fdir = os.getcwd()
    ): 

    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import wave
    
    home = os.getcwd()
    
    if mode != 'txt':
        print("Modo: 'wav'")
    else:
        print("Modo: 'txt'")
        print("Guardar txt: %s" % savetxt)
        print("Mostrar gráfico: %s" % showplot)
    
    print("Longitud del buffer: %i" % int(dT/dt))
    if int(dT/dt) != dT/dt:
        print("¡Ojo! El intervalo dt no entra un número entero \
        de veces en dT")
        dt = dT/int(dT/dt)
        print("Intervalo redefinido a %f s" % dt)
        
    if int(T/dT) != T/dT:
        print("¡Ojo! El tiempo de grabación \
        no es un número entero de veces dT")
        if int(T/dT) != 0:
            T = int(T/dT)*dT
        else:
            print("¡Ojo! El tiempo de grabación era menor a dT")
            T = dT
        print("Tiempo de grabación redefinido a %f s" % T)
    
    p = pyaudio.PyAudio()
    s_f = []    
    n = int(dT/dt)
    
    if form=='sine':
        
        s_0 = np.sin(2*np.pi*np.linspace(0,dT,dt)/dT)
        
    if form=='freq':
        
        s_0 = np.sin(2*np.pi*np.arange(sr*dT)*freq/sr)
        
    elif form=='saw':
        
        s_0 = np.zeros(n)
        
        s_0[0:n//2+1] = np.linspace(0,1,n//2+1)
        s_0[n//2:n] = np.linspace(1,0,n//2+1)[0:n//2]
    
    else:
        return "¡Error! Modo de onda de output no especificada"
    
    s_0 = s_0.astype(np.float32)
    
    def callback(in_data, frame_count, time_info, status):
        return (s_0, pyaudio.paContinue)
    
    streamplay = p.open(format=ft,
                channels=ch,
                rate=sr,
                output=True,
                stream_callback = callback)

    streamrecord = p.open(format=ft,
                channels=ch,
                rate=sr,
                input=True,
                frames_per_buffer=n)

    streamplay.start_stream()
    print("* recording")
    streamrecord.start_stream()
    data = streamrecord.read(int(sr * T))
    print("* done recording")

    streamrecord.stop_stream()
    streamplay.stop_stream()
    
    streamrecord.close()
    streamplay.close()
       
    p.terminate()

    if mode == 'txt':
        s_f.extend(np.fromstring(data, 'Float32'))
        if savetxt:
            os.chdir(fdir)
            np.savetxt((fname+'.txt'), s_f)
            os.chdir(home)
        if showplot:
            plt.figure()
            plt.plot(s_f[2000:3000], 'ro-')
            plt.ylabel('señal grabada')
            plt.grid()
            plt.show()
        return s_0, s_f
            
    else:
        s_f.append(data)
        os.chdir(fdir)
        wf = wave.open((fname + '.wav'), 'wb')
        wf.setnchannels(ch)
        wf.setsampwidth(p.get_sample_size(ft))
        wf.setframerate(sr)
        wf.writeframes(b''.join(s_f))
        wf.close()
        os.chdir(home)