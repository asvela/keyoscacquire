#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from (Keysight) oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

This script can be called resulting in one trace being captured and stored.
Optional argument from the command line: string setting the base filename of the output files.
Change the VISA_ADDRESS under default options to the desired instrument.

Tested with Keysight DSOX2024A.
See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import sys, os  # required for reading user input and command line arguments
import visa # instrument communication
import numpy as np, matplotlib.pyplot as plt
import time, datetime # for measuring elapsed time and adding current date and time to exported files

from keysightoscacquire.default_options import VISA_ADDRESS, WAVEFORM_FORMAT, CH_NUMS, ACQ_TYPE, NUM_AVG, FILENAME, FILETYPE, TIMEOUT, EXPORT_PNG, SHOW_PLOT # local file with default options

##============================================================================##

def initialise(instrument, timeout=TIMEOUT, wav_format=WAVEFORM_FORMAT, acq_type='HRESolution', num_averages=2, p_mode='RAW', num_points=0):
    """
    Open a connection to instrument and choose settings for the connection and acquisitionself.
    Output: instrument object, identity of the instrument
    Some alternative settings are listed.
    instrument = {'USB0::2391::6038::MY57233636::INSTR' | 'TCPIP0::192.168.20.30::4000::SOCKET'}
    timeout = ms before timeout on the channel to the instrument
    wav_format = {'BYTE' | 'ASCii'}
    acq_type = {'HRESolution' | 'NORMal'}
    num_averages = 2 to 65536: applies only to the NORMal mode
    p_mode = {'RAW' | 'MAXimum'}: RAW gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
    num_points = {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000
                 | 50000 | 100000 | 200000 | 500000 | 1000000}: optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.
    """
    try:
        rm = visa.ResourceManager()
        inst = rm.open_resource(instrument)
    except visa.Error as ex:
        print('\nVisaError: Could not connect to \'%s\', exiting now...' % instrument)
        sys.exit()
    # For TCP/IP socket connections enable the read Termination Character, or reads will timeout
    if inst.resource_name.endswith('SOCKET'):
        inst.read_termination = '\n'

    inst.timeout = timeout
    inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
    id = inst.query('*IDN?') # get the id of the connected device
    print('Connected to ', id)

    #inst.write(':ACQuire:COMPlete 100') # completion criteria for acquisition: 100 percent of the time buckets must be full for the acquisition to be complete (100 is only value possible)
    inst.write(':ACQuire:TYPE ' + acq_type)
    print("Acquiring type ", acq_type, end='')
    if acq_type[:4] == 'NORM' or acq_type[:4] == 'AVER': # averaging applies for NORMal and AVERage modes only
        #inst.write(':ACQuire:MODE RTIME')
        inst.write(':ACQuire:COUNt ' + str(num_averages))
        print(", number of averages ", num_averages)
    else:
        print("") #newline

    ## Set options for waveform export
    inst.write(':WAVeform:FORMat ' +  wav_format) # choose format for the transmitted waveform
    if acq_type[:4] == 'AVER' and p_mode[:4] != 'NORM':
        inst.write(':WAVeform:POINts:MODE NORMal')
        print(":WAVeform:POINts:MODE overridden (from %s) to NORMal due to :ACQuire:TYPE:AVERage." % p_mode)
    else:
        inst.write(':WAVeform:POINts:MODE ' + p_mode)
    #print("Max number of points for mode %s: %s" % (p_mode, inst.query(':WAVeform:POINts? MAXimum')))
    if num_points != 0: #if number of points has been specified
        inst.write(':WAVeform:POINts ' + str(num_points))
        print("Number of points set to: ", num_points)
    return inst, id

def capture_and_read(inst, sources, sourcestring, wav_format=WAVEFORM_FORMAT):
    if wav_format[:3] == 'WOR':
        return capture_and_read_binary(inst, sources, sourcestring, datatype='H')
    elif wav_format[:3] == 'BYT':
        return capture_and_read_binary(inst, sources, sourcestring, datatype='B')
    elif wav_format[:3] == 'ASC':
        return capture_and_read_ascii(inst, sources, sourcestring)
    else:
        raise Exception("\nError: Could not capture and read data, waveform format \'{}\' is unknown.\nExiting..\n".format(wav_format))
        sys.exit()

