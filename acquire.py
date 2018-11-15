# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from oscilloscopes using pyVISA.
Traces are stored as .csv files and will by default be accompanied by a .png too.

This script can be called resulting in one trace being captured and stored.
Optional argument from the command line: string setting the base filename of the output files.
Change the VISA_ADDRESS under default options to the desired instrument.

Tested with Keysight DSOX2024A.
See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import sys  # required for reading user input and command line arguments
import visa # instrument communication
import numpy as np, matplotlib.pyplot as plt
import time, datetime # for measuring elapsed time and adding current date and time to exported files

# Default options
VISA_ADDRESS = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
DEFAULT_FILENAME = "data" # default base filename of all traces and pngs exported, a number is appended to the base
FILETYPE = ".csv"   # filetype of exported data, can also be txt/dat etc.
EXPORT_PNG = True   # export png of plot of obtained trace
SHOW_PLOT = False   # show each plot when generated (program pauses until it is closed)
TIMEOUT = 15000     #ms timeout for the instrument connection

def initialise(instrument, timeout, acq_type='HRESolution', num_averages=2, p_mode='RAW', num_points=0):
    """
    Open a connection to instrument and choose settings for the connection and acquisition.
    Some alternative settings are listed.
    instrument = {'USB0::2391::6038::MY57233636::INSTR' | 'TCPIP0::192.168.20.30::4000::SOCKET'}
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
        print('Couldn\'t connect to \'%s\', exiting now...' % instrument)
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
    if acq_type == 'NORMal': # averaging only applies for the NORMal mode
        inst.write(':ACQuire:COUNt ' + str(num_averages))

    ## Set options for waveform export
    inst.write(':WAVeform:FORMat BYTE') # values are transferred
    inst.write(':WAVeform:POINts:MODE ' + p_mode)
    #print("Max number of points for mode %s: %s" % (p_mode, inst.query(':WAVeform:POINts? MAXimum')))
    if num_points != 0: #if number of points has been specified
        inst.write(':WAVeform:POINts ' + str(num_points))
        print("Number of points set to: ", num_points)
    return inst, id

def capture_and_read(inst, sources, sourcesstring):
    ## Capture data
    print("Start acquisition..")
    start_time = time.time() # time the acquiring process
    inst.write(':DIGitize ' + sourcesstring) # DIGitize is a specialized RUN command.
                                             # Waveforms are acquired according to the settings of the :ACQuire commands.
                                             # When acquisition is complete, the instrument is stopped.
    ## Read out data
    raw = [] # initialise array for storing data
    for source in sources: # loop through all the sources
        inst.write(':WAVeform:SOURce ' + source) # selects the channel for which the succeeding WAVeform commands applies to
        try:
            raw.append(inst.query(':WAVeform:DATA?')) # read out data for this source
        except visa.Error as ex:
            print("Failed to obtain waveform, have you checked that the TIMEOUT is sufficently long? Currently %d ms" % TIMEOUT)
            sys.exit()
    end_time = time.time()
    print("Elapsed time:", end_time-start_time)
    measurement_time = float(inst.query(':TIMebase:RANGe?')) # returns the current full-scale range value for the main window

    return raw, measurement_time

def process_data(raw, measurement_time):
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

def connect_and_getTrace(channel_nums=[''], source_type='CHANnel', instrument=VISA_ADDRESS,  timeout=TIMEOUT, acq_type='HRESolution', num_averages=2, p_mode='RAW', num_points=0):
    """
    Get trace from channels of instrument. Returns one numpy array of the x time values and one numpy array of y values.
    Some alternative settings are listed.
    channelnum = list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
    source_type = {'CHANnel' | 'MATH' | 'FUNCtion'}: MATH is an alias for FUNCtion
    instrument = {'USB0::2391::6038::MY57233636::INSTR' | 'TCPIP0::192.168.20.30::4000::SOCKET'}
    acq_type = {'HRESolution' | 'NORMal'}
    num_averages = 2 to 65536: applies only to the NORMal mode
    p_mode = {'RAW' | 'MAXimum'}: RAW gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
    num_points = {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000
                 | 50000 | 100000 | 200000 | 500000 | 1000000}: optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.
    """

    ## Initialise
    inst, id = initialise(instrument, timeout, acq_type, num_averages, p_mode, num_points)

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
    raw, measurement_time = capture_and_read(inst, sources, sourcesstring)
    x, y = process_data(raw, measurement_time)

    # Set the oscilloscope running before closing the connection
    inst.write(':RUN')
    inst.close()
    return x, y, id, channel_nums

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


## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    if len(sys.argv) == 2: #if optional argument is supplied on the command line
        fname = sys.argv[1] # use this as the filename base
    else:
        fname = DEFAULT_FILENAME
    ext = FILETYPE
    x, y, id, channel_nums = connect_and_getTrace()
    plotTrace(x, y, channel_nums, fname=fname)
    saveTrace(fname+ext, x, y, fileheader=id+"time,"+str(channel_nums)+"\n")
