# -*- coding: utf-8 -*-
"""
Obtain trace from Keysight DSOX2024A Oscilloscope

See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import visa

def queryChannels(instrument='USB0::2391::6038::MY57233636::INSTR'):

    ## Initialise
    rm = visa.ResourceManager()
    inst = rm.open_resource(instrument)
    inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
    id = inst.query('*IDN?') # get the id of the connected device
    print('Connected to ', id)

    print("Channel 1:", inst.query(':CHANnel1:DISPlay?'))
    print("Channel 2:", inst.query(':CHANnel2:DISPlay?'))
    print("Channel 3:", inst.query(':CHANnel3:DISPlay?'))
    print("Channel 4:", inst.query(':CHANnel4:DISPlay?'))

    inst.close()

queryChannels()
