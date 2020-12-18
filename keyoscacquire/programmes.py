# -*- coding: utf-8 -*-
"""
Python backend for installed command line programmes. These can also be integrated in python scripts or used as examples.

    * :func:`list_visa_devices`: listing visa devices
    * :func:`path_of_config`: finding path of config.py
    * :func:`get_single_trace`: taking a single trace and saving it to csv and png
    * :func:`get_traces_single_connection_loop` :func:`get_traces_connect_each_time_loop`: two programmes for taking multiple traces when a key is pressed, see descriptions for difference
    * :func:`get_num_traces`: get a specific number of traces

"""

import os
import sys
import pyvisa
import logging; _log = logging.getLogger(__name__)
import keyoscacquire.oscacq as acq
import numpy as np
from tqdm import tqdm

# local file with default options:
import keyoscacquire.config as config
import keyoscacquire.config as auxiliary


def list_visa_devices(ask_idn=True):
    """Prints a list of the VISA instruments connected to the computer,
    including their addresses."""
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    if len(resources) == 0:
        print("\nNo VISA devices found!")
    else:
        print(f"\nFound {len(resources)} resources. Now obtaining information about them..")
        information, could_not_connect = [], []
        # Loop through resources to learn more about them
        for i, address in enumerate(resources):
            current_resource_info = []
            info_object = rm.resource_info(address)
            alias = info_object.alias if info_object.alias is not None else "N/A"
            current_resource_info.extend((str(i), address, alias))
            if ask_idn:
                # Open the instrument and get the identity string
                try:
                    error_flag = False
                    instrument = rm.open_resource(address)
                    id = instrument.query("*IDN?").strip()
                    instrument.close()
                except pyvisa.Error as e:
                    error_flag = True
                    could_not_connect.append(i)
                    current_resource_info.extend(["no IDN response"]*5)
                    print(f"Instrument #{i}: Did not respond to *IDN?: {e}")
                except Exception as ex:
                    error_flag = True
                    print(f"Instrument #{i}: Got exception {ex.__class__.__name__} "
                          f"when asking for its identity.")
                    could_not_connect.append(i)
                    current_resource_info.extend(["Error"]*5)
                if not error_flag:
                    try:
                        current_resource_info.extend(auxiliary.interpret_visa_id(id))
                    except Exception as ex:
                        print(f"Instrument #{i}: Could not interpret VISA id, got"
                              f"exception {ex.__class__.__name__}: VISA id returned was '{id}'")
                        could_not_connect.append(i)
                        current_resource_info.extend(["failed to interpret"]*5)
            information.append(current_resource_info)
        if ask_idn:
            # transpose to lists of property
            nums, addrs, aliases, makers, models, serials, firmwares, model_series = (list(category) for category in zip(*information))
            # select what properties to list
            selection = (nums, addrs, makers, models, firmware, aliases)
            # name columns
            header_fields = (' #', 'address', 'maker', 'model', 'firmware', 'alias')
            row_format = "{:>{p[0]}s}  {:{p[1]}s}  {:{p[2]}s}  {:{p[3]}s}  {:{p[4]}s}  {:{p[5]}s}"
        else:
            selection = [list(category) for category in zip(*information)]
            header_fields = (' #', 'address', 'alias')
            row_format = "{:>{p[0]}s}  {:{p[1]}s}  {:{p[2]}s}"
        # find max number of characters for each property to use as padding
        padding = [max([len(instance) for instance in property]) for property in selection]
        # make sure the padding is not smaller than the header field length
        padding = [max(pad, len(field)) for pad, field in zip(padding, header_fields)]
        header = row_format.format(*header_fields, p=padding)
        # print the table
        print("\nVISA devices connected:")
        print(header)
        print("="*(len(header)+2))
        for info in zip(*selection):
            print(row_format.format(*info, p=padding))


def path_of_config():
    """Print the absolute path of the config.py file."""
    print("config.py can be found in:")
    print(f"   {os.path.dirname(os.path.abspath(__file__))}\n")


def get_single_trace(fname=config._filename, ext=config._filetype, address=config._visa_address,
                     timeout=config._timeout, wav_format=config._waveform_format,
                     channels=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                     num_averages=config._num_avg, p_mode='RAW', num_points=0):
    """This programme captures and stores a single trace."""
    with acq.Oscilloscope(address=address, timeout=timeout) as scope:
        scope.set_options_get_trace_save(fname=fname, ext=ext, wav_format=wav_format,
                              channels=channels, source_type=source_type, acq_type=acq_type,
                              num_averages=num_averages, p_mode=p_mode, num_points=num_points)
    print("Done")


