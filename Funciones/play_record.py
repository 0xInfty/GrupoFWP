# -*- coding: utf-8 -*-
"""
Función Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

def play_record():

    import pyaudio
    import numpy as np
    import time
    import wave
    
    p = pyaudio.PyAudio()
    
    A = 1 # range [0,1]
    T = 1
    #n = 200
    dt = 0.005
    m = 3 # cantidad de veces a repetir el buffer
    sr = 44000
    ch = 2
    ft = pyaudio.paInt16
    fname='output'
    
    frames = []
    
    print("Longitud del buffer: %i" % int(T/dt))
    if int(T/dt) != T/dt:
        print("¡Ojo! El intervalo dt no entra un número entero de veces en T")
        dt = T/int(T/dt)
        print("Intervalo redefinido a %f s" % dt)
    
    n = int(T/dt)
    samples = np.zeros(n)
    
    samples[0:n//2+1] = np.linspace(0,1,n//2+1)
    samples[n//2:n] = np.linspace(1,0,n//2+1)[0:n//2]
    
    samples = samples.astype(np.float32)
    
    def callback(in_data, frame_count, time_info, status):

        streamrecord = p.open(format=ft,
            channels=ch,
            rate=sr,
            input=True,
            frames_per_buffer=n)
        
        print("* recording")
        
        for i in range(0, int(sr / n * m * T)):
            data = streamrecord.read(n)
            frames.append(data)
        print("* done recording")
           
        streamrecord.stop_stream()
        streamrecord.close()
        outputdata = samples

        return (outputdata, pyaudio.paContinue)
    
    
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    streamplay = p.open(format=ft,
                    channels=ch,
                    rate=sr,
                    output=True,
                    stream_callback = callback)
    
    
    # play. May repeat with different volume values (if done interactively) 
    # start the stream (4)
    streamplay.start_stream()
    
    
    # wait for stream to finish (5)
    for i in range(10):
        if streamplay.is_active()==True:
            time.sleep(0.1)
            i=i+1
    
    streamplay.stop_stream()
    streamplay.close()
       
    p.terminate()
    
    wf = wave.open((fname+'.wav'), 'wb')
    wf.setnchannels(ch)
    wf.setsampwidth(p.get_sample_size(ft))
    wf.setframerate(sr)
    wf.writeframes(b''.join(frames))
    wf.close()