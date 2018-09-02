# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:42:57 2018

@author: 0xInfty
"""

def wav_to_txt(
    fname, 
    fdir='C:\\Users\\Usuario\\Documents\\Git\\Público\\GrupoFWP',
    gdir='C:\\Users\\Usuario\\Documents\\Git\\Público\\Pais',
    returndata=False,
    ):

    """File conversion from '.wav' to '.txt'
    
Takes the wav file named fname from the fdir directory and converts it \
to txt. If returndata=True, this function also returns an array \
containing time and data from all the chanels
    
Variables:
>> fname (str) [wav file name, without format]
>> fdir (str) [wav file directory]
>> gdir (str) [txt file directory]

Returns:
>> return_datos (array) [wav data, where first column is time]
    
Beware:
- It takes the file name as fname; i.e. "Hi" and not "Hi.wav".
- It saves the txt file with fname name; i.e. fname="Hi" converts \
fdir\\Hi.wav into gdir\\Hi.wav

Raises:
- RuntimeWarning if wav file would make a txt file with more than \
500 000 rows.
    
    """
    
    from numpy import arange, savetxt, zeros
    from scipy.io import wavfile
    from os import getcwd, makedirs, chdir
    from os.path import isdir, isfile
    
    home = getcwd()
    chdir(fdir)
    
    file = fname + '.wav'

    sr, datos = wavfile.read(file)
    
    n = len(datos[:,0])
    if n > 500000:
        raise RuntimeWarning("Wav file is too long")
        
    t = arange(0, n/sr, 1/sr)
    ch = len(datos[0,:])

    if isdir(gdir) == False:
        makedirs(gdir)
    chdir(gdir)

    return_datos = zeros(n, ch+1)
    return_datos[:,0] = t
    return_datos[:,1:] = datos

    fnamet = fname
    while isfile(fnamet+'.txt') == True:
        fnamet = fnamet + ' (2)'
    savetxt((fnamet+'.txt'), return_datos, delimiter='\t', newline='\n')
    
    chdir(home)
    
    if returndata:
        return return_datos
    else:
        return
