# -*- coding: utf-8 -*-
"""
Función Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

from pyaudio import paInt16

def play_record(fname='output', 
    #A = 1, # amplitud, range [0,1]
    T = 1, # duración del buffer
    #n = 200 # cantidad de frames en un buffer = chunk
    dt = 0.005, # duración de cada frame del buffer
    m = 3, # cantidad de veces a repetir el buffer
    sr = 44000, # sample rate
    ch = 2, # cantidad de canales tanto de input como de output
    ft = paInt16, # formato de input
    frec = 440,
    mode = 'saw', # modo de input "saw" o "sine"
    savewav = True,
    savetext = False,
    returntxt = False): 

    import pyaudio
    from numpy import linspace, float32
    import wave
    
    p = pyaudio.PyAudio()
    
    s_out = []
    
    print("Longitud del buffer: %i" % int(T/dt))
    if int(T/dt) != T/dt:
        print("¡Ojo! El intervalo dt no entra un número entero de veces en T")
        dt = T/int(T/dt)
        print("Intervalo redefinido a %f s" % dt)
    
    n = int(T/dt)
    
    if mode=='sine':
        from numpy import sin, pi
        
        s_in = sin(2*pi*linspace(0,T,dt)/T)
        
    if mode=='frec':
        from numpy import sin, pi, arange
        
        s_in = sin(2*pi*arange(sr*T)*frec/sr)
        
    elif mode=='saw':
        from numpy import zeros
        
        s_in = zeros(n)
        
        s_in[0:n//2+1] = linspace(0,1,n//2+1)
        s_in[n//2:n] = linspace(1,0,n//2+1)[0:n//2]
    
    
    else:
        return "¡Error! Modo de onda de output no especificada"
    
    s_in = s_in.astype(float32)
    
    def callback(in_data, frame_count, time_info, status):
        return (s_in, pyaudio.paContinue)
    
    streamplay = p.open(format=ft,
                channels=ch,
                rate=sr,
                output=True,
                stream_callback = callback)


    streamplay.start_stream()

    streamrecord = p.open(format=ft,
                channels=ch,
                rate=sr,
                input=True,
                frames_per_buffer=n)
    
    print("* recording")
    for i in range(0, int(sr / n * 10 * T)):#m * T)):
        data = streamrecord.read(n)
        s_out.append(data)
    print("* done recording")    
    

    streamrecord.stop_stream()
    streamplay.stop_stream()
    
    streamrecord.close()
    streamplay.close()
       
    p.terminate()
    
    wf = wave.open((fname+'.wav'), 'wb')
    wf.setnchannels(ch)
    wf.setsampwidth(p.get_sample_size(ft))
    wf.setframerate(sr)
    wf.writeframes(b''.join(s_out))
    wf.close()