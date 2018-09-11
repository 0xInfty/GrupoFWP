# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 18:34:02 2018

@author: mfar
"""
import pyaudio
import numpy as np
import time
import wave
import matplotlib.pyplot as plt



p = pyaudio.PyAudio()

volume = 1     # range [0.0, 1.0]
duration = 4   # in seconds, may be float
f = 440        # sine frequency, Hz, may be float



CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"


# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(RATE*duration)*f/RATE)).astype(np.float32)


def recordsignal(in_data, frame_count, time_info, status):
    outputdata = samples
    return (outputdata, pyaudio.paContinue)


streamplay = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                stream_callback = recordsignal)


# start the stream (4)
streamplay.start_stream()

streamrecord = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
#frames = []
#recording_float=[]
#print("* recording")
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#    data = streamrecord.read(CHUNK)
#    recording_float.extend(np.fromstring(data, 'Float32'))
#    frames.append(data)
#print("* done recording")



frames = []
recording_float=[]
print("* recording")
data = streamrecord.read(CHUNK*(RATE / CHUNK * RECORD_SECONDS))
recording_float.extend(np.fromstring(data, 'Float32'))
frames.append(data)
print("* done recording")





#while streamplay.is_active():
#   time.sleep(0.1)
   
streamrecord.stop_stream()
streamrecord.close()

# wait for stream to finish (5)


streamplay.stop_stream()
streamplay.close()

    
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()



#graficar pa ver que sale
plt.figure()
#plt.plot(samples[2000:3000],'bo')
plt.plot(recording_float[2000:3000],'ro')
plt.ylabel('señal grabada')
plt.grid()
plt.show()


i=1
np.savetxt('archivo%01d.txt' % i,recording_float)


#usando la funcion de vale
#for i in range[len(frecuencias)]:
#    play_record(freq=frecuencias [i])
#    np.savetxt('archivo%01d.txt' % i,frames)
