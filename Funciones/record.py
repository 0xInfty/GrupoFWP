# -*- coding: utf-8 -*-
"""
Record

@author: 0xInfty
"""

def record(fname = "output", \
    T = 10, \
    ch = 2, \
    sr = 44100, \
    chunk = 1024, \
    gdir = r"C:\Users\Usuario\Documents\Git\Público\GrupoFWP"): #¿Qué onda el chunk?

    """Graba un archivo wav de nombre fname.wav en gdir

Variables:
>> fname (str) [nombre del archivo sin formato]
>> T (int, float) [duración de la grabación]
>> ch (int) [número de canales]
>> sr (int) [frecuencia de muestreo]
>> chunk (int) [???]
>> gdir (str) [directorio del archivo a guardar]

"""           
           
    from os import getcwd, makedirs, chdir
    from os.path import isdir, isfile
    from pyaudio import PyAudio, paInt16
    import wave
    
    home = getcwd()
    
    if isdir(gdir) == False:
        makedirs(gdir)
    chdir(gdir)
    
    p = PyAudio()
    
    stream = p.open(format=paInt16,
                    channels=ch,
                    rate=sr,
                    input=True,
                    frames_per_buffer=chunk)
    
    print("* recording")
    
    frames = []
    
    for i in range( 0, int(sr / chunk * T) ):
        data = stream.read(chunk)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    fnameg = fname
    if isfile(fnameg+'.wav') == True:
        fnameg = fnameg + ' (2)'

    wf = wave.open((fnameg+'.wav'), 'wb')
    wf.setnchannels(ch)
    wf.setsampwidth(p.get_sample_size(paInt16))
    wf.setframerate(sr)
    wf.writeframes(b''.join(frames))
    wf.close()
        
    chdir(home)