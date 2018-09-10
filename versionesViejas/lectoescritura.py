# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 14:53:10 2018

@author: mfar
"""

import pyaudio
import numpy as np
import matplotlib.pyplot as plt



def decode(in_data, channels):
    import numpy as np

    """
    Convert a byte stream into a 2D numpy array with 
    shape (chunk_size, channels)

    Samples are interleaved, so for a stereo stream with left channel 
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output 
    is ordered as [L0, R0, L1, R1, ...]
    """
    result = np.fromstring(in_data, dtype=np.float32)

    chunk_length = len(result) / channels
    assert chunk_length == int(chunk_length)

    result = np.reshape(result, (int(chunk_length), channels))
    return result


def encode(signal):
    import numpy as np

    """
    Convert a 2D numpy array into a byte stream for PyAudio

    Signal should be a numpy array with shape (chunk_size, channels)
    """
    interleaved = signal.flatten()
    out_data = interleaved.astype(np.float32).tostring()
    return out_data



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


samplesleft =(np.sin(2*np.pi*np.arange(RATE*duration)*(f*3)/RATE)).astype(np.float32) #lo que quiero en el canal de la izquierda
samplesright = (np.sin(2*np.pi*np.arange(RATE*duration)*f/RATE)).astype(np.float32) # lo que quiero en el canal de la derecha
samplestuple = [np.transpose(samplesleft), np.transpose(samplesright)] # me armo una tupla que tenga en cada columna lo que quiero reproducir por cada canal
samplesarray=np.transpose(np.array(samplestuple)) # la paso a array, y la traspongo para que este en el formato correcto de la funcion de encode
samples=encode(samplesarray) #formateo los datos para que puedan ser interpretados por el modulo pyaudio

#me armo el callback que simplemente reproduce la señal
def recordsignal(in_data, frame_count, time_info, status):
    outputdata = samples
    return (outputdata, pyaudio.paContinue)

#me armo el stream de reproduccion con los parametros definidos al principio
streamplay = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                stream_callback = recordsignal)


# Le doy play
streamplay.start_stream()

#me armo el stream de grabacion
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



frames = [] #este va a tener la data tal cual se graba, para despues hacer un wav
recording_float=[] #este me pasa lo grabado a array
print("* recording")
data = streamrecord.read(RATE * RECORD_SECONDS)#grabo todo lo que hay que grabar
recording_float.extend(np.fromstring(data, 'Float32'))#paso a array lo grabado
frames.append(data)
print("* done recording")



#cierro el stream de grabacion y de reproduccion
streamrecord.stop_stream()
streamrecord.close()

streamplay.stop_stream()
streamplay.close()
    
p.terminate()

#paso lo grabado a un array de dos columnas, en cada una de ellas un canal
result= decode(data, 2)


#graficar pa ver que sale
plt.figure()
plt.plot(samplesarray[3000:3100,0]/10,'m-')
plt.plot(samplesarray[3000:3100,1]/10,'k-')
plt.plot(result[3000:3100,0],'r-')
plt.plot(result[3000:3100,1],'b-')
plt.ylabel('señal grabada')
plt.grid()
plt.show()
