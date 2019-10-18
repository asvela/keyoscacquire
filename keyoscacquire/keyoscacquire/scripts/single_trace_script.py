# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from Keysight oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

This program captures a single trace and stores it.

Optional argument from the command line: string setting the base filename of the output files.
Change the config._visa_address under default options to the desired instrument.

Tested with Keysight DSOX2024A.
See Keysight's Programmer's Guide for reference.

Andreas Svela 2018
"""

import sys
import keyoscacquire.programmes as acq


##============================================================================##
##                         MAIN FUNCTION                                    ##
##============================================================================##

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    acq.run_programme("single_trace", sys.argv)
