# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 14:53:10 2018

@author: mfar
"""

from stereo import encode, decode

import pyaudio
import numpy as np
import matplotlib.pyplot as plt



p = pyaudio.PyAudio()

volume = 1     # range [0.0, 1.0]
duration = 3   # in seconds, may be float
f = 440        # sine frequency, Hz, may be float



CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"


# generate samples, note conversion to float32 array
samplesleft =(np.sin(2*np.pi*np.arange(RATE*duration)*(f*3)/RATE)).astype(np.float32)
samplesright = (np.sin(2*np.pi*np.arange(RATE*duration)*f/RATE)).astype(np.float32)
samplestuple = [np.transpose(samplesleft), np.transpose(samplesright)]
#samplestuple = [samplesleft, samplesright]
samplesarray=np.transpose(np.array(samplestuple))
a=samplesarray.flatten()
samples=encode(samplesarray)
#samples=encode(np.transpose(samplesarray))

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

result= decode(data, 2)


#graficar pa ver que sale
plt.figure()
plt.plot(samplesarray[2000:2100,0]/10,'m-')
plt.plot(samplesarray[2000:2100,1]/10,'k-')
#plt.plot(np.array(recording_float[2000:2100]),'g-')
plt.plot(result[2000:2100,0],'r-')
plt.plot(result[2000:2100,1],'b-')
#plt.plot(samplesright[2000:2100],'m-')
#plt.plot(samplesleft[2000:2100],'k-')
plt.ylabel('señal grabada')
plt.grid()
plt.show()



#usando la funcion de vale
#for i in range[len(frecuencias)]:
#    play_record(freq=frecuencias [i])
#    np.savetxt('archivo%01d.txt' % i,frames)