# -*- coding: utf-8 -*-
"""
Función Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

def play_record(
    T, # duración de la grabación
    dt = 0.005, # duración de cada frame del buffer
    form = 'freq', # modo de input "saw" o "sine"
    mode = 'txt',
    savetxt = False,
    showplot = True,
    *kwargs
    ):
    
    """Reproduce una señal de sonido y graba por jack al mismo tiempo.

Crea una señal cuya forma de onda está dada por 'form'. Ésta crea un \
buffer cuyos frames duran 'dt'. Reproduce y graba durante un tiempo \
'T'. Devuelve el array reproducido y la lista grabada. 

Tiene dos modos de funcionamiento dados por 'mode'. Si 'mode=="wav", \
guarda un archivo de audio. Y si 'mode=="txt"', 
Además, si 'savetxt==True', guarda un archivo de texto. Y si \
'showplot=="True", muestra un gráfico.
    
    """

    import pyaudio
    import numpy as np
    import os
    import wave
    import matplotlib.pyplot as plt
    
    import new_name

    home = os.getcwd()
    
    if 'ch' not in globals():
        ch = 1    
    if 'sr' not in globals():
        sr = 44000
    if 'dT' not in globals():
        dT = 1
    if 'dt' not in globals():
        dt = 0.005
    if form=='freq':
        if 'freq' not in globals():
            freq = 440
    if 'fname' not in globals():
        if 'freq' in globals():
            fname = '%i' % int(freq)
        else:
            fname = 'output'
    if 'fdir' not in globals():
        fdir = home
    
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
        
        s_0 = np.sin(2*np.pi*np.linspace(0,n)/n)
        
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
    
    streamplay = p.open(format=pyaudio.paFloat32,
                channels=ch,
                rate=sr,
                output=True,
                stream_callback = callback)

    streamrecord = p.open(format=pyaudio.paFloat32,
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
            savetxt((new_name(fname, 'txt', fdir)+'.txt'), s_f)
            os.chdir(home)
        if showplot:
            plt.figure()
            #plt.plot(samples[2000:3000],'bo')
            plt.plot(s_f[2000:3000],'ro')
            plt.ylabel('señal grabada')
            plt.grid()
            plt.show()
        return s_0, s_f
            
    else:
        s_f.append(data)
        fname = new_name(fname, 'wav', fdir)
        wf = wave.open((fname+'.wav'), 'wb')
        wf.setnchannels(ch)
        wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
        wf.setframerate(sr)
        wf.writeframes(b''.join(s_f))
        wf.close()

    return s_0, s_f