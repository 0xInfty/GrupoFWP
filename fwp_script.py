# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 12:48:15 2018

@author: Marcos
"""

#import fwp_lab_instruments as ins
import fwp_pyaudio as fwp
import fwp_save as sav
import matplotlib.pyplot as plt
import numpy as np
import os, rms
import pyaudiowave as paw
import wavemaker as wmaker

#%% Read an write in two channels using generators to avoid signal cutoff

#Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = True,
                                     saveplot = False, savetext = False)                                     
duration = 5
nchannelsrec = 2
nchannelsplay = 2
signal_freq = 2000

#A square and a sine wave
seno1 = wmaker.Wave('sine', frequency=signal_freq)
seno2 = wmaker.Wave('sine',frequency=signal_freq*2)
cuadrada = wmaker.Wave('square',frequency=signal_freq)

#Create signal to play
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay)
signal_generator = signalmaker.generator_setup((seno1,cuadrada))
#NOTE: to write two different signals in two channels use tuples: (wave1,wave2)

thesignal = fwp.play_rec(signal_generator, 
                          recording_duration=duration,
                          nchannelsrec=nchannelsrec,
                          after_recording=after_record_do)

#%% Example of just_play

duration = 3
nchannelsplay = 2
signal_freq = 400

#A square and a sine wave
seno1 = wmaker.Wave('sine', frequency=signal_freq)
seno2 = wmaker.Wave('sine',frequency=signal_freq*1.5)
suma = wmaker.Wave('sum', frequency = np.array((1, 1.25, 1.5, 2)) * signal_freq)

#Create signal to play
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay)
signal_generator = signalmaker.generator_setup(suma, duration=duration)

fwp.just_play(signal_generator)

#%% Frequency sweep using generators

freq_start = 50
freq_stop = 22000
freq_step = 50

# Some configurations
after_record_do = fwp.AfterRecording(savewav = False, showplot = False,
                                     saveplot = False, savetext = True) 
nchannelsrec = 2
nchannelsplay = 2 # Cause of cable issues
name = 'Freq_Sweep'

seno = wmaker.Wave('sine') # Default frequency and amplitude.
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay) # Default srate

# Frequencies and durations
frequencies = np.arange(freq_start, freq_stop, freq_step)
#durations = np.array([100/freq for freq in frequencies]) # 100 periods
duration = 50/frequencies[0] #play 50 periods of slowest wave
durations = [duration] * len(frequencies)

# If non existent, create directory to save to
savedir = sav.new_dir(os.path.join(os.getcwd(), 'Measurements', name))
filename = os.path.join(savedir, name)
makefile = lambda freq : '{}_{:.0f}_Hz'.format(filename, freq)

signalrms = []

for freq, dur in zip(frequencies, durations):
    
    # Set up stuff for this frequency
    seno.frequency = freq
    signal_to_play = signalmaker.generator_setup(seno)
    after_record_do.filename = makefile(freq)
    
    # Play, record and process
    thesignal = fwp.play_rec(
                        signal_to_play, 
                        recording_duration=dur,
                        nchannelsrec=nchannelsrec,
                        after_recording=after_record_do)
    
    signalrms.append(rms.rms(thesignal))

signalrms = np.array(signalrms)
signaldec = 10*np.log10(signalrms/max(signalrms))

plt.figure()
plt.plot(frequencies, signaldec, 'b-')
plt.ylabel('Decibels')
plt.xlabel('Frequency (Hz)')
plt.grid()
plt.show() 

sav.saveplot('{}_Plot.pdf'.format(filename))
sav.savetext(
        np.transpose(np.array([frequencies, signalrms, signaldec])),
        '{}_Data.txt'.format(filename))

#%% Calibrate playing

amp_start = 1
amp_stop = 0
amp_step = 0.05

freq = 2000
n_per = 50
duration = n_per/freq

port = 'USB0::0x0699::0x0363::C108013::INSTR'

nchannelsplay = 2
samplerate = 44100
name = 'Cal_Play_{:.0f}_Hz'.format(freq)
after_record_do = fwp.AfterRecording(savetext = True)

osci = ins.Osci(port=port)
seno = wmaker.Wave('sine', frequency=signal_freq)
signalmaker = paw.PyAudioWave(nchannels=nchannelsplay,
                              samplingrate=samplerate)

savedir = sav.new_dir(os.path.join(os.getcwd(), 'Measurements', name))
filename = os.path.join(savedir, name)
makefile = lambda amp: '{}_{:.2f}'.format(filename, amp)

amplitude = np.arange(amp_start, amp_stop, amp_step)
amp_osci = []

osci.config_measure('pk2', 1)
osci.config_measure('pk2', 2)

for amp in amplitude:
    
    seno.amplitude = amp #update signals ampitude
    signal_to_play = signalmaker.generator_setup(seno, #play for 1000 periods
                                              duration=1000 / seno.frequency)
    after_record_do.filename = makefile(amp)
    
    fwp.just_play(signal_to_play)
    
    result_left = osci.measure('pk2', 1, reconfig=False)
    result_right = osci.measure('pk2', 2, reconfig=False)
    
    amp_osci.append([result_left, result_right])

amp_osci = np.array(amp_osci)

plt.figure()
plt.plot(amplitude, amp_osci, 'o')
plt.xlabel("Factor de amplitud")
plt.ylabel("Amplitud real (Vpp)")
plt.legend(["Izquierda","Derecha"])
plt.grid()
plt.show()

sav.saveplot('{}_Plot.pdf'.format(filename))
sav.savetext(np.transpose([amplitude, amp_osci]), 
             '{}_Data.txt'.format(filename))

#%% Calibrate recording

amp_stop = 2 # Vpp
amp_step = 0.1
amp_start = amp_step

freq = 2000
n_per = 50
duration = n_per/freq

port = 'USB0::0x0699::0x0363::C108013::INSTR'

nchannelsplay = 2
nchannelsrec = 2
samplerate = 44100
name = 'Cal_Rec_{:.0f}_Hz'.format(freq)
after_record_do = fwp.AfterRecording(savetext = True)

gen = ins.Gem(port=port)
#seno = wmaker.Wave('sine', frequency=signal_freq)
#signalmaker = paw.PyAudioWave(nchannels=nchannelsplay,
#                              samplingrate=samplerate)

savedir = sav.new_dir(os.path.join(os.getcwd(), 'Measurements', name))
filename = os.path.join(savedir, name)
makefile = lambda amp: '{}_{:.2f}'.format(filename, amp)

amplitude = np.arange(amp_start, amp_stop, amp_step)

gen.config_output(output_waveform='sin', 
                  output_frequency=freq, 
                  output_ch=1) # Left
gen.config_output(output_waveform='sin', 
                  output_frequency=freq, 
                  output_ch=2) # Right

amp_rec = []
                  
for amp in amplitude:
    
    after_record_do.filename = makefile(amp)
    
    gen.output(output_frequency=freq, 
               output_amplitude=amp,
               output_ch=1,
               reconfig=True)
    gen.output(output_frequency=freq, 
               output_amplitude=amp,
               output_ch=2,
               reconfig=True)
    
    signal_rec = fwp.just_rec(duration,
                              nchannelsrec=nchannelsrec,
                              after_recording=after_record_do)

    amp_rec.append([max(signal_rec[:,0])-min(signal_rec[:,0]), # Left
                    max(signal_rec[:,1])-min(signal_rec[:,1])]) # Right

amp_rec = np.array(amp_rec)

plt.figure()
plt.plot(amplitude, amp_rec, 'o')
plt.xlabel("Amplitud leída (pp)")
plt.ylabel("Amplitud real (Vpp)")
plt.grid()
plt.legend(["Izquierda","Derecha"])
plt.show()

sav.saveplot('{}_Plot.pdf'.format(filename))
sav.savetext(np.transpose([amplitude, amp_osci]), 
             '{}_Data.txt'.format(filename))

#%% Get a diode's IV curve

# PARAMETERS

resistance = 5.6e3 # ohms

amp = 1 # between 0 and 1
freq = 1000 # hertz
n_per = 200 #number of periods
#duration = n_per/freq
duration = 1 #in seconds

nchannelsplay = 2
nchannelsrec = 2
samplerate = 44100

name = 'Diode_IV_{:.0f}_Hz_{:.2f}'.format(freq, amp)
after_record_do = fwp.AfterRecording(showplot = True, savetext = True)

# CODE --> ¡OJO! FALTA CALIBRACIÓN

signalmaker = paw.PyAudioWave(nchannels=nchannelsplay,
                              samplingrate=samplerate)

seno = wmaker.Wave('ramp', frequency=freq)
signal_to_play = signalmaker.generator_setup(seno)

savedir = sav.new_dir(os.path.join(os.getcwd(), 'Measurements', name))
filename = os.path.join(savedir, name)
after_record_do.filename = filename

signal_rec = fwp.play_rec(signal_to_play, 
                           duration,
                           nchannelsrec=nchannelsrec,
                           after_recording=after_record_do)
chL = signal_rec[:,0]
chR = signal_rec[:,1]

V = chR - chL
I = chR/resistance

if after_record_do.showplot:
    plt.figure()
    plt.plot(V, I, '.')
    plt.xlabel("Voltaje V")
    plt.ylabel("Corriente I")
    plt.grid()
#    
#    sav.saveplot('{}_Plot.pdf'.format(filename))
#    sav.savetext(np.transpose(np.array([V, I])),
#                 '{}_Data.txt'.format(filename))
