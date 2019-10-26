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
Change the _visa_address under in config to the desired instrument.

Andreas Svela // 2019
"""

import sys, argparse
import keyoscacquire.programmes as acqprog
import keyoscacquire.config as config

##============================================================================##
##                   INSTALLED COMMAND LINE PROGRAMMES                        ##
##============================================================================##

# Help strings
acq_help = 'The acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536]. Defaults to \''+config._acq_type+"\'."
file_help = 'The filename base, (without extension, \''+config._filetype+'\' is added). Defaults to \''+config._filename+"\'."


def connect_each_time_command_line():
    """Function installed on the command line: Obtains and stores multiple traces,
    connecting to the oscilloscope each time."""
    parser = argparse.ArgumentParser(usage=acqprog.get_traces_connect_each_time_loop.__doc__)
    parser.add_argument('-f', nargs='?', help=file_help)
    parser.add_argument('-a', nargs='?', help=acq_help)
    args = parser.parse_args()

    acqprog.run_programme("connect_each_time", ['', args.f, args.a])


def single_connection_command_line():
    """Function installed on the command line: Obtains and stores multiple traces,
    keeping a the same connection to the oscilloscope open all the time."""
    parser = argparse.ArgumentParser(usage=acqprog.get_traces_single_connection_loop.__doc__)
    parser.add_argument('-f', nargs='?', help=file_help)
    parser.add_argument('-a', nargs='?', help=acq_help)
    args = parser.parse_args()

    acqprog.run_programme("single_connection", ['', args.f, args.a])


def single_trace_command_line():
    """Function installed on the command line: Obtains and stores a single trace."""
    parser = argparse.ArgumentParser(usage=acqprog.get_single_trace.__doc__)
    parser.add_argument('-f', nargs='?', help=file_help)
    parser.add_argument('-a', nargs='?', help=acq_help)
    args = parser.parse_args()

    acqprog.run_programme("single_trace", ['', args.f, args.a])

def num_traces_command_line():
    """Function installed on the command line: Obtains and stores a single trace."""
    parser = argparse.ArgumentParser(usage=acqprog.get_num_traces.__doc__)
    parser.add_argument('-n', nargs='?', help='The number of traces to obtain. Defaults to 1.')
    parser.add_argument('-f', nargs='?', help=file_help)
    parser.add_argument('-a', nargs='?', help=acq_help)
    args = parser.parse_args()

    acqprog.run_programme("num_traces", ['', args.f, args.a, args.n])

def list_visa_devices_command_line():
    """Function installed on the command line: Lists VISA devices"""
    parser = argparse.ArgumentParser(usage=acqprog.list_visa_devices.__doc__)
    args = parser.parse_args()
    acqprog.list_visa_devices()

def path_of_config_command_line():
    """Function installed on the command line: Prints the full path of the config module"""
    parser = argparse.ArgumentParser(usage=acqprog.path_of_config.__doc__)
    args = parser.parse_args()
    acqprog.path_of_config()