def get_traces_connect_each_time_loop(fname=config._filename, ext=config._filetype, address=config._visa_address,
                                      timeout=config._timeout, wav_format=config._waveform_format,
                                      channels=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                                      num_averages=config._num_avg, p_mode='RAW', num_points=0, start_num=0, file_delim=config._file_delimiter):
    """This program consists of a loop in which the program connects to the oscilloscope,
    a trace from the active channels are captured and stored for each loop.

    This permits the active channels to be changing thoughout the measurements, but has larger
    overhead due to establishing and closing a new connection every time.

    The loop runs each time 'enter' is hit. Alternatively one can input n-1 characters before hitting
    'enter' to capture n traces back to back. To quit press 'q'+'enter'.
    """
    # Check that file does not exist from before, append to name if it does
    n = start_num
    fname = auxiliary.check_file(fname, ext, num=f"{file_delim}{n}")
    print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
    print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
    while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
        fnum = f"{file_delim}{n}"
        with acq.Oscilloscope(address=address, timeout=timeout) as scope:
            scope.ext = ext
            scope.set_options_get_trace(wav_format=wav_format,
                                  channels=channels, source_type=source_type, acq_type=acq_type,
                                  num_averages=num_averages, p_mode=p_mode, num_points=num_points)
            scope.save_trace(fname+fnum)
        n += 1
    print("Quit")


def get_traces_single_connection_loop(fname=config._filename, ext=config._filetype, address=config._visa_address,
                                      timeout=config._timeout, wav_format=config._waveform_format,
                                      channels=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                                      num_averages=config._num_avg, p_mode='RAW', num_points=0, start_num=0, file_delim=config._file_delimiter):
    """This program connects to the oscilloscope, sets options for the acquisition and then
    enters a loop in which the program captures and stores traces each time 'enter' is pressed.

    Alternatively one can input n-1 characters before hitting 'enter' to capture n traces
    back to back. To quit press 'q'+'enter'. This programme minimises overhead for each measurement,
    permitting measurements to be taken with quicker succession than if connecting each time
    a trace is captured. The downside is that which channels are being captured cannot be
    changing thoughout the measurements.
    """
    with acq.Oscilloscope(address=address, timeout=timeout) as scope:
        ## Initialise
        scope.set_acquiring_options(wav_format=wav_format, acq_type=acq_type,
                                   num_averages=num_averages, p_mode=p_mode,
                                   num_points=num_points)
        scope.ext = ext
        scope.set_channels_for_capture(channels=channels)
        # Check that file does not exist from before, append to name if it does
        n = start_num
        fname = auxiliary.check_file(fname, ext, num=f"{file_delim}{n}")
        print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
        print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
        while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
            scope.verbose_acquistion = (i==n)
            fnum = f"{file_delim}{n}"
            scope.get_trace()
            scope.save_trace(fname+fnum)
            n += 1
    print("Quit")


def get_num_traces(fname=config._filename, ext=config._filetype, num=1, address=config._visa_address,
                   timeout=config._timeout, wav_format=config._waveform_format,
                   channels=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                   num_averages=config._num_avg, p_mode='RAW', num_points=0, start_num=0, file_delim=config._file_delimiter):
    """This program connects to the oscilloscope, sets options for the
    acquisition, and captures and stores 'num' traces.
    """
    with acq.Oscilloscope(address=address, timeout=timeout) as scope:
        scope.set_acquiring_options(wav_format=wav_format, acq_type=acq_type,
                                   num_averages=num_averages, p_mode=p_mode,
                                   num_points=num_points, acq_print=False)
        scope.ext = ext
        ## Select sources
        scope.set_channels_for_capture(channels=channels)
        n = start_num
        fnum = file_delim+str(n)
        # Check that file does not exist from before, append to name if it does
        fname = auxiliary.check_file(fname, ext, num=fnum)
        for i in tqdm(range(n, n+num)):
            fnum = file_delim+str(i)
            scope.verbose_acquistion = (i==n)
            scope.get_trace()
            scope.save_trace(fname+fnum)
    print("Done")
