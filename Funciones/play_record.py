# -*- coding: utf-8 -*-
"""
Función Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

from pyaudio import paFloat32 # paInt16

def play_record(
    T = 3, # tiempo en seg de grabación deseado
    fname = 'output',
    #A = 1, # amplitud, range [0,1]
    dT = 1, # duración del buffer
    #n = 200 # cantidad de frames en un buffer = chunk
    dt = 0.005, # duración de cada frame del buffer
    sr = 44000, # sample rate
    ch = 2, # cantidad de canales tanto de input como de output
    ft = paFloat32, # formato de input
    freq = 440,
    form = 'saw', # modo de input "saw" o "sine"
    mode = 'txt',
    savetxt = False,
    showplot = True,
    ):

    import pyaudio
    from numpy import linspace, float32, fromstring, savetxt
    import wave
    import matplotlib.pyplot as plt
   
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
    
    if mode=='sine':
        from numpy import sin, pi
        
        s_0 = sin(2*pi*linspace(0,dT,dt)/dT)
        
    if mode=='freq':
        from numpy import sin, pi, arange
        
        s_0 = sin(2*pi*arange(sr*dT)*freq/sr)
        
    elif mode=='saw':
        from numpy import zeros
        
        s_0 = zeros(n)
        
        s_0[0:n//2+1] = linspace(0,1,n//2+1)
        s_0[n//2:n] = linspace(1,0,n//2+1)[0:n//2]
    
    else:
        return "¡Error! Modo de onda de output no especificada"
    
    s_0 = s_0.astype(float32)
    
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
    data = streamrecord.read(n * (sr/n * T))
    print("* done recording")    

    streamrecord.stop_stream()
    streamplay.stop_stream()
    
    streamrecord.close()
    streamplay.close()

    p.terminate()

    if mode == 'txt':
        s_f.extend(fromstring(data, 'Float32'))
        if savetxt:
            savetxt(str(freq)+'.txt', s_f)
        if showplot:
            plt.figure()
            #plt.plot(samples[2000:3000],'bo')
            plt.plot(s_f[2000:3000],'ro')
            plt.ylabel('señal grabada')
            plt.grid()
            plt.show()
            
    else:
        s_f.append(data)   
        wf = wave.open((fname+'.wav'), 'wb')
        wf.setnchannels(ch)
        wf.setsampwidth(p.get_sample_size(ft))
        wf.setframerate(sr)
        wf.writeframes(b''.join(s_f))
        wf.close()

    return s_0, s_f