def capture_and_read_binary(inst, sources, sourcesstring, datatype='H'):
    """
    Capture and read data and metadata from sources of the oscilloscope inst when waveform format is WORD or BYTE
    Datatype is 'H' for 16 bit unsigned int (WORD), 'B' for 8 bit unsigned bit (BYTE)
    Output: array of raw data, array of preamble metadata (ascii comma separated values)
    """
    ## Capture data
    print("Start acquisition..")
    start_time = time.time() # time the acquiring process
    reg = int(inst.query(':OPERegister:CONDition?')) # The third bit of the operation register is 1 if the instrument is running
        # If the instrument is not running, we presumably want the data on the screen and hence don't want
        # to use DIGitize as digitize will obtain a new trace.
    if (reg & 8) == 8: # If the third bit is 1 (ie. instrument is running)
        inst.write(':DIGitize ' + sourcesstring) # DIGitize is a specialized RUN command.
                                                 # Waveforms are acquired according to the settings of the :ACQuire commands.
                                                 # When acquisition is complete, the instrument is stopped.

    ## Read out meta data and data
    raw, preambles = [], []
    for source in sources:
        inst.write(':WAVeform:SOURce ' + source) # selects the channel for which the succeeding WAVeform commands applies to
        try:
            preambles.append(inst.query(':WAVeform:PREamble?')) # comma separated metadata values for processing of raw data for this source
            raw.append(inst.query_binary_values(':WAVeform:DATA?', datatype=datatype)) # read out data for this source
        except visa.Error as err:
            print("\nError: Failed to obtain waveform, have you checked that the TIMEOUT (currently %d ms) is sufficently long?" % TIMEOUT)
            print(err)
            print("\nExiting..\n")
            inst.write(':RUN')
            sys.exit()
    print("Elapsed time:", time.time()-start_time)
    inst.write(':RUN') # set the oscilloscope running again
    return raw, preambles

def capture_and_read_ascii(inst, sources, sourcesstring):
    """
    Capture and read data and metadata from sources of the oscilloscope inst when waveform format is ASCii
    Output: array of raw data (commaseparated ascii values), time range of the measurement
    """
    ## Capture data
    print("Start acquisition..")
    start_time = time.time() # time the acquiring process
    reg = int(inst.query(':OPERegister:CONDition?')) # The third bit of the operation register is 1 if the instrument is running
        # If the instrument is not running, we presumably want the data on the screen and hence don't want
        # to use DIGitize as digitize will obtain a new trace.
    if (reg & 8) == 8: # If the third bit is 1 (ie. instrument is running)
        inst.write(':DIGitize ' + sourcesstring) # DIGitize is a specialized RUN command.
                                                 # Waveforms are acquired according to the settings of the :ACQuire commands.
                                                 # When acquisition is complete, the instrument is stopped.
    ## Read out data
    raw = []
    for source in sources: # loop through all the sources
        inst.write(':WAVeform:SOURce ' + source) # selects the channel for which the succeeding WAVeform commands applies to
        try:
            raw.append(inst.query(':WAVeform:DATA?')) # read out data for this source
        except visa.Error as err:
            print("\nVisaError: Failed to obtain waveform, have you checked that the TIMEOUT (currently %d ms) is sufficently long?" % TIMEOUT)
            print(err)
            print("\nExiting..\n")
            inst.write(':RUN')
            sys.exit()
    print("Elapsed time:", time.time()-start_time)
    measurement_time = float(inst.query(':TIMebase:RANGe?')) # returns the current full-scale range value for the main window
    inst.write(':RUN') # set the oscilloscope running again
    return raw, measurement_time

def process_data(raw, metadata,  wav_format=WAVEFORM_FORMAT):
    if wav_format[:3] == 'WOR' or wav_format[:3] == 'BYT':
        return process_data_binary(raw, metadata)
    elif wav_format[:3] == 'ASC':
        return process_data_ascii(raw, metadata)
    else:
        raise Exception("\nError: Could not process data, waveform format \'{}\' is unknown.\nExiting..\n".format(wav_format))
        sys.exit()

def process_data_binary(raw, preambles):
    """
    Process raw 8/16-bit data to time x values and y voltage values.
    Output: numpy array x containing time values, numpy array y containing voltages for caputred channels
    """
    preamble = preambles[0].split(',')  # values separated by commas
    # 0 FORMAT : int16 - 0 = BYTE, 1 = WORD, 4 = ASCII.
    # 1 TYPE : int16 - 0 = NORMAL, 1 = PEAK DETECT, 2 = AVERAGE
    num_samples = int(preamble[2])    # POINTS : int32 - number of data points transferred.
    # 3 COUNT : int32 - 1 and is always 1.
    xIncr = float(preamble[4])        # XINCREMENT : float64 - time difference between data points.
    xOrig = float(preamble[5])        # XORIGIN : float64 - always the first data point in memory.
    xRef = int(preamble[6])           # XREFERENCE : int32 - specifies the data point associated with x-origin.
    # 7 YINCREMENT : float32 - voltage diff between data points.
    # 8 YORIGIN : float32 - value is the voltage at center screen.
    # 9 YREFERENCE : int32 - specifies the data point where y-origin occurs.

    print("Points captured per channel: ", num_samples)
    y = []
    for i, data in enumerate(raw):
        preamble = preambles[i].split(',')
        yIncr, yOrig, yRef = float(preamble[7]), float(preamble[8]), int(preamble[9])
        data = np.array([((sample-yRef)*yIncr)+yOrig for sample in data])
        y.append(data) # add the voltage values for this channel to y array

    y = np.transpose(np.array(y)) # convert y to np array and transpose for vertical channel columns in csv file
    x = np.array([((sample-xRef)*xIncr)+xOrig for sample in range(num_samples)]) # compute x-values
    x = np.vstack(x) # make x values vertical
    return x, y

