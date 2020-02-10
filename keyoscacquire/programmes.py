# -*- coding: utf-8 -*-
"""
Python backend for installed command line programmes. These can also be integrated in python scripts or used as examples.

* :func:`list_visa_devices`: listing visa devices

* :func:`path_of_config`: finding path of config.py

* :func:`get_single_trace`: taking a single trace and saving it to csv and png

* :func:`get_traces_single_connection_loop` :func:`get_traces_connect_each_time_loop`: two programmes for taking multiple traces when a key is pressed, see descriptions for difference

* :func:`get_num_traces`: get a specific number of traces

"""

import sys, logging; _log = logging.getLogger(__name__)
import keyoscacquire.oscacq as acq
import numpy as np
from tqdm import tqdm #progressbar

# local file with default options:
import keyoscacquire.config as config


def list_visa_devices(ask_idn=True):
    """Prints a list of the VISA instruments connected to the computer, including their addresses."""
    import pyvisa
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    if len(resources) == 0:
        print("\nNo VISA devices found!")
    else:
        print("Found {} resources. Now obtaining information about them..".format(len(resources)))
        information, could_not_connect = [], []
        for i, address in enumerate(resources): # loop through resources to learn more about them
            current_resource_info = []
            info_object = rm.resource_info(address)
            alias = info_object.alias if info_object.alias is not None else "N/A"
            current_resource_info.extend((str(i), address, alias))
            if ask_idn:
                try: # open the instrument and get the identity string
                    instrument = rm.open_resource(address)
                    id = instrument.query('*IDN?')
                    current_resource_info.extend(acq.interpret_visa_id(id))
                    instrument.close()
                except pyvisa.Error as e:
                    could_not_connect.append(i)
                    current_resource_info.extend(["no connection"]*5)
                except Exception as ex:
                    print("(i) Got exception %s when asking instrument #%i for identity." % (ex.__class__.__name__, i))
                    could_not_connect.append(i)
                    current_resource_info.extend(["Error"]*5)
            information.append(current_resource_info)
        if ask_idn:
            # transpose to lists of property
            nums, addrs, aliases, makers, models, serials, firmwares, model_series = (list(category) for category in zip(*information))
            # select what properties to list
            selection = (nums, addrs, makers, models, model_series, aliases)
            # name columns
            header_fields = (' #', 'address', 'maker', 'model', 'series', 'alias')
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
    import os
    print("config.py can be found in:\n\t%s\n" % os.path.dirname(os.path.abspath(__file__)))


def get_single_trace(fname=config._filename, ext=config._filetype, address=config._visa_address,
                     timeout=config._timeout, wav_format=config._waveform_format,
                     channel_nums=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                     num_averages=config._num_avg, p_mode='RAW', num_points=0):
    """This programme captures and stores a single trace."""
    scope = acq.Oscilloscope(address=address, timeout=timeout)
    scope.set_options_get_trace_save(fname=fname, ext=ext, wav_format=wav_format,
                          channel_nums=channel_nums, source_type=source_type, acq_type=acq_type,
                          num_averages=num_averages, p_mode=p_mode, num_points=num_points)
    scope.close()
    print("Done")


def get_traces_connect_each_time_loop(fname=config._filename, ext=config._filetype, address=config._visa_address,
                                      timeout=config._timeout, wav_format=config._waveform_format,
                                      channel_nums=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                                      num_averages=config._num_avg, p_mode='RAW', num_points=0, start_num=0, file_delim=config._file_delimiter):
    """This program consists of a loop in which the program connects to the oscilloscope,
    a trace from the active channels are captured and stored for each loop.

    This permits the active channels to be changing thoughout the measurements, but has larger
    overhead due to establishing and closing a new connection every time.

    The loop runs each time 'enter' is hit. Alternatively one can input n-1 characters before hitting
    'enter' to capture n traces back to back. To quit press 'q'+'enter'.
    """
    n = start_num
    fnum = file_delim+str(n)
    fname = acq.check_file(fname, ext, num=fnum) # check that file does not exist from before, append to name if it does
    print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
    print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
    while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
        fnum = file_delim+str(n)
        scope = acq.Oscilloscope(address=address, timeout=timeout)
        x, y, channels = scope.set_options_get_trace(wav_format=wav_format,
                              channel_nums=channel_nums, source_type=source_type, acq_type=acq_type,
                              num_averages=num_averages, p_mode=p_mode, num_points=num_points)
        acq.plot_trace(x, y, channels, fname=fname+fnum)
        fhead = scope.generate_file_header(channel_nums)
        acq.save_trace(fname+fnum, x, y, fileheader=fhead, ext=ext)
        scope.close()
        n += 1
    print("Quit")

