# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 17:26:06 2018

@author: Marcos
"""

# -*- coding: utf-8 -*-
"""
Osciloscopio Tektronix TDS1002B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS1002 Manual.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TDS 100-1000-2000_prog.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\TDS1002 Manual.pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\TDS 200-1000-2000_prog.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import

import time

from matplotlib import pyplot as plt
import numpy as np
import visa

print(__doc__)
#%%
# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'USB0::0x0699::0x0363::C102220::INSTR'

rm = visa.ResourceManager()

osci = rm.open_resource(resource_name)

osci.query('*IDN?')

# Le pido algunos parametros de la pantalla, para poder escalear adecuadamente
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

# Modo de transmision: Binario
osci.write('DAT:ENC RPB')
osci.write('DAT:WID 1')

# Adquiere los datos del canal 1 y los devuelve en un array de numpy
data = osci.query_binary_values('CURV?', datatype='B', container=np.array)

tiempo = xze + np.arange(len(data)) * xin

plt.plot(tiempo, data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')


# Si vas a repetir la adquisicion muchas veces sin cambiar la escala
# es util definir una funcion que mida y haga las cuentas
def definir_medir(inst):
    xze, xin, yze, ymu, yoff = inst.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

    # creamos una function auxiliar
    def _medir():
        # Adquiere los datos del canal 1 y los devuelve en un array de numpy
        data = inst.query_binary_values('CURV?', datatype='B', container=np.array)
        data = yze + ymu * (data - yoff)
        
        tiempo = xze + np.arange(len(data)) * xin
        print('Medí')
        return tiempo, data
    
    # Devolvemos la funcion auxiliar que "sabe" la escala
    return _medir

#%%
    
import fwp_lab_instruments as ins
import fwp_pyaudio as fwp
import fwp_save as sav
import matplotlib.pyplot as plt
import numpy as np
import os
import pyaudiowave as paw
import wavemaker as wmaker


medir = definir_medir(osci)

amp = .7
 
seno = wmaker.Wave('sine', frequency=2000, amplitude=amp)
signalmaker = paw.PyAudioWave(nchannels=2)

#seno.amplitude = amp #update signals ampitude
signal_to_play = signalmaker.generator_setup(seno, duration=2 ) 

tiempo, data = fwp.just_play_NB(signal_to_play, do_while_playing=medir, wait_time=.3)

#    plt.figure()
plt.plot(tiempo, data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')

file = os.path.join('Measurements', 'amp{}.txt'.format(amp))
sav.savetext(np.array([tiempo, data]).T, file)
#%%

#osci.close()


amp_start = 1
amp_stop = .5
amp_step = -0.05

freq = 2000
n_per = 50
duration = n_per/freq

port = 'USB0::0x0699::0x0363::C102220::INSTR'

name = 'Cal_Play_{:.0f}_Hz'.format(freq)
after_record_do = fwp.AfterRecording(savetext = True)

osci = ins.Osci(port=port)
seno = wmaker.Wave('sine', frequency=freq)
signalmaker = paw.PyAudioWave(nchannels=2)

savedir = sav.new_dir(os.path.join(os.getcwd(), 'Measurements', name))
filename = os.path.join(savedir, name)
makefile = lambda amp: '{}_{:.2f}'.format(filename, amp)

amplitude = np.arange(amp_start, amp_stop, amp_step)
amp_osci = []

def measure():
    medir
    return result_left, result_right


for amp in amplitude:
    
    seno.amplitude = amp #update signals ampitude
    signal_to_play = signalmaker.generator_setup(seno, duration=1 ) 
    
    result = fwp.just_play_NB(signal_to_play, measure)
    amp_osci.append(result)

#amp_osci = np.array(amp_osci)

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
