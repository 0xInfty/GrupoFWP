# -*- coding: utf-8 -*-
"""
Save Module

This module contains some functions that save data into files.

@author: Vall
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pyaudio
import wave

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
