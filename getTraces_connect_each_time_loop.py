# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from (Keysight) oscilloscopes using pyVISA.
Traces are stored as .csv files and will by default be accompanied by a .png too.

This program consists of a loop in which the program connects to the oscilloscope,
a trace from the active channels are captured and stored for each loop. This permits
the active channels to be changing thoughout the measurements, but has larger
overhead due to establishing and closing a new connection every time.

The loop runs each time 'enter' is hit. Alternatively one can input n-1 characters before hitting
'enter' to capture n traces back to back. To quit press 'q'+'enter'.

Optional argument from the command line: string setting the base filename of the output files.
Change the VISA_ADDRESS under default options to the desired instrument.

Tested with Keysight DSOX2024A.
See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import sys
import acquire as acq

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

def getTraces_connect_each_time_loop(fname, ext, instrument=VISA_ADDRESS, timeout=TIMEOUT, wav_format=WAVEFORM_FORMAT,
                                     channel_nums=CH_NUMS, source_type='CHANnel', acq_type='HRESolution',
                                     num_averages=2, p_mode='RAW', num_points=0, start_num=0):
    n = start_num
    fname = acq.check_file(fname, ext, num=str(n)) # check that file does not exist from before, append to name if it does
    print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
    print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
    while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
        x, y, id, channels = acq.connect_and_getTrace(channel_nums, source_type, instrument, timeout, wav_format, acq_type, num_averages, p_mode, num_points)
        acq.plotTrace(x, y, channels, fname=fname+str(n))
        channelstring = ", ".join([channel for channel in channels]) # make string of sources
        acq.saveTrace(fname+str(n)+ext, x, y, fileheader=id+"time,"+channelstring+"\n")
        n += 1
    print("Quit")

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    if len(sys.argv) == 2: #if optional argument is supplied on the command line
        fname = sys.argv[1] # use this as the filename base
    else:
        fname = DEFAULT_FILENAME
    ext = FILETYPE
    getTraces_connect_each_time_loop(fname, ext)
