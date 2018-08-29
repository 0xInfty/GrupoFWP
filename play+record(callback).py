# -*- coding: utf-8 -*-
"""
Play + Record
@date: 29/08/2018
@author: Vall
Basado en....
Created on Tue Aug 28 18:34:02 2018
@author: mfar
"""

import pyaudio
import numpy as np
import time
import wave

p = pyaudio.PyAudio()

A = 1 # range [0,1]
T = 1
dt = 0.005
sr = 44000
ch = 2
ft = pyaudio.paInt16
fname='output'

frames = []

# generate samples, note conversion to float32 array
#samples = (np.sin(2*np.pi*np.arange(RATE*duration)*f/RATE)).astype(np.float32)

n = int(T/dt) + 1
samples = np.zeros(n-1)

samples[0:n//2+1] = np.linspace(0,1,n//2+1)
samples[n//2:n-1] = np.linspace(1,0,n//2+1)[0:n//2]

def recordsignal(in_data, frame_count, time_info, status):
    streamrecord = p.open(format=ft,
        channels=ch,
        rate=sr,
        input=True,
        frames_per_buffer=n)
    
    print("* recording")
    
    for i in range(0, int(sr / n * T)):
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
                stream_callback = recordsignal)


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