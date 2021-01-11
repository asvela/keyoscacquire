# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from Keysight oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

This program consists of a loop in which the program connects to the oscilloscope,
a trace from the active channels are captured and stored for each loop. This permits
the active channels to be changing thoughout the measurements, but has larger
overhead due to establishing and closing a new connection every time.

The loop runs each time 'enter' is hit. Alternatively one can input n-1 characters before hitting
'enter' to capture n traces back to back. To quit press 'q'+'enter'.

Optional argument from the command line: string setting the base filename of the output files.
Change _visa_address in keyoscacquire.config to the desired instrument's address.

"""

import sys
import argparse

import keyoscacquire.programmes as programmes
import keyoscacquire.config as config

##============================================================================##
##                   INSTALLED COMMAND LINE PROGRAMMES                        ##
##============================================================================##

# Help strings
acq_help = f"The acquire type: {{HRESolution, NORMal, AVER<m>}} where <m> is the number of averages in range [2, 65536]. Defaults to '{config._acq_type}'."
wav_help = f"The waveform format: {{BYTE, WORD, ASCii}}. \nDefaults to '{config._waveform_format}'."
file_help = f"The filename base, (without extension, '{config._filetype}' is added). Defaults to '{config._filename}'."
visa_help = f"Visa address of instrument. To find the visa addresses of the instruments connected to the computer run 'list_visa_devices' in the command line. Defaults to '{config._visa_address}'."
timeout_help = f"Milliseconds before timeout on the channel to the instrument. Defaults to {config._timeout}."
channels_help = f"List of the channel numbers to be acquired, for example '1 3' (without ') or 'active' (without ') to capture all the currently active channels on the oscilloscope. Defaults to the currently active channels."
points_help = f"Use 0 to get the maximum number of points, or set a specific number (the scope might change it slightly). Defaults to '{config._num_points}."
delim_help = f"Delimiter used between filename and filenumber (before filetype). Defaults to '{config._file_delimiter}'."


def standard_arguments(parser):
    connection_gr = parser.add_argument_group('Connection settings')
    connection_gr.add_argument('-v', '--visa_address',
                               nargs='?', default=config._visa_address, help=visa_help)
    connection_gr.add_argument('-t', '--timeout',
                               nargs='?', type=int, default=config._timeout, help=timeout_help)
    acquire_gr = parser.add_argument_group('Acquisition settings')
    acquire_gr.add_argument('-c', '--channels',
                            nargs='*', type=int, default=None, help=channels_help)
    acquire_gr.add_argument('-a', '--acq_type',
                            nargs='?',default=None, help=acq_help)
    trans_gr = parser.add_argument_group('Transfer and storage settings')
    trans_gr.add_argument('-w', '--wav_format',
                          nargs='?', default=config._waveform_format, help=wav_help)
    trans_gr.add_argument('-p', '--num_points',
                          nargs='?', type=int, default=config._num_points,  help=points_help)
    trans_gr.add_argument('-f', '--filename',
                          nargs='?', default=config._filename, help=file_help)
    return trans_gr


def connect_each_time_cli():
    """Function installed on the command line: Obtains and stores multiple traces,
    connecting to the oscilloscope each time."""
    parser = argparse.ArgumentParser(description=programmes.get_traces_connect_each_time_loop.__doc__)
    trans_gr = standard_arguments(parser)
    trans_gr.add_argument('--file_delimiter', nargs='?', help=delim_help, default=config._file_delimiter)
    args = parser.parse_args()
    # Convert channels arg to ints
    if args.channels is not None:
        args.channels = [int(c) for c in args.channels]
    programmes.get_traces_connect_each_time_loop(fname=args.filename,
                                                 address=args.visa_address,
                                                 timeout=args.timeout,
                                                 wav_format=args.wav_format,
                                                 channels=args.channels,
                                                 acq_type=args.acq_type,
                                                 num_points=args.num_points,
                                                 file_delim=args.file_delimiter)


def single_connection_cli():
    """Function installed on the command line: Obtains and stores multiple traces,
    keeping a the same connection to the oscilloscope open all the time."""
    parser = argparse.ArgumentParser(description=programmes.get_traces_single_connection_loop.__doc__)
    trans_gr = standard_arguments(parser)
    trans_gr.add_argument('--file_delimiter', nargs='?', help=delim_help, default=config._file_delimiter)
    args = parser.parse_args()
    # Convert channels arg to ints
    if args.channels is not None:
        args.channels = [int(c) for c in args.channels]
    programmes.get_traces_single_connection_loop(fname=args.filename,
                                                 address=args.visa_address,
                                                 timeout=args.timeout,
                                                 wav_format=args.wav_format,
                                                 channels=args.channels,
                                                 acq_type=args.acq_type,
                                                 num_points=args.num_points,
                                                 file_delim=args.file_delimiter)


def single_trace_cli():
    """Function installed on the command line: Obtains and stores a single trace."""
    parser = argparse.ArgumentParser(description=programmes.get_single_trace.__doc__)
    standard_arguments(parser)
    args = parser.parse_args()
    # Convert channels arg to ints
    if args.channels is not None:
        args.channels = [int(c) for c in args.channels]
    programmes.get_single_trace(fname=args.filename,
                                address=args.visa_address,
                                timeout=args.timeout,
                                wav_format=args.wav_format,
                                channels=args.channels,
                                acq_type=args.acq_type,
                                num_points=args.num_points)


def num_traces_cli():
    """Function installed on the command line: Obtains and stores a single trace."""
    parser = argparse.ArgumentParser(description=programmes.get_num_traces.__doc__)
    # postitional arg
    parser.add_argument('num', help='The number of successive traces to obtain.', type=int)
    # optional args
    trans_gr = standard_arguments(parser)
    trans_gr.add_argument('--file_delimiter', nargs='?', help=delim_help, default=config._file_delimiter)
    args = parser.parse_args()
    # Convert channels arg to ints
    if args.channels is not None:
        args.channels = [int(c) for c in args.channels]
    programmes.get_num_traces(num=args.num,
                              fname=args.filename,
                              address=args.visa_address,
                              timeout=args.timeout,
                              wav_format=args.wav_format,
                              channels=args.channels,
                              acq_type=args.acq_type,
                              num_points=args.num_points)


def list_visa_devices_cli():
    """Function installed on the command line: Lists VISA devices"""
    parser = argparse.ArgumentParser(description=programmes.list_visa_devices.__doc__)
    parser.add_argument('-n', action="store_false",
                        help=("If this flag is set, the programme will not query "
                              "the instruments for their IDNs."))
    args = parser.parse_args()
    programmes.list_visa_devices(ask_idn=args.n)


def path_of_config_cli():
    """Function installed on the command line: Prints the full path of the config module"""
    parser = argparse.ArgumentParser(description=programmes.path_of_config.__doc__)
    args = parser.parse_args()
    programmes.path_of_config()
