#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from (Keysight) oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

This program connects to the oscilloscope, sets options for the acquisition and then
enters a loop in which the program captures and stores traces each time 'enter' is pressed.
Alternatively one can input n-1 characters before hitting 'enter' to capture n traces
back to back. To quit press 'q'+'enter'. This programme minimises overhead for each measurement,
permitting measurements to be taken with quicker succession than if connecting each time
a trace is captured. The downside is that which channels are being captured cannot be
changing thoughout the measurements.

1st optional argument from the command line: string setting the base filename of the output files.
2nd optional arg: acquire type {HRESolution, NORMal, AVER<m>} where <m> is the number of averages [1, 65536]

Change the VISA_ADDRESS under default options to the desired instrument.


Tested with Keysight DSOX2024A.
See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import sys
import keyoscacquire.programmes as acq


##============================================================================##
##                           MAIN FUNCTION                                    ##
##============================================================================##

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    acq.run_programme("single_connection", sys.argv)
