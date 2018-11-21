# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from (Keysight) oscilloscopes using pyVISA.
Traces are stored as .csv files and will by default be accompanied by a .png too.

This program connects to the oscilloscope, sets options for the acquisition and then
enters a loop in which the program captures and stores traces each time 'enter' is pressed.
Alternatively one can input n-1 characters before hitting 'enter' to capture n traces
back to back. To quit press 'q'+'enter'. This programme minimises overhead for each measurement,
permitting measurements to be taken with quicker succession than if connecting each time
a trace is captured. The downside is that which channels are being captured cannot be
changing thoughout the measurements.

Optional argument from the command line: string setting the base filename of the output files.
Change the VISA_ADDRESS under default options to the desired instrument.

Tested with Keysight DSOX2024A.
See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import sys
import acquire as acq
import numpy as np

# Default options
VISA_ADDRESS = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
WAVEFORM_FORMAT = 'WORD'    # WORD formatted data is transferred as 16-bit uint.
                            # BYTE formatted data is transferred as 8-bit uint.
                            # ASCii formatted data converts the internal integer data values to real Y-axis values.
                            #       Values are transferred as ASCii digits in floating point notation, separated by commas.
CH_NUMS=['']        # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
DEFAULT_FILENAME = "data" # default base filename of all traces and pngs exported, a number is appended to the base
FILETYPE = ".csv"   # filetype of exported data, can also be txt/dat etc.
TIMEOUT = 15000     #ms timeout for the instrument connection

def getTraces_single_connection_loop(fname, ext, instrument=VISA_ADDRESS, timeout=TIMEOUT, wav_format=WAVEFORM_FORMAT,
                                     channel_nums=CH_NUMS, source_type='CHANnel', acq_type='HRESolution',
                                     num_averages=2, p_mode='RAW', num_points=0, start_num=0):
    ## Initialise
    inst, id = acq.initialise(instrument, timeout, wav_format, acq_type, num_averages, p_mode, num_points)

    ## Select sources
    if channel_nums == ['']: # if no channels specified, find the channels currently active and acquire from those
        channels = np.array(['1', '2', '3', '4'])
        displayed_channels = [inst.query(':CHANnel'+channel+':DISPlay?')[0] for channel in channels] # querying DISP for each channel to determine which channels are currently displayed
        channel_mask = np.array([bool(int(i)) for i in displayed_channels]) # get a mask of bools for the channels that are on [need the int() as int('0') = True]
        channel_nums = channels[channel_mask] # apply mask to the channel list
    sources = [source_type+channel for channel in channel_nums] # build list of sources
    sourcesstring = ", ".join([source_type+channel for channel in channel_nums]) # make string of sources

    n = start_num
    fname = acq.check_file(fname, ext, num=str(n)) # check that file does not exist from before, append to name if it does
    print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
    print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
    print("Acquire from sources", sourcesstring)
    while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
        raw, metadata = acq.capture_and_read(inst, sources, sourcesstring, wav_format)
        x, y = acq.process_data(raw, metadata, wav_format) # capture, read and process data
        acq.plotTrace(x, y, channel_nums, fname=fname+str(n))                    # plot trace and save png
        acq.saveTrace(fname+str(n)+ext, x, y, fileheader=id+"time,"+sourcesstring+"\n") # save trace to ext file
        n += 1

    print("Quit")
    # Set the oscilloscope running before closing the connection
    inst.write(':RUN')
    inst.close()

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    if len(sys.argv) == 2: #if optional argument is supplied on the command line
        fname = sys.argv[1] # use this as the filename base
    else:
        fname = DEFAULT_FILENAME
    ext = FILETYPE
    getTraces_single_connection_loop(fname, ext)
