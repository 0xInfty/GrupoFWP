# -*- coding: utf-8 -*-
"""
Módulo PyAudio
@date: 05/09/2018
@author: Vall
"""

import pyaudio
import os
import numpy as np
import matplotlib.pyplot as plt
import wave
import wavemaker as wmaker

#%%

def decode(in_data, channels):
    
    """Coverts a PyAudio byte stream into a Numpy array.
    
    This function converts a byte stream into a Numpy array. If 
    channels=1, it makes a 1D Numpy array. Otherwise, it returns a 2D 
    Numpy array with shape (chunk_size, channels). 
    
    Samples are interleaved, so for a stereo stream with left channel 
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the 
    output is ordered as [L0, R0, L1, R1, ...].
    
    Variables
    ---------
    in_data: PyAudio byte array
        The data to be converted
    channels: int
        The number of channels the audio has.
    
    Returns
    -------
    result: Numpy array
        The converted data.
        
    """
    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    result = np.fromstring(in_data, dtype=np.float32)

    chunk_length = len(result) / channels
    assert chunk_length == int(chunk_length)

    if channels>1:
        result = np.reshape(result, (int(chunk_length), channels))
        
    return result

#%%

def encode(signal):
    import numpy as np

    """Converts a Numpy array into a byte stream for PyAudio.

    Signal can be a 1D Numpy array if it has 1 channel. And it should be
    a 2D Numpy array with shape (chunk_size, channels) if it has more 
    than 1 channel.
    
    Variables
    ---------
    signal: Numpy array
        The data to be converted
    
    Returns
    -------
    out_data: PyAudio byte stream
        The converted data.
    
    """
    
    try:
        len(signal[:,0])
    except IndexError:
        signal = np.reshape(signal, (-1,2))
    
    interleaved = signal.flatten()

    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    out_data = interleaved.astype(np.float32).tostring()
    return out_data

#%%

