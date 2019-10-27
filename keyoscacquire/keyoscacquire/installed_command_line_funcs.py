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

Andreas Svela // 2019
"""

import sys, argparse
import keyoscacquire.programmes as acqprog
import keyoscacquire.config as config

##============================================================================##
##                   INSTALLED COMMAND LINE FUNCTIONS                         ##
##============================================================================##

# Help strings
acq_help = "The acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536]. Defaults to \'"+config._acq_type+"\'."
wav_help = "The waveform format: {BYTE, WORD, ASCii}. \nDefaults to \'"+config._waveform_format+"\'."
file_help = "The filename base, (without extension, \'"+config._filetype+"\' is added). Defaults to \'"+config._filename+"\'."
visa_help = "Visa address of instrument. To find the visa addresses of the instruments connected to the computer run 'list_visa_devices' in the command line. Defaults to \'"+config._visa_address+"\'."
timeout_help = "Milliseconds before timeout on the channel to the instrument. Defaults to "+str(config._timeout)+"."
channels_help = "List of the channel numbers to be acquired, for example '1 3' (without '). Use an empty string ('') to capture all the currently active channels on the oscilloscope. Defaults to \'"+" ".join(config._ch_nums)+"\'."
points_help = "Use 0 to get the maximum number of points, or set a smaller number to speed up the acquisition and transfer. Defaults to 0."
delim_help = "Delimiter used between filename and filenumber (before filetype). Defaults to \'"+config._file_delimiter+"\'."

def connect_each_time_command_line():
    """Function installed on the command line: Obtains and stores multiple traces,
    connecting to the oscilloscope each time."""
    parser = argparse.ArgumentParser(description=acqprog.getTraces_connect_each_time_loop.__doc__)
    connection_gr = parser.add_argument_group('Connection settings')
    connection_gr.add_argument('-v', '--visa_address', nargs='?', help=visa_help, default=config._visa_address)
    connection_gr.add_argument('-t', '--timeout', nargs='?', help=timeout_help, default=config._timeout, type=int)
    acquire_gr = parser.add_argument_group('Acquiring settings')
    acquire_gr.add_argument('-c', '--channels', nargs='*', help=channels_help, default=config._ch_nums)
    acquire_gr.add_argument('-a', '--acq_type', nargs='?', help=acq_help, default=config._acq_type)
    trans_gr = parser.add_argument_group('Transfer and storage settings')
    trans_gr.add_argument('-w', '--wav_format', nargs='?', help=wav_help, default=config._waveform_format)
    trans_gr.add_argument('-p', '--num_points', nargs='?', help=points_help, default=0, type=int)
    trans_gr.add_argument('-f', '--filename', nargs='?', help=file_help, default=config._filename)
    trans_gr.add_argument('--file_delimiter', nargs='?', help=delim_help, default=config._file_delimiter)
    args = parser.parse_args()

    acqprog.getTraces_connect_each_time_loop(fname=args.filename, address=args.visa_address, timeout=args.timeout, wav_format=args.wav_format,
                             channel_nums=args.channels, acq_type=args.acq_type, num_points=args.num_points, file_delim=args.file_delimiter)


def single_connection_command_line():
    """Function installed on the command line: Obtains and stores multiple traces,
    keeping a the same connection to the oscilloscope open all the time."""
    parser = argparse.ArgumentParser(description=acqprog.get_traces_single_connection_loop.__doc__)
    connection_gr = parser.add_argument_group('Connection settings')
    connection_gr.add_argument('-v', '--visa_address', nargs='?', help=visa_help, default=config._visa_address)
    connection_gr.add_argument('-t', '--timeout', nargs='?', help=timeout_help, default=config._timeout, type=int)
    acquire_gr = parser.add_argument_group('Acquiring settings')
    acquire_gr.add_argument('-c', '--channels', nargs='*', help=channels_help, default=config._ch_nums)
    acquire_gr.add_argument('-a', '--acq_type', nargs='?', help=acq_help, default=config._acq_type)
    trans_gr = parser.add_argument_group('Transfer and storage settings')
    trans_gr.add_argument('-w', '--wav_format', nargs='?', help=wav_help, default=config._waveform_format)
    trans_gr.add_argument('-p', '--num_points', nargs='?', help=points_help, default=0, type=int)
    trans_gr.add_argument('-f', '--filename', nargs='?', help=file_help, default=config._filename)
    trans_gr.add_argument('--file_delimiter', nargs='?', help=delim_help, default=config._file_delimiter)
    args = parser.parse_args()

    acqprog.getTraces_single_connection_loop(fname=args.filename, address=args.visa_address, timeout=args.timeout, wav_format=args.wav_format,
                             channel_nums=args.channels, acq_type=args.acq_type, num_points=args.num_points, file_delim=args.file_delimiter)


def single_trace_command_line():
    """Function installed on the command line: Obtains and stores a single trace."""
    parser = argparse.ArgumentParser(description=acqprog.get_single_trace.__doc__)
    connection_gr = parser.add_argument_group('Connection settings')
    connection_gr.add_argument('-v', '--visa_address', nargs='?', help=visa_help, default=config._visa_address)
    connection_gr.add_argument('-t', '--timeout', nargs='?', help=timeout_help, default=config._timeout, type=int)
    acquire_gr = parser.add_argument_group('Acquiring settings')
    acquire_gr.add_argument('-c', '--channels', nargs='*', help=channels_help, default=config._ch_nums)
    acquire_gr.add_argument('-a', '--acq_type', nargs='?', help=acq_help, default=config._acq_type)
    trans_gr = parser.add_argument_group('Transfer and storage settings')
    trans_gr.add_argument('-w', '--wav_format', nargs='?', help=wav_help, default=config._waveform_format)
    trans_gr.add_argument('-p', '--num_points', nargs='?', help=points_help, default=0, type=int)
    trans_gr.add_argument('-f', '--filename', nargs='?', help=file_help, default=config._filename)
    args = parser.parse_args()

    acqprog.get_single_trace(fname=args.filename, address=args.visa_address, timeout=args.timeout, wav_format=args.wav_format,
                             channel_nums=args.channels, acq_type=args.acq_type, num_points=args.num_points)

def num_traces_command_line():
    """Function installed on the command line: Obtains and stores a single trace."""
    parser = argparse.ArgumentParser(description=acqprog.get_num_traces.__doc__)
    # postitional arg
    parser.add_argument('num', help='The number of successive traces to obtain.', type=int)
    # optional args
    connection_gr = parser.add_argument_group('Connection settings')
    connection_gr.add_argument('-v', '--visa_address', nargs='?', help=visa_help, default=config._visa_address)
    connection_gr.add_argument('-t', '--timeout', nargs='?', help=timeout_help, default=config._timeout, type=int)
    acquire_gr = parser.add_argument_group('Acquiring settings')
    acquire_gr.add_argument('-c', '--channels', nargs='*', help=channels_help, default=config._ch_nums)
    acquire_gr.add_argument('-a', '--acq_type', nargs='?', help=acq_help, default=config._acq_type)
    trans_gr = parser.add_argument_group('Transfer and storage settings')
    trans_gr.add_argument('-w', '--wav_format', nargs='?', help=wav_help, default=config._waveform_format)
    trans_gr.add_argument('-p', '--num_points', nargs='?', help=points_help, default=0, type=int)
    trans_gr.add_argument('-f', '--filename', nargs='?', help=file_help, default=config._filename)
    trans_gr.add_argument('--file_delimiter', nargs='?', help=delim_help, default=config._file_delimiter)
    args = parser.parse_args()

    acqprog.get_num_traces(num=args.num, fname=args.filename, address=args.visa_address, timeout=args.timeout, wav_format=args.wav_format,
                             channel_nums=args.channels, acq_type=args.acq_type, num_points=args.num_points)

def list_visa_devices_command_line():
    """Function installed on the command line: Lists VISA devices"""
    parser = argparse.ArgumentParser(description=acqprog.list_visa_devices.__doc__)
    args = parser.parse_args()
    acqprog.list_visa_devices()

def path_of_config_command_line():
    """Function installed on the command line: Prints the full path of the config module"""
    parser = argparse.ArgumentParser(description=acqprog.path_of_config.__doc__)
    args = parser.parse_args()
    acqprog.path_of_config()
