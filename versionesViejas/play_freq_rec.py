# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:36:19 2018

@author: Usuario
"""

import fwp_pyaudio as fwp
import matplotlib.pyplot as plt

#%%

T = 1 # duración en seg de la grabación
waveformkey = 'freq' # forma de onda {'freq', 'sin', 'squ', 'tri', 'saw'}
mode = 'txt' # modo de funcionamiento del programa {'txt', 'wav'}
savetxt = False
showplot = True
buffer = {'dT': 1, 'dt': 0.005, 'freq': 440, 'vol': 1}
audio = {'sr': 44000, 'ch_play': 1, 'ch_rec': 2,
        'ft_play': pyaudio.paInt16, 'ft_rec': pyaudio.paInt16}
filendir = {'fname': 'output', 'fdir': os.getcwd()}

#'sine': create_sine,
#'sawtoothup': create_sawtooth_up,
#'sawtoothdown': create_sawtooth_down  ,          
#'ramp': create_sawtooth_up, #redirects to sawtooth
#'triangular': create_triangular,
#'square': create_square,
#'custom': create_custom,

#%%

home = os.getcwd()

#%%

ref = {'dT': 1, 'dt': 0.005, 'freq': 440, 'vol': 1,
       'sr': 44000, 'ch_play': 1, 'ch_rec': 1,
       'ft_play': pyaudio.paInt16, 'ft_rec': pyaudio.paInt16,
       'fname': 'output', 'fdir': os.getcwd()}
bkey = ['dT', 'dt', 'freq', 'vol']
akey = ['sr', 'ch_play', 'ch_rec', 'ft_play', 'ft_rec']
fkey = ['fname', 'fdir']

for key in bkey:    
    if key not in buffer:
        buffer.update({key: ref[key]})
for key in akey:
    if key not in audio:
        audio.update({key: ref[key]})
for key in fkey:
    if key not in filendir:
        filendir.update({key: ref[key]})

bsp = Namespace(**buffer) # buffer space
asp = Namespace(**audio) # audio space
fsp = Namespace(**filendir) # filendir space

#%%
               
if mode != 'txt':
    print("Modo: 'wav'")
else:
    print("Modo: 'txt'")
    print("Guardar txt: %s" % savetxt)
    print("Mostrar gráfico: %s" % showplot)

print("Longitud del buffer: %i" % int(bsp.dT/bsp.dt))
if int(bsp.dT/bsp.dt) != bsp.dT/bsp.dt:
    print("¡Ojo! El intervalo dt no entra un número entero \
    de veces en dT")
    bsp.dt = bsp.dT/int(bsp.dT/bsp.dt)
    print("Intervalo redefinido a %f s" % bsp.dt)
    
if int(T/bsp.dT) != T/bsp.dT:
    print("¡Ojo! El tiempo de grabación \
    no es un número entero de veces dT")
    if int(T/bsp.dT) != 0:
        T = int(T/bsp.dT)*bsp.dT
    else:
        print("¡Ojo! El tiempo de grabación era menor a dT")
        T = bsp.dT
    print("Tiempo de grabación redefinido a %f s" % T)

if asp.ch_play != 1:
    raise ValueError("El código no está preparado para reproducir \
    en 2 canales")

print("Canales para grabar: ch_rec=%i" % asp.ch_rec)

#%%

p = pyaudio.PyAudio()
s_f = []
n = int(bsp.dT/bsp.dt)

if form=='freq':
    s_0 = np.sin(2*np.pi*np.arange(asp.sr*bsp.dT)*bsp.freq/asp.sr)
else:
    s_0 = waveform(form, n)
s_0 = bsp.vol * s_0.astype(np.float32)

def callback(in_data, frame_count, time_info, status):
    return (s_0, pyaudio.paContinue)

streamplay = p.open(format=asp.ft_play,
            channels=asp.ch_play,
            rate=asp.sr,
            output=True,
            stream_callback = callback)

streamrecord = p.open(format=asp.ft_rec,
            channels=asp.ch_rec,
            rate=asp.sr,
            input=True,
            frames_per_buffer=n)

#%%

streamplay.start_stream()
print("* recording")
streamrecord.start_stream()
data = streamrecord.read(int(asp.sr * T))
print("* done recording")

streamrecord.stop_stream()
streamplay.stop_stream()

streamrecord.close()
streamplay.close()
   
p.terminate()

if mode == 'txt':
    # s_f.extend(np.fromstring(data, 'Float32'))
    s_f = decode(s_f, asp.ch_rec)
    if savetxt:
        os.chdir(fsp.fdir)
        savetxt((new_name(fsp.fname, 'txt', fsp.fdir)+'.txt'), s_f)
        os.chdir(home)
    if showplot:
        plt.figure()
        plt.plot(s_f[2000:3000], 'ro-')
        plt.ylabel('señal grabada')
        plt.grid()
        plt.show()
        
else:
    s_f.append(data)
    fsp.fname = new_name(fsp.fname, 'wav', fsp.fdir)
    os.chdir(fsp.fdir)
    wf = wave.open((fsp.fname + '.wav'), 'wb')
    wf.setnchannels(asp.ch_rec)
    wf.setsampwidth(p.get_sample_size(asp.ft_rec))
    wf.setframerate(asp.sr)
    wf.writeframes(b''.join(s_f))
    wf.close()
    os.chdir(home)