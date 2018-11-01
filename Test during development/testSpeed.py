# -*- coding: utf-8 -*-
"""
Obtain trace from Keysight DSOX2024A Oscilloscope

See Keysight's Programmer's Guide for reference.

Andreas Svela 2018

Tektronix TCPIP0::192.168.20.30::4000::SOCKET
"""

import visa
import numpy as np
import time

def testSpeed(channel_nums=[''], source_type='CHANnel', instrument='USB0::2391::6038::MY57233636::INSTR', acq_type='HRESolution', num_averages=2, p_mode='RAW', num_points=0):
    """
    Get trace from channel of instrument. Some alternative settings are listed.
    channelnum = : use a list with an empty string [''] to capture all currently displayed channels
    source_type = {'CHANnel' | 'MATH' | 'FUNCtion'}: MATH is an alias for FUNCtion
    instrument = {'USB0::2391::6038::MY57233636::INSTR' | 'TCPIP0::192.168.20.30::4000::SOCKET'}
    acq_type = {'HRESolution' | 'NORMal'}
    num_averages = 2 to 65536: applies only to the NORMal mode
    p_mode = {'RAW' | 'MAXimum'}: RAW gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
    num_points = {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000
                 | 50000 | 100000 | 200000 | 500000 | 1000000}: optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.
    """

    ## Initialise
    rm = visa.ResourceManager()
    inst = rm.open_resource(instrument)
    # For Serial and TCP/IP socket connections enable the read Termination Character, or reads will timeout
    if inst.resource_name.startswith('ASRL') or inst.resource_name.endswith('SOCKET'):
        inst.read_termination = '\n'
    inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
    id = inst.query('*IDN?') # get the id of the connected device
    print('Connected to ', id)

    #inst.write(':ACQuire:COMPlete 100') # completion criteria for acquisition: 100 percent of the time buckets must be full for the acquisition to be complete (100 is only value possible)
    inst.write(':ACQuire:TYPE ' + acq_type)
    if acq_type == 'NORMal': # averaging only applies for the NORMal mode
        inst.write(':ACQuire:COUNt ' + str(num_averages))

    ## Set options for waveform export
    inst.write(':WAVeform:FORMat ASCii') # values are transferred as ASCii digits in floating point notation, separated by commas
    inst.write(':WAVeform:POINts:MODE ' + p_mode)
    #print("Max number of points for mode %s: %s" % (p_mode, inst.query(':WAVeform:POINts? MAXimum')))
    if num_points != 0: #if number of points has been specified
        inst.write(':WAVeform:POINts ' + str(num_points))
        print("Number of points set to ", num_points)

    ## Select sources
    if channel_nums == ['']: # if no channels specified, find the channels currently active and aquire from those
        channels = np.array(['1', '2', '3', '4'])
        channel_mask = np.array([int(inst.query(':CHANnel'+channel+':DISPlay?')[0]) for channel in channels]) # get a mask of ones and zeros for the channels that are on by querying DISP for each channel
        channel_nums =channels[channel_mask] # apply mask to the channel list
    sources = [source_type+channel for channel in channel_nums] # build list of sources
    sourcesstring = ", ".join([source_type+channel for channel in channel_nums]) # make string of sources
    print("Acquiring from sources ", sourcesstring)

    ## Capture data
    inst.write(':DIGitize ' + sourcesstring) # DIGitize is a specialized RUN command.
                                             # Waveforms are acquired according to the settings of the :ACQuire commands.
                                             # When acquisition is complete, the instrument is stopped.
    # Read out data
    print("start dynamic capture")
    start = time.time()
    raw = []
    for source in sources:
        inst.write(':WAVeform:SOURce ' + source) # selects the channel for which the succeeding WAVeform commands applies to
        raw.append(inst.query(':WAVeform:DATA?')) # read out data for each channel
    end = time.time()
    print("elapsed:", end-start)
    measurement_time = float(inst.query(':TIMebase:RANGe?')) # returns the current full-scale range value for the main window

    print("start explicit capture")
    start = time.time()
    inst.write(':WAVeform:SOURce CHAN1')
    raw1 = inst.query(":WAVeform:DATA?")
    inst.write(':WAVeform:SOURce CHAN2')
    raw2 = inst.query(":WAVeform:DATA?")
    inst.write(':WAVeform:SOURce CHAN3')
    raw3 = inst.query(":WAVeform:DATA?")
    inst.write(':WAVeform:SOURce CHAN4')
    raw4 = inst.query(":WAVeform:DATA?")
    end = time.time()
    print("elapsed:", end-start)

    ## Process data
    y = []
    for data in raw:
        data = data.split(data[:10])[1] # remove first 10 characters (is this a quick but not so intuitive way?)
        data = data.split(',') # samples separated by commas
        data = np.array([float(sample) for sample in data])
        y.append(data)

    num_samples = np.size(y[0]) # number of samples captured per channel
    x = np.linspace(0, measurement_time, num_samples) # compute x-values
    print("Points captured per channel: ", num_samples)

    inst.write(':RUN')
    inst.close()

    #return x, y

testSpeed(channel_nums=['1', '2', '3','4'], num_points=1000)
testSpeed(channel_nums=['1', '2', '3','4'], num_points=1000, instrument='TCPIP0::192.168.20.30::4000::SOCKET')