def get_traces_single_connection_loop(fname=config._filename, ext=config._filetype, address=config._visa_address,
                                      timeout=config._timeout, wav_format=config._waveform_format,
                                      channel_nums=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                                      num_averages=config._num_avg, p_mode='RAW', num_points=0, start_num=0, file_delim=config._file_delimiter):
    """This program connects to the oscilloscope, sets options for the acquisition and then
    enters a loop in which the program captures and stores traces each time 'enter' is pressed.

    Alternatively one can input n-1 characters before hitting 'enter' to capture n traces
    back to back. To quit press 'q'+'enter'. This programme minimises overhead for each measurement,
    permitting measurements to be taken with quicker succession than if connecting each time
    a trace is captured. The downside is that which channels are being captured cannot be
    changing thoughout the measurements.
    """
    ## Initialise
    scope = acq.Oscilloscope(address=address, timeout=timeout)
    scope.set_acquiring_options(wav_format=wav_format, acq_type=acq_type,
                               num_averages=num_averages, p_mode=p_mode,
                               num_points=num_points)
    ## Select sources
    sources, sourcesstring, channel_nums = scope.determine_channels(source_type=source_type, channel_nums=channel_nums)
    fhead = scope.generate_file_header(channel_nums)
    n = start_num
    fnum = file_delim+str(n)
    fname = acq.check_file(fname, ext, num=fnum) # check that file does not exist from before, append to name if it does
    print("Running a loop where at every 'enter' oscilloscope traces will be saved as %s<n>%s," % (fname, ext))
    print("where <n> increases by one for each captured trace. Press 'q'+'enter' to quit the programme.")
    while sys.stdin.read(1) != 'q': # breaks the loop if q+enter is given as input. For any other character (incl. enter)
        fnum = file_delim+str(n)
        x, y = scope.get_trace(sources, sourcesstring)
        acq.plot_trace(x, y, channel_nums, fname=fname+fnum)                    # plot trace and save png
        acq.save_trace(fname+fnum, x, y, fileheader=fhead, ext=ext) # save trace to ext file
        n += 1

    print("Quit")
    scope.close()


def get_num_traces(fname=config._filename, ext=config._filetype, num=1, address=config._visa_address,
                   timeout=config._timeout, wav_format=config._waveform_format,
                   channel_nums=config._ch_nums, source_type='CHANnel', acq_type=config._acq_type,
                   num_averages=config._num_avg, p_mode='RAW', num_points=0, start_num=0, file_delim=config._file_delimiter):
        """This program connects to the oscilloscope, sets options for the
        acquisition, and captures and stores 'num' traces.
        """
        ## Initialise
        scope = acq.Oscilloscope(address=address, timeout=timeout)
        scope.set_acquiring_options(wav_format=wav_format, acq_type=acq_type,
                                   num_averages=num_averages, p_mode=p_mode,
                                   num_points=num_points, acq_print=False)
        ## Select sources
        sources, sourcesstring, channel_nums = scope.determine_channels(source_type=source_type, channel_nums=channel_nums)
        fhead = scope.generate_file_header(channel_nums)
        n = start_num
        fnum = file_delim+str(n)
        fname = acq.check_file(fname, ext, num=fnum) # check that file does not exist from before, append to name if it does
        for i in tqdm(range(n, n+num)):
            fnum = file_delim+str(i)
            x, y = scope.get_trace(sources, sourcesstring, acquire_print=(i==n))
            #acq.plot_trace(x, y, channel_nums, fname=fname+fnum)        # plot trace and save png
            acq.save_trace(fname+fnum, x, y, fileheader=fhead, ext=ext, print_filename=(i==n)) # save trace to ext file
        print("Done")
        scope.close()
