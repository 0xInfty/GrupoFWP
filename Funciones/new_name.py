# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 21:48:06 2018

@author: Usuario
"""

def new_name(fname, ftype, fdir):
    """Makes a name for a new file to avoid overwriting.
    
Takes a file name 'fname' and its file format 'ftype' as if you were \
thinking to make a new file 'fname.ftype' in 'fdir' directory. If no \
'fdir' directory exists, then it makes a new 'fdir' directory. It then \
returns the name of an unoccupied file.
    
Parameters
----------
fname: str
    Tentative file name.
ftype: str
    Desired file format.
fdir: str
    Desired file directory.

Returns
-------
new_fname: str
    Unoccupied file name.
    
    """
    
    from os import getcwd, makedirs, chdir
    from os.path import isdir, isfile
    
    home = getcwd()
    
    if not isdir(fdir):
        makedirs(fdir)
        new_fname = fname
    
    else:
        chdir(fdir)
        new_fname = fname
        while isfile(new_fname+'.'+ftype):
            new_fname = new_fname + ' (2)'        
        
    chdir(home)
    
    return new_fname
    