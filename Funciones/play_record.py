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
    #A = 1, # range [0,1]
    T = 1,
    #n = 200
    dt = 0.005,
    m = 3, # cantidad de veces a repetir el buffer
    sr = 44000,
    ch = 2,
    ft = paInt16):

    import pyaudio
    import numpy as np
    import time
    import wave
    
    p = pyaudio.PyAudio()
    
    s_in = []
    
    print("Longitud del buffer: %i" % int(T/dt))
    if int(T/dt) != T/dt:
        print("¡Ojo! El intervalo dt no entra un número entero de veces en T")
        dt = T/int(T/dt)
        print("Intervalo redefinido a %f s" % dt)
    
    n = int(T/dt)
    s_out = np.zeros(n)
    
    s_out[0:n//2+1] = np.linspace(0,1,n//2+1)
    s_out[n//2:n] = np.linspace(1,0,n//2+1)[0:n//2]
    
    s_out = s_out.astype(np.float32)
    
    def callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)
    
    
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=ft,
                    channels=ch,
                    rate=sr,
                    input=True,
                    output=True,
                    input_device_index=1,
                    output_device_index=3,
                    frames_per_buffer=n,
                    stream_callback = callback)
    
    stream.start_stream()
    
    
    # wait for stream to finish (5)
    while stream.is_active()==True:
        time.sleep(0.1)
    
    stream.stop_stream()
    stream.close()
       
    p.terminate()
    
    wf = wave.open((fname+'.wav'), 'wb')
    wf.setnchannels(ch)
    wf.setsampwidth(p.get_sample_size(ft))
    wf.setframerate(sr)
    wf.writeframes(b''.join(s_in))
    wf.close()