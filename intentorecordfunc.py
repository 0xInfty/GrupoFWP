# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 19:17:41 2018

@author: mfar
"""
import pyaudio
import time
import numpy as np

volume = 1     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1   # in seconds, may be float
f = 440        # sine frequency, Hz, may be float

wf = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
for i in range(10):
    if stream.is_active()==True:
        time.sleep(0.1)
        i=i+1

# stop stream (6)
stream.stop_stream()
stream.close()


# close PyAudio (7)
p.terminate()