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

import sys, argparse
import keysightoscacquire.programmes as acqprog


##============================================================================##
##                   INSTALLED COMMAND LINE FUNCTIONS                         ##
##============================================================================##

def connect_each_time_command_line():
    """When the installed function is called from the command line"""
    parser = argparse.ArgumentParser(usage=acqprog.getTraces_connect_each_time_loop.__doc__)
    parser.add_argument('-f', nargs='?', help='Specify filename base')
    parser.add_argument('-a', nargs='?', help='Specify acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [1, 65536]')
    args = parser.parse_args()

    print(args)

    acqprog.run_programme("connect_each_time", ['', args.f, args.a])


def single_connection_command_line():
    """When the installed function is called from the command line"""
    parser = argparse.ArgumentParser(usage=acqprog.getTraces_single_connection_loop.__doc__)
    parser.add_argument('-f', nargs='?', help='Specify filename base')
    parser.add_argument('-a', nargs='?', help='Specify acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [1, 65536]')
    args = parser.parse_args()

    acqprog.run_programme("single_connection", ['', args.f, args.a])
