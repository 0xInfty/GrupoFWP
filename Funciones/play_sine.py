# -*- coding: utf-8 -*-
"""
Play_Sine

@author: 0xInfty
"""

def play_sine(f, A=1, T=10, sr=44100, ch=1):

    """Reproduce un tono de frecuencia f, al que se le pueden elegir volumen, duración y frecuencia de muestreo
    
Variables:
>> f (int, float) [frecuencia del tono en Hertz]
>> A=1 (float) [amplitud del tono en escala normalizada 0<=A<=1]
>> T=10 (int, float) [duración del tono en segundos]
>> sr=441000 (int) [frecuencia de muestreo del tono en Hertz]
>> ch=1 (int) [cantidad de canales]
    
    """
    
    import pyaudio
    from numpy import sin, pi, arange, float32
    
    p = pyaudio.PyAudio()
    
    #volume = 1     # range [0.0, 1.0]
    #fs = 44100       # sampling rate, Hz, must be integer
    #duration = 60.0   # in seconds, may be float
    #f = 440        # sine frequency, Hz, may be float
    
    # generate samples, note conversion to float32 array
    samples = ( sin( 2*pi*arange(sr*T)*f/sr ) ).astype( float32 )
    
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=ch,
                    rate=sr,
                    output=True)
    
    # play. May repeat with different volume values (if done interactively) 
    stream.write(A*samples)
    
    stream.stop_stream()
    stream.close()
    
    p.terminate()