def process_data_ascii(raw, measurement_time):
    """
    Process raw comma separated ascii data to time x values and y voltage values.
    Output: numpy array x containing time values, numpy array y containing voltages for caputred channels
    """
    y = []
    for data in raw:
        data = data.split(data[:10])[1] # remove first 10 characters (is this a quick but not so intuitive way?)
        data = data.split(',') # samples separated by commas
        data = np.array([float(sample) for sample in data])
        y.append(data) # add ascii data for this channel to y array

    y = np.transpose(np.array(y))
    num_samples = np.shape(y)[0] # number of samples captured per channel
    x = np.linspace(0, measurement_time, num_samples) # compute x-values
    x = np.vstack(x) # make list vertical
    print("Points captured per channel: ", num_samples)
    return x, y

def connect_and_getTrace(channel_nums=[''], source_type='CHANnel', instrument=VISA_ADDRESS, timeout=TIMEOUT,
                         wav_format=WAVEFORM_FORMAT, acq_type='HRESolution', num_averages=2, p_mode='RAW', num_points=0):
    """
    Get trace from channels of instrument. Returns one numpy array of the x time values and one numpy array of y values.
    Some alternative settings are listed.
    channelnum = list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
    source_type = {'CHANnel' | 'MATH' | 'FUNCtion'}: MATH is an alias for FUNCtion
    timeout = ms before timeout on the channel to the instrument
    wav_format = {'BYTE' | 'ASCii'}
    instrument = {'USB0::2391::6038::MY57233636::INSTR' | 'TCPIP0::192.168.20.30::4000::SOCKET'}
    acq_type = {'HRESolution' | 'NORMal'}
    num_averages = 2 to 65536: applies only to the NORMal mode
    p_mode = {'RAW' | 'MAXimum'}: RAW gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
    num_points = {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000
                 | 50000 | 100000 | 200000 | 500000 | 1000000}: optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.
    """
    ## Connect to instrument and specify acquiring settings
    inst, id = initialise(instrument, timeout,  wav_format, acq_type, num_averages, p_mode, num_points)

    ## Select sources
    if channel_nums == ['']: # if no channels specified, find the channels currently active and acquire from those
        channels = np.array(['1', '2', '3', '4'])
        displayed_channels = [inst.query(':CHANnel'+channel+':DISPlay?')[0] for channel in channels] # querying DISP for each channel to determine which channels are currently displayed
        channel_mask = np.array([bool(int(i)) for i in displayed_channels]) # get a mask of bools for the channels that are on [need the int() as int('0') = True]
        channel_nums = channels[channel_mask] # apply mask to the channel list
    sources = [source_type+channel for channel in channel_nums] # build list of sources
    sourcesstring = ", ".join([source_type+channel for channel in channel_nums]) # make string of sources
    print("Acquire from sources", sourcesstring)

    ## Capture, read and process data
    raw, preambles = capture_and_read(inst, sources, sourcesstring,  wav_format)
    x, y = process_data(raw, preambles,  wav_format)

    ## Closing the connection
    inst.close()
    return x, y, id, channel_nums

def check_file(fname, ext, num=""):
    """
    Checking if file fname+num+ext exists. If it does the user is prompted
    for a string to append to fname until a unique fname is found.
    Output: new fname.
    """
    while os.path.exists(fname+num+ext):
        append = input("File \'%s\' exists! Append to filename \'%s\' before saving: " % (fname+num+ext, fname))
        fname += append
    return fname

def saveTrace(filename, x, y, fileheader=""):
    """
    Saves the trace with x values and y values as a txt/csv/dat etc specified by the filename string containing the extension.
    Current date and time is automatically added to the header.
    """
    date_time = str(datetime.datetime.now()) # get current date and time
    print("Saving trace to ", filename)
    data = np.append(x, y, axis=1) # make one array with coloumns x y1 y2 ..
    np.savetxt(filename, data, delimiter=",", header=fileheader+date_time)
    print("\n")

def plotTrace(x, y, channel_nums, fname="", show=SHOW_PLOT, savepng=EXPORT_PNG):
    """
    Plots the trace with channel colours according to the Keysight colourmap
    and saves as a png with filename 'fname'.
    """
    colors = {'1':'C1', '2':'C2', '3':'C0', '4':'C3'} # Keysight colour map
    i = 0
    for vals in np.transpose(y): # for each channel
        plt.plot(x, vals, color=colors[channel_nums[i]])
        i += 1
    if savepng: plt.savefig(fname+".png", bbox_inches='tight')
    if show: plt.show()
    plt.close()


##============================================================================##
##                           MAIN FUNCTION                                    ##
##============================================================================##

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    if len(sys.argv) == 2: #if optional argument is supplied on the command line
        fname = sys.argv[1] # use this as the filename base
    else:
        fname = FILENAME
    ext = FILETYPE
    fname = check_file(fname, ext)
    x, y, id, channel_nums = connect_and_getTrace()
    plotTrace(x, y, channel_nums, fname=fname)
    saveTrace(fname+ext, x, y, fileheader=id+"time,"+str(channel_nums)+"\n")
