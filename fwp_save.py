# -*- coding: utf-8 -*-
"""
Save Module

This module contains some functions that save data into files.

new_dir: Makes and returns a new related directory to avoid overwriting.
new_filename: Returns a related free file name to avoid overwriting.
saveplot: Saves a matplotlib.pyplot plot on an image file (i.e: 'png').
savetext: Saves some np.array like data on a '.txt' file.
savewav: Saves a PyAudio encoded audio on a '.wav' file.

@author: Vall
@date: 09-17-2018
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pyaudio
import wave

#%%

def new_dir(my_dir, into_dir, newformat='{}_{}'):
    
    """Makes and returns a new directory to avoid overwriting.
    
    Takes a directory name 'dirname' and checks whether it already 
    exists on 'intodir' directory. If it doesn't, it returns 'dirname'. 
    If it does, it returns a related unoccupied directory name.
    
    Parameters
    ----------
    my_dir: str
        Desired directory.
    into_dir: str
        Directory's directory.
    
    Returns
    -------
    new_dir: str
        New directory.
    
    Yields
    ------
    new_dir: directory
    
    """
        
    home = os.getcwd()
    
    os.chdir(into_dir)
    
    sepformat = newformat.split('{}')
    new_dir = my_dir
    while os.path.isdir(new_dir):
        new_dir = new_dir.split(sepformat[-2])[-1]
        try:
            new_dir = new_dir.split(sepformat[-1])[0]
        except ValueError:
            new_dir = new_dir
        try:
            new_dir = newformat.format(my_dir, str(int(new_dir)+1))
        except ValueError:
            new_dir = newformat.format(my_dir, 2)
    os.makedirs(new_dir)
    
    os.chdir(new_dir)
    
    new_dir = os.getcwd()
    
    os.chdir(home)
    
    return new_dir

#%%

def new_filename(filename, filetype, savedir, newformat='{}_{}'):
    
    """Makes a name for a new file to avoid overwriting.
        
    Takes a file name 'filename' and its file format 'filetype' as if 
    you were thinking to make a new file 'filename.filetype' in 
    'savedir' directory. It returns a related unnocupied file name.
        
    Parameters
    ----------
    filename: str
        Tentative file name.
    filetype: str
        Desired file format.
    savedir: str
        Desired file directory.
    newformat='{}_{}': str
        Format string that indicates how to make new names.
    
    Returns
    -------
    new_fname: str
        Unoccupied file name.
        
    """
    
    home = os.getcwd()
    
    if not os.path.isdir(savedir):
        new_filename = filename
    
    else:
        os.chdir(savedir)
        sepformat = newformat.split('{}')
        new_filename = filename
        while os.path.isfile(new_filename+'.'+filetype):
            new_filename = new_filename.split(sepformat[-2])[-1]
            try:
                new_filename = new_filename.split(sepformat[-1])[0]
            except ValueError:
                new_filename = new_filename
            try:
                new_filename = newformat.format(
                        filename, 
                        str(int(new_filename)+1),
                        )
            except ValueError:
                new_filename = newformat.format(filename, 2)
    
    os.chdir(home)
    
    return new_filename

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
        filename = new_filename(filename, plotformat, savedir)

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
        filename = new_filename(filename, 'txt', savedir)

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
        filename = new_filename(filename, 'wav', savedir)
    
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
