#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from (Keysight) oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

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
import keysightoscacq as acq

# Default options
VISA_ADDRESS = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
WAVEFORM_FORMAT = 'WORD'        # WORD formatted data is transferred as 16-bit uint.
                                # BYTE formatted data is transferred as 8-bit uint.
                                # ASCii formatted data converts the internal integer data values to real Y-axis values.
                                #       Values are transferred as ASCii digits in floating point notation, separated by commas.
CH_NUMS = ['']                  # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
DEFAULT_ACQ_TYPE = "HRESolution"# {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [1, 65536]
DEFAULT_NUM_AVG = 2             # default number of averages used if only AVER is given as acquisition type
DEFAULT_FILENAME = "data"       # default base filename of all traces and pngs exported, a number is appended to the base
FILETYPE = ".csv"   # filetype of exported data, can also be txt/dat etc.
TIMEOUT = 15000     #ms timeout for the instrument connection

def getTraces_connect_each_time_loop(fname, ext, instrument=VISA_ADDRESS, timeout=TIMEOUT, wav_format=WAVEFORM_FORMAT,
                                     channel_nums=CH_NUMS, source_type='CHANnel', acq_type='HRESolution',
                                     num_averages=2, p_mode='RAW', num_points=0, start_num=0, file_delim=" f"):
    n = start_num
    fnum = file_delim+str(n)
    fname = acq.check_file(fname, ext, num=fnum) # check that file does not exist from before, append to name if it does
    print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
    print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
    while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
        fnum = file_delim+str(n)
        x, y, id, channels = acq.connect_and_getTrace(channel_nums, source_type, instrument, timeout, wav_format, acq_type, num_averages, p_mode, num_points)
        acq.plotTrace(x, y, channels, fname=fname+fnum)
        channelstring = ", ".join([channel for channel in channels]) # make string of sources
        acq.saveTrace(fname+fnum+ext, x, y, fileheader=id+"time,"+channelstring+"\n")
        n += 1
    print("Quit")


##============================================================================##
##                           MAIN FUNCTION                                    ##
##============================================================================##

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    fname = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_FILENAME #if optional argument is supplied on the command line use as base filename
    ext = FILETYPE
    a_type = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_ACQ_TYPE #if 2nd optional argument is supplied on the command line use acquiring mode
    if a_type[:4] == 'AVER':
        try:
            num_avg = int(a_type[4:]) if len(a_type)>4 else DEFAULT_NUM_AVG # if the type is longer than four characters, treat characters from fifth to end as number of averages
        except ValueError:
            print("\nValueError: Failed to convert \'%s\' to an integer, check that acquisition type is on the form AVER or AVER<m> where <m> is an integer (currently acq. type is \'%s\').\nExiting..\n" % (a_type[4:], a_type))
            sys.exit()
        if num_avg < 1 or num_avg > 65536: #check that num_avg is within acceptable range
            raise ValueError("\nValueError: The number of averages {} is out of range.\nExiting..\n".format(num_avg))
            sys.exit()
        fname += " " + a_type
    else:
        num_avg = DEFAULT_NUM_AVG # not relevant unless AVERage
    getTraces_connect_each_time_loop(fname, ext, acq_type=a_type, num_averages=num_avg)
