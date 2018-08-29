# -*- coding: utf-8 -*-
"""
Función Play+Record

@author: Usuario
"""


def check_devices():
    """Imprime los puertos de entrada y salida con nombre e índice.
    
    Basado en: https://stackoverflow.com/questions/36894315/how-to-select-a-specific-input-device-with-pyaudio
    """
    
    from pyaudio import PyAudio
    
    p = PyAudio()
    
    info = p.get_host_api_info_by_index(0)
    
    numdevices = info.get('deviceCount')
    
    for i in range(0, numdevices):
            
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", 
                       p.get_device_info_by_host_api_device_index(0, i).get('name'))

        else:
            print ("Output Device id ", i, " - ", 
                       p.get_device_info_by_host_api_device_index(0, i).get('name'))