class PyAudioWave:
    ''' A class which takes in a wave object and formats it accordingly to the
    requirements of the pyaudio module for playing. It includes two simple 
    methods that return a signal formated to play or a signal formated to plot,
    respectively.
    
    Pyaudio parameters required:
        samplingrate: (int). Sampling (or playback) rate
        buffersize: (int). Writing buffer size
        nchannels: (1 or 2). Number of channels.'''
        
    def __init__(self, samplingrate=44100, buffersize=1024, nchannels=1):
        
        self.sampling_rate = samplingrate
        self.buffer_size = buffersize
        self.nchannels = nchannels
    
    def create_time(self, wave, periods_per_chunk=1):
        ''' Creates a time arry for other functions tu use.'''
        
        period = 1/wave.frequency
        time = np.linspace(start = 0, stop = period * periods_per_chunk, 
                           num = period * periods_per_chunk * self.sampling_rate,
                           endpoint = False)
        return time
    
        
    def write_signal(self, wave, periods_per_chunk=1, display_warnings=True):
        ''' Creates a signal the pyaudio stream can write (play). If signal is 
        two-channel, output is formated accordingly.'''
    
        if self.nchannels == 1:
            #If user passed two wave objects but requested single-channel signal:
            if isinstance(wave,tuple):
                if display_warnings: print('Requested a one channel signal but provided more than one wave. Will precede using the first wave.')
                wave = wave[0]
                
            time = self.create_time(wave, periods_per_chunk)
            
            return wave.evaluate(time)
    
        else:
            ''' Ahora mismo hay un probema de diseño con escrir en dos canales
            y loopear sobre un únic array, porque lo que se quiere escribir en
            los dos canales pede no tener frecuencias compatibles y una de
            ellas queda cortada en cada iteración. Para solucionarlo, habría 
            que rehacer play_callback para que llame a algo que le de una señal
            en cada iteración. Por ahora, devuelve los cachos cortados.'''
            
            #If user passed one wave object, but requested two-channel signal
            if not isinstance(wave,tuple): #should rewrite as warning
                if display_warnings: print('''Requested two channel signal, but only provided one wave object. Will write same signal in both channels.''')
                wave = (wave,wave)
          
            else: #should rewrite as warning
                if display_warnings: print('''Requested two channel signal. If frequencies are not compatible, second channel wave will be cut off.''')
            
            time = self.create_time(wave[0], periods_per_chunk)

            #me armo una lista que tenga en cada columna lo que quiero reproducir por cada canal
            sampleslist = [np.transpose(wave[0].evaluate(time)),
                           np.transpose(wave[1].evaluate(time))] 
            
            #la paso a array, y la traspongo para que este en el formato correcto de la funcion de encode
            samplesarray=np.transpose(np.array(sampleslist))
            
            return encode(samplesarray)
    
    def write_gen(self, wave, duration=None):
        
        #Get whole number of periods bigger than given buffer_size
        required_periods = self.buffer_size * wave.frequency / self.sampling_rate
        required_periods = int(required_periods) + 1
        
        #Create a time vector just greater than scale_factor*buffer_size
        scale_factor = 50
        time = self.create_time(wave, required_periods * scale_factor)
        signal = wave.evaluate(time)
        yield_signal = signal
        
        #OJO si duración es muy corto no hay que hacer todo esto
        for _ in range(duration * wave.frequency // (required_periods * scale_factor)):
            for i in range(scale_factor): #pensar si len(signal)//buffer_size anda
                yield yield_signal[self.buffer_size * i:self.buffer_size * (i+1)]
                
            yield_signal = np.append((yield_signal[self.buffer_size:],signal))
                
               
    def plot_signal(self, wave, periods_per_chunk=1):
        ''' Returns time and signal arrays ready to plot. If only one wave is
        given, output will be the same as write_signal, but will also return
        time. If a tuple of waves is given, output will be time and a list of
        the signal arrays.'''
        

        if not isinstance(wave,tuple):
            time = self.create_time(wave, periods_per_chunk)
            
            return time, wave.evaluate(time)
      
        else: 
            time = self.create_time(wave[0],periods_per_chunk)
            signal_list = [w.evaluate(time) for w in wave]
            
            return time, signal_list
        
        
#%%

def make_buffer(waveform, frequency, amplitude=1,
                framesperbuffer=1024, samplerate=44100):
    
    """Makes a sort of audio buffer with a given waveform and frequency.
    
    This function returns one or several periods of a wave which 
    waveform is given by the 'waveform' string. The returned signal
    has a frequency given by 'frequency' and is intended to fill a 
    buffer whith 'framesperbuffer' frames, which should be read at a 
    'samplerate' sampling rate.
    
    Variables
    ---------
    waveform: string {'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 
    'triangular', 'square'}
        Signal's waveform.
    frequency: int, float
        Signal's frequency.
    amplitude: int, float {between 0 and 1}
        Signal's amplitude.
    framesperbuffer: int
        Audio buffer's number of frames.
    samplerate: int, float
        Audio sampling rate.
    
    Returns
    -------
    buffer: array
        Audio signal designed to fill an audio buffer.
    
    """
    
    duration = 1/frequency
    
    buffer = wmaker.function_creator(waveform, freq=frequency,
                                    duration=duration,
                                    amp=amplitude,
                                    samplig_freq=samplerate)

    m = 1
    while len(buffer) < framesperbuffer:
        m = m + 1
        buffer = wmaker.function_creator(waveform, freq=frequency,
                                        duration=m*duration,
                                        amp=amplitude,
                                        samplig_freq=samplerate)
        
    if len(buffer) / framesperbuffer == \
          int(len(buffer) / framesperbuffer):
              print("Entra bien en un buffer")
    
    return buffer

#%%

def make_signal(waveform, frequency, signalplayduration, 
               amplitude=1, samplerate=44100):
    
    """Makes a signal with given waveform, duration and frequency.
    
    This function makes an audio signal whith given waveform, duration, 
    frequency and amplitude, designed to be played at a given sampling 
    rate.
    
    Variables
    ---------
    waveform: string {'sine', 'sawtoothup', 'sawtoothdown', 'ramp', 
    'triangular', 'square'}
        Signal's waveform.
    frequency: int, float
        Signal's frequency.
    signalplayduration: int, float.
        Signal's duration in seconds.
    amplitude=1: int, float {from 0 to 1}
        Signal's amplitude.
    samplerate=44100: int, float
        Signal's sampling rate.
    
    Returns
    -------
    signal: array
        Output signal.    
    
    """
    
    signal = wmaker.function_creator(waveform, freq=frequency, 
                                   duration=signalplayduration,
                                   amp=amplitude, 
                                   samplig_freq=samplerate)
    
    return signal
#%%
    

def play_callback(signalplay,
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32,
                  samplerate=44100, 
                  repeat=True):
    
    """Takes a signal generator and returns a stream that plays it on callback.
    
    This function takes a signal and returns a PyAudio stream that plays 
    it in non-blocking mode.
    
    Variables
    ---------
    signalplay: array
        Signal to be played.
    nchannelsplay: int
        Number of channels it should be played at.
    formatplay: PyAudio format.
        Signal's format.
    samplerate=44100: int, float
        Sampling rate at which the signal should be played.
    
    Returns
    -------
    streamplay: PyAudio stream object
        Object to be called to play the signal.
    
    """
   
    p = pyaudio.PyAudio()
    
    def callback(in_data, frame_count, time_info, status):
         return (signalplay, pyaudio.paContinue)
            

            
    streamplay = p.open(format=formatplay,
                        channels=nchannelsplay,
                        rate=samplerate,
                        output=True,
                        stream_callback=callback)
                        
    return streamplay

#%%

def play_callback_gen(signalplaygen,
                  nchannelsplay=1, 
                  formatplay=pyaudio.paFloat32,
                  samplerate=44100, 
                  repeat=True):
    
    """Takes a signal generator and returns a stream that plays it on callback.
    
    This function takes a signal and returns a PyAudio stream that plays 
    it in non-blocking mode.
    
    Variables
    ---------
    signalplay: array
        Signal to be played.
    nchannelsplay: int
        Number of channels it should be played at.
    formatplay: PyAudio format.
        Signal's format.
    samplerate=44100: int, float
        Sampling rate at which the signal should be played.
    
    Returns
    -------
    streamplay: PyAudio stream object
        Object to be called to play the signal.
    
    """
   
    p = pyaudio.PyAudio()
    
    if repeat:
        signalplay = next(signalplaygen)
        def callback(in_data, frame_count, time_info, status):
             return (signalplay, pyaudio.paContinue)
            
    else: #Still needs checks to see if generator run out
        def callback(in_data, frame_count, time_info, status):
            signalplay = next(signalplaygen) 
            return (signalplay, pyaudio.paContinue)
            
    streamplay = p.open(format=formatplay,
                        channels=nchannelsplay,
                        rate=samplerate,
                        output=True,
                        stream_callback=callback)
    
    return streamplay

#%%

def rec(nchannelsrec=1,
        formatrec=pyaudio.paFloat32,
        samplerate=44100):
    
    """Returns a PyAudio stream that records a signal.
    
    Creates a PyAudio stream that will allow to record a signal on a 
    certain format at a certain sampling rate.
    
    Variables
    ---------
    nchannels=1: int
        Number of channels the signal should be recorded at.
    formatrec=pyaudio.paFloat32: PyAudio format
        Format the signal should be recorded with.
    samplerate=44100: int, float
        Sampling rate at which the signal should be recorded.
    
    Returns
    -------
    streamrec: PyAudio stream object
        Object to be called to record a signal.
    
    """
    
    p = pyaudio.PyAudio()

    streamrec = p.open(format=formatrec,
                       channels=nchannelsrec,
                       rate=samplerate,
                       input=True)
    
    return streamrec   

#%%

class AfterRecording:
    '''Very simple class containing paramaters to decide what actions to take after recording.'''
    def __init__(self, savewav=False, showplot=True, saveplot=False,
                 savetext=False, filename='Output'):
        self.savewav=savewav
        self.showplot=showplot
        self.saveplot=saveplot
        self.savetext=savetext
        self.filename=filename

    def act(self, signalrec, nchannelsrec, filename=None):
        
        if filename is None:
            filename = self.filename
        
        if filename is None and any((self.saveplot, self.savetext, self.savewav)):
            print('filename required.')
            return
        
        if self.savewav:
            savewav(signalrec, filename, datanchannels=nchannelsrec)
        
        signalrec = decode(signalrec, nchannelsrec)
        
        if self.showplot:
            signal_plot(signalrec)
            
            if self.saveplot:
                saveplot(filename)
        
        if self.savetext:
            savetext(signalrec, filename)
#%%

def play_callback_rec(signalplay, #1st column left
                      recording_duration=None,
                      nchannelsplay=1,
                      nchannelsrec=1,
                      samplerate=44100,
                      after_recording=None):
    
    """Plays a signal and records another one at the same time.
    
    This function plays an audio signal with a certain number of 
    channels. At the same time, it records another signal with a given 
    number of channels. It runs for a given time. And it plays and 
    records using the same sampling rate and the same pyaudio.paFloat32 
    format.
    
    Variables
    ---------
    stramplay: PyAudio stream
        The signal to be played.
    signalrecduration: int, float.
        Signals' duration in seconds.
    nchannelsplay: int
        Played signal's number of channels.
    nchannelsrec: int
        Recorded signal's number of channels.
    samplerate: int, float
        Signals' sampling rate.
    
    Returns
    -------
    signalrec: PyAudio byte stream
        Recorded signal.
    
    """
    
    if recording_duration is None:
        recording_duration = len(signalplay)/samplerate
        
    streamplay = play_callback(signalplay,
                               nchannelsplay=nchannelsplay,
                               formatplay=pyaudio.paFloat32,
                               samplerate=samplerate)
    
    streamrec = rec(nchannelsrec=nchannelsrec,
                    formatrec=pyaudio.paFloat32,
                    samplerate=samplerate)
    
    streamplay.start_stream()
    print("* Recording")
    streamrec.start_stream()
    signalrec = streamrec.read(int(samplerate * recording_duration))
    print("* Done recording")

    streamrec.stop_stream()
    streamplay.stop_stream()
    
    streamrec.close()
    streamplay.close()
    
    if after_recording is None:
        after_recording = AfterRecording()
    
    after_recording.act(signalrec, nchannelsrec)
    
    return signalrec

#%%

def signal_plot(signal, samplerate=44100, 
                plotunits=None, plotlegend=None):
    
    """Takes an audio signal and plots it as a function of time.
    
    It takes an audio signal recorded at a certain samplerate and plots 
    it as a function of time. The signal's units can be specified. The 
    signals' channels' names can also be specified if there's more than 
    one.
    
    Variables
    ---------
    signal: array, list
        Signal to be plotted (could have more than 1 column).
    samplerate=44100: int, float
        Signal's sampling rate.
    plotunits=None: None or string
        Signal's units as they would appear in Y-axis.
    plotlegend=None: None or list of strings.
        Signals' channels' names if there's more than one channel.
    
    Returns
    -------
    nothing        
    
    """
    
    try:
        n = len(signal[:,0])
        m = len(signal[0,:])
    except:
        n = len(signal)
        m = 1
    
    time = np.linspace(0, (n-1)/samplerate, n)
    
    plt.figure()
    plt.plot(time, signal)
    plt.grid()
    plt.xlabel('Tiempo (s)')
    if plotunits is not None:
        plt.ylabel('Señal ({})'.format(plotunits))
    else:
        plt.ylabel('Señal')
    if m != 1:
        if plotlegend is not None:
            plt.legend(plotlegend)
        else:
            plt.legend(['Izquierda','Derecha'])

#%%

def saveplot(filename,
             plotformat='pdf',
             savedir=os.getcwd(),
             overwrite=False):
    
    """Saves a plot on an image file.
    
    This function saves the current matplotlib.pyplot plot on an image 
    file. Its format is given by 'plotformat'. And it is saved on 
    'savedir' directory. If overwrite=False, it checks whether 
    'filename.plotformat' exists or not; if it already exists, it saves 
    the plot as 'filename (2).plotformat'. If overwrite=True, it saves 
    the plot on 'filename.plotformat' even if it already exists.
    
    Variables
    ---------
    filename: string
        The name you wish the file to have.
    plotformat='pdf': string
        The file's format.
    savedir=os.getcwd(): string
        The directory where the file is saved.
    overwrite=False: bool
        Parameter that allows to overwrite files.
    
    Returns
    -------
    nothing
    
    Yields
    ------
    an image file
    
    """
    
    home = os.getcwd()
    
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    
    os.chdir(savedir)
    
    if not overwrite:
        while os.path.isfile(filename+'.'+plotformat):
            filename = filename + ' (2)'

    plt.savefig((filename + '.' + plotformat), bbox_inches='tight')
    
    os.chdir(home)
    
    print('Archivo {}.{} guardado'.format(filename, plotformat))
    

#%%

def savetext(datanumpylike,
             filename,
             savedir=os.getcwd(),
             overwrite=False):
    
    """Takes some array-like data and saves it on a .txt file.
    
    This function takes some data and saves it on a .txt file on 
    savedir directory. If overwrite=False, it checks whether 
    'filename.txt' exists or not; if it already exists, it saves the 
    data as 'filename (2).txt'. If overwrite=True, it saves the data 
    on 'filename.txt' even if it already exists.
    
    Variables
    ---------
    datanumpylike: array, list
        The data to be saved.
    filename: string
        The name you wish the .txt file to have.
    savedir=os.getcwd: string
        The directory you wish to save the .txt file at.
    overwrite=False: bool
        A parameter which allows or not to overwrite a file.
    
    Return
    ------
    nothing
    
    Yield
    -----
    .txt file
    
    """
    
    home = os.getcwd()
    
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    
    os.chdir(savedir)
    
    if not overwrite:
        while os.path.isfile(filename+'.txt'):
            filename = filename + ' (2)'

    np.savetxt((filename+'.txt'), np.array(datanumpylike), 
               delimiter='\t', newline='\n')

    os.chdir(home)
    
    print('Archivo {}.txt guardado'.format(filename))
    
    return

#%%

def savewav(datapyaudio,
            filename,
            datanchannels=1,
            dataformat=pyaudio.paFloat32,
            samplerate=44100,
            savedir=os.getcwd(),
            overwrite=False):
    
    """Takes a PyAudio byte stream and saves it on a .wav file.
    
    Takes a PyAudio byte stream and saves it on a .wav file at savedir 
    directory. It specifies some parameters: number of audio channels, 
    format of the audio data, sampling rate of the data. If 
    overwrite=False, it checks whether 'filename.wav' exists or not; if 
    it already exists, then it saves it as 'filename (2).wav'. If 
    overwrite=True, it saves it as 'filename.wav' even if it already 
    exists.
    
    """
    
    home = os.getcwd()
    
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    
    os.chdir(savedir)
    
    if not overwrite:
        while os.path.isfile(filename+'.wav'):
            filename = filename + ' (2)'
    
    datalist = []
    datalist.append(datapyaudio)
    
    os.chdir(savedir)
    
    p = pyaudio.PyAudio()
    wf = wave.open((filename + '.wav'), 'wb')
    
    wf.setnchannels(datanchannels)
    wf.setsampwidth(p.get_sample_size(dataformat))
    wf.setframerate(samplerate)
    wf.writeframes(b''.join(datalist))
    
    wf.close()

    os.chdir(home)
    
    print('Archivo {}.wav guardado'.format(filename))
    
    return
