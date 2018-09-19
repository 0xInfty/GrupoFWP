# -*- coding: utf-8 -*-
"""
This module defines classes to manipulate lab instruments via PyVisa.

Osci:
    Allows communication with a Tektronix Digital Oscilloscope.

@author: Vall
"""

import visa

class Osci:
    
    """Allows communication with a Tektronix Digital Oscilloscope.
    
    It allows communication with multiple models, based on the official 
    Programmer Guide (https://www.tek.com/oscilloscope/tds1000-manual).
    
        TBS1000B/EDU, 
        TBS1000, 
        TDS2000C/TDS1000C-EDU,
        TDS2000B/TDS1000B, 
        TDS2000/TDS1000, 
        TDS200,
        TPS2000B/TPS2000.
    
    Examples
    --------
    >> osci = Osci(port='USB0::0x0699::0x0363::C108013::INSTR')
    >> result, units = osci.measure('Min', 1, print_result=True)
    1.3241 V
    >> result
    1.3241
    >> units
    'V'   
    
    """

    def __init__(self, port):
        
        """Defines oscilloscope object and opens it as Visa resource.
        
        Variables
        ---------
        port: str
            Computer's port where the oscilloscope is connected.
            i.e.: 'USB0::0x0699::0x0363::C108013::INSTR'
        
        """
        
        rm = visa.ResourceManager()
        osci = rm.open_resource(port, read_termination="\n")
        
        # General Configuration
        osci.write('DAT:ENC RPB')
        osci.write('DAT:WID 1') # Binary transmission mode
        
        # Trigger configuration
        osci.write('TRIG:MAI:MOD NORM') # Waits for the trigger
        osci.write('TRIG:MAI:TYP EDGE')
        osci.write('TRIG:MAI:LEV 5')
        osci.write('TRIG:MAI:EDGE:SLO RIS')
        osci.write('TRIG:MAI:EDGE:SOU EXT')
        osci.write('HOR:MAI:POS 0') # Makes the complete measure at once
        
        self.port = port
        self.osci = osci
        
    def measure(self, measure_type, measure_ch=1, print_result=False):
        
        """Takes a measure of a certain type on a certain channel.
        
        Variables
        ---------
        measure_type: str
            Key that configures the measure type.
            i.e.: 'Min', 'min', 'minimum', etc.
        measure_ch=1: int {1, 2}
            Number of the measure's channel.
        
        Returns
        -------
        result: int, float
            Measured value.
        units: str
            Measured value's units.
        
        """
        
        self.config_measure(measure_type, measure_ch)
        
        result = self.osci.query('MEAS:MEAS1:VAL?')
        units = self.osci.query('MEAS:MEAS1:UNI?')
        
        if print_result:
            print("{} {}".format(result, units))
        
        return result, units
        
    def config_measure(self, measure_type, measure_ch):

        dic = {'mean': 'MEAN',
               'min': 'MINI',
               'max': 'MAXI',
               'freq': 'FREQ',
               'per': 'PER',
               'rms': 'RMS',
               'amp': 'PK2', # absolute difference between max and min
               'ph': 'PHA',
               'crms': 'CRM', # RMS on the first complete period
               'cmean': 'CMEAN',
               'rise': 'RIS', # time betwee  10% and 90% on rising edge
               'fall': 'FALL',
               'low': 'LOW', # 0% reference
               'high': 'HIGH'} # 100% reference

        if measure_ch != 1 and measure_ch != 2:
            print("Measure channel unrecognized ('CH1' as default).")
            measure_ch = 1
        
        if 'c' in measure_type.lower():
            if 'rms' in measure_type.lower():
                measure_type = dic['crms']
            else:
                measure_type = dic['cmean']
        else:
            for key, value in dic:
                if key in measure_type.lower():
                    measure_type = value
            if measure_type not in dic.values():
                measure_type = 'FREQ'
                print("Measure type unrecognized ('FREQ' as default).")
            
        self.osci.write('MEASU:MEAS1:SOU CH{:.0f}'.format(measure_ch))
        self.osci.write('MEASU:MEAS1:TYP {}'.format(measure_type))
        
        return
