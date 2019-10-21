# -*- coding: utf-8 -*-
"""
The PyVISA communication with the oscilloscope.
See Keysight's Programmer's Guide for reference.

Andreas Svela // 2019
"""

__docformat__ = "restructuredtext en"

import sys, os        # required for reading user input and command line arguments
import pyvisa         # instrument communication
import time, datetime # for measuring elapsed time and adding current date and time to exported files
import numpy as np
import matplotlib.pyplot as plt
import logging; _log = logging.getLogger(__name__)

# local file with default options:
import keyoscacquire.config as config

_screen_colors = {'1':'C1', '2':'C2', '3':'C0', '4':'C3'} # Keysight colour map
# Datatype is 'H' for 16 bit unsigned int (WORD), 'B' for 8 bit unsigned bit (BYTE)
# (same naming as for structs, see https://docs.python.org/3/library/struct.html#format-characters)
_datatypes = {'BYTE':'B', 'WORD':'H'}


##============================================================================##

class Oscilloscope():
    """
    Wrapper class for PyVISA communication with the oscilloscope.
    """

    def __init__(self, address=config._visa_address, timeout=config._timeout):
        """
        Open a connection to instrument and choose settings for the connection.
        Raises pyvisa.Error if no successful connection is made.

        Parameters
        ----------
        address : str
            Visa address of instrument. To find the visa addresses of the instruments
            connected to the computer use the
            examples 'USB0::2391::6038::MY5737636::INSTR', 'TCPIP0::192.168.20.30::4000::SOCKET'
        timeout : int
            Milliseconds before timeout on the channel to the instrument
        """
        self.timeout = timeout
        self.acquire_print = True

        try:
            rm = pyvisa.ResourceManager()
            self.inst = rm.open_resource(address)
            self.address = address
        except pyvisa.Error as err:
            print('\nVisaError: Could not connect to \'%s\', exiting now...' % address)
            raise
        # make sure WORD and BYTE data is transeferred as unsigned ints
        self.inst.write(':WAVeform:UNSigned ON')
        # For TCP/IP socket connections enable the read Termination Character, or reads will timeout
        if self.inst.resource_name.endswith('SOCKET'):
            self.inst.read_termination = '\n'

        self.inst.timeout = self.timeout
        self.inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
        self.id = self.inst.query('*IDN?').strip() # get the id of the connected device
        print("Connected to \'%s\'" % self.id)

    def run(self):
        """Set the ocilloscope to running mode."""
        self.inst.write(':RUN')

    def stop(self):
        """Stop the oscilloscope."""
        self.inst.write(':STOP')

    def is_running(self):
        """
        Determine if the oscilloscope is running.

        Returns
        -------
        b : bool
            True if running
        """
        reg = int(self.inst.query(':OPERegister:CONDition?')) # The third bit of the operation register is 1 if the instrument is running
        return (reg & 8) == 8

    def close(self, set_running=True):
        """
        Closes the connection to the oscilloscope.

        Parameters
        ----------
        set_running : bool, optional, default True
            decide whether to set the oscilloscope to running before closing the connection
        """
        # Set the oscilloscope running before closing the connection
        if set_running: self.run()
        self.inst.close()
        _log.debug("Closed connection to \'%s\'" % self.id)

    def set_acquire_print(self, value):
        """
        Control attribute which decides whether to print information while acquiring.

        Parameters
        ----------
        value : bool
            True to print information to info level in log
        """
        self.acquire_print = value

    def set_acquiring_options(self, wav_format=config._waveform_format, acq_type=config._acq_type,
                              num_averages=config._num_avg, p_mode='RAW', num_points=0, acq_print=None):
        """
        Sets the options for acquisition from the oscilloscope.

        Parameters
        ----------
        wav_format : str, optional, default config._waveform_format
            Select the format of the communication of waveform from the oscilloscope
            possible choices {'WORD' | 'BYTE' | 'ASCii'}
        acq_type : str, optional, default config._acq_type
            Selects the acquisition mode of the oscilloscope
            possible choices {'HRESolution' | 'NORMal' | 'AVERage' | 'AVER<m>'}
            <m> will be used as num_averages if supplied
        num_averages : int, optional, default config._num_avg
            2 to 65536: applies only to the NORMal and AVERage modes
        p_mode : str, optional, default 'RAW'
            possible choices {'RAW' | 'MAXimum'}
            'RAW' gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
        num_points : int, optional, default 0
            possible choices {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000
                                | 50000 | 100000 | 200000 | 500000 | 1000000}
            optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.
        """
        self.wav_format = wav_format; self.acq_type = acq_type[:4]
        self.p_mode = p_mode; self.num_points = num_points

        if acq_print is not None:
            self.acquire_print = acq_print #set acquiring_print only if not None

        self.inst.write(':ACQuire:TYPE ' + self.acq_type)
        print("  Acquiring type:", self.acq_type)
        # handle AVER<m> expressions
        if self.acq_type == 'AVER':
            try:
                self.num_averages = int(acq_type[4:]) if len(acq_type) > 4 else num_averages # if the type is longer than four characters, treat characters from fifth to end as number of averages
            except ValueError:
                print("\nValueError: Failed to convert \'%s\' to an integer,"
                      " check that acquisition type is on the form AVER or AVER<m>"
                      " where <m> is an integer (currently acq. type is \'%s\').\n"
                       % (acq_type[4:], acq_type))
            if self.num_averages < 1 or self.num_averages > 65536: #check that self.num_averages is within acceptable range
                raise ValueError("\nThe number of averages {} is out of range.\nExiting..\n".format(self.num_averages))
        else:
            self.num_averages = num_averages

        # now set the number of averages parameter if relevant
        if self.acq_type[:4] == 'NORM' or self.acq_type[:4] == 'AVER': # averaging applies for NORMal and AVERage modes only
            #self.inst.write(':ACQuire:MODE RTIME')
            self.inst.write(':ACQuire:COUNt ' + str(self.num_averages))
            print("  # of averages: ", self.num_averages)

        ## Set options for waveform export
        self.inst.write(':WAVeform:FORMat ' +  self.wav_format) # choose format for the transmitted waveform]
        a_isaver = self.acq_type == 'AVER'
        p_isnorm = self.p_mode[:4] == 'NORM'
        if a_isaver and not p_isnorm:
            self.p_mode = 'NORM'
            _log.debug(":WAVeform:POINts:MODE overridden (from %s) to NORMal due to :ACQuire:TYPE:AVERage." % p_mode)
        else:
            self.p_mode = p_mode
        self.inst.write(':WAVeform:POINts:MODE ' + self.p_mode)
        #_log.debug("Max number of points for mode %s: %s" % (self.p_mode, self.inst.query(':WAVeform:POINts?')))
        if self.num_points != 0: #if number of points has been specified
            inst.write(':WAVeform:POINts ' + str(self.num_points))
            print("Number of points set to: ", self.num_points)

    def build_sourcesstring(self, source_type='CHANnel', channel_nums=config._ch_nums):
        """
        Set the channels to be acquired, or determine by checking active channels on the oscilloscope.

        Parameters
        ----------
        source_type : str, optional, default 'CHANnel'
            Selects the source type. Must be 'CHANnel' in current implementation.
            Future version might include { 'MATH' | 'FUNCtion'}.
        channel_nums : list, optional, default config._ch_nums
            list of the channel numbers to be acquired from
            Example ['1', '3']
            .. note::
                Use channel_nums=[''] to capture all the currently active channels on the oscilloscope.

        Returns
        -------
        sources : list of strs
            list of the sources
            Example ['CHAN1', 'CHAN3']
        channel_nums : list of chars
            list of the channels
            Example ['1', '3']
        """
        if channel_nums == ['']: # if no channels specified, find the channels currently active and acquire from those
            channels = np.array(['1', '2', '3', '4'])
            displayed_channels = [self.inst.query(':CHANnel'+channel+':DISPlay?')[0] for channel in channels] # querying DISP for each channel to determine which channels are currently displayed
            channel_mask = np.array([bool(int(i)) for i in displayed_channels]) # get a mask of bools for the channels that are on [need the int() as int('0') = True]
            channel_nums = channels[channel_mask] # apply mask to the channel list
        sources = [source_type+channel for channel in channel_nums] # build list of sources
        sourcesstring = ", ".join(sources) # make string of sources
        if self.acquire_print: print("Acquire from sources", sourcesstring)
        return sourcesstring, sources, channel_nums

    def capture_and_read(self, sources, sourcestring):
        """
        This is a wrapper function for choosing the correct capture_and_read function according to wav_format:
            :py:func:`capture_and_read_binary`
            :py:func:`capture_and_read_ascii`

        Acquire raw data from selected channels according to acquring options currently set.
        The parameters are provided by build_sourcesstring()

        Parameters
        ----------
        sources : list of strs
            list of sources
            Example ['CHANnel1', 'CHANnel3']
        sourcesstring : str
            String of comma separated sources
            Example 'CHANnel1, CHANnel3'
        Returns
        -------
        See respective
            :py:func:`capture_and_read_binary`
            :py:func:`capture_and_read_ascii`

        See also
        --------
        Setting acquiring options: :py:func:`set_acquiring_options`


        """
        if self.wav_format[:3] in ['WOR', 'BYT']:
            return self.capture_and_read_binary(sources, sourcestring, datatype=_datatypes[self.wav_format])
        elif self.wav_format[:3] == 'ASC':
            return self.capture_and_read_ascii(sources, sourcestring)
        else:
            raise Exception("\nError: Could not capture and read data, waveform format \'{}\' is unknown.\nExiting..\n".format(self.wav_format))

    def capture_and_read_binary(self, sources, sourcesstring, datatype=_datatypes[self.wav_format]):
        """
        Capture and read data and metadata from sources of the oscilloscope when waveform format is WORD or BYTE
        The parameters are provided by :py:func:`build_sourcesstring`

        Parameters
        ----------
        sources : list of strs
            list of sources
            Example ['CHANnel1', 'CHANnel3']
        sourcesstring : str
            String of commaseparated sources
            Example 'CHANnel1, CHANnel3'
        datatype : char, optional but must match wav_format used
            To determine how to read the values from the oscilloscope depending on the
            wav_format setting. Datatype is 'H' for 16 bit unsigned int (WORD), 'B' for
            8 bit unsigned bit (BYTE) (same naming as for structs, see
            https://docs.python.org/3/library/struct.html#format-characters).
            Use _datatypes[self.wav_format] to automativally

        Returns
        -------
        raw : ndarray
            Raw data to be processed by :py:func:`process_data` (using :py:func:`process_data_binary`)
            An ndarray of ints that is converted to voltage values using the preamble.
        preamble : list
            Preamble metadata (ascii comma separated values)
        """
        ## Capture data
        if self.acquire_print: print("Start acquisition..")
        start_time = time.time() # time the acquiring process
        # If the instrument is not running, we presumably want the data on the screen and hence don't want
        # to use DIGitize as digitize will obtain a new trace.
        if self.is_running():
            self.inst.write(':DIGitize ' + sourcesstring) # DIGitize is a specialized RUN command.
                                                     # Waveforms are acquired according to the settings of the :ACQuire commands.
                                                     # When acquisition is complete, the instrument is stopped.
        ## Read out metadata and data
        raw, preambles = [], []
        for source in sources:
            self.inst.write(':WAVeform:SOURce ' + source) # selects the channel for which the succeeding WAVeform commands applies to
            try:
                # obtain comma separated metadata values for processing of raw data for this source
                preambles.append(self.inst.query(':WAVeform:PREamble?'))
                # obtain the data
                raw.append(self.inst.query_binary_values(':WAVeform:DATA?', datatype=datatype, container=np.array)) # read out data for this source
            except pyvisa.Error as err:
                print("\nError: Failed to obtain waveform, have you checked that"
                      " the timeout (currently %d ms) is sufficently long?" % self.timeout)
                print(err)
                print("\nExiting..\n")
                self.close()
                raise
        if self.acquire_print:
            _log.info("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        else:
            _log.debug("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        self.inst.write(':RUN') # set the oscilloscope running again
        return raw, preambles

    def capture_and_read_ascii(self, sources, sourcesstring):
        """
        Capture and read data and metadata from sources of the oscilloscope when waveform format is ASCii.
        The parameters are provided by :py:func:`build_sourcesstring`

        Parameters
        ----------
        sources : list of strs
            list of sources
            Example ['CHANnel1', 'CHANnel3']
        sourcesstring : str
            String of commaseparated sources
            Example 'CHANnel1, CHANnel3'

        Returns
        -------
        raw : list
            Raw data to be processed by :py:func:`process_data` (using :py:func:`process_data_ascii`)
            The raw data is a list of one IEEE block per channel with a head and then comma separated ascii values
        measurement_time : float
            The time duration of the measurement *(note: the length of the time axis)* in seconds
            Used in :py:func:`process_data_ascii` to calculate the time axis (for all channels)
        """
        ## Capture data
        if self.acquire_print: print("Start acquisition..")
        start_time = time.time() # time the acquiring process
        # If the instrument is not running, we presumably want the data on the screen and hence don't want
        # to use DIGitize as digitize will obtain a new trace.
        if self.is_running():
            self.inst.write(':DIGitize ' + sourcesstring) # DIGitize is a specialized RUN command.
                                                     # Waveforms are acquired according to the settings of the :ACQuire commands.
                                                     # When acquisition is complete, the instrument is stopped.
        ## Read out data
        raw = []
        for source in sources: # loop through all the sources
            self.inst.write(':WAVeform:SOURce ' + source) # selects the channel for which the succeeding WAVeform commands applies to
            try:
                raw.append(self.inst.query(':WAVeform:DATA?')) # read out data for this source
            except pyvisa.Error:
                print("\nVisaError: Failed to obtain waveform, have you checked that"
                      " the timeout (currently %d ms) is sufficently long?" % self.timeout)
                print("\nExiting..\n")
                self.close()
                raise
        if self.acquire_print:
            _log.info("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        else:
            _log.debug("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        measurement_time = float(self.inst.query(':TIMebase:RANGe?')) # returns the current full-scale range value for the main window
        self.inst.write(':RUN') # set the oscilloscope running again
        return raw, measurement_time

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    def getTrace(self, sources, sourcesstring, acquire_print=None):
        """
        Obtain one trace with current settings.

        Parameters
        ----------
        sources : list of strs
            list of sources
            Example ['CHANnel1', 'CHANnel3']
        sourcesstring : str
            String of commaseparated sources
            Example 'CHANnel1, CHANnel3'
        acquire_print : {bool, None}, optional, default None
            Possibility to override acquire_print temporarily, but the current
            setting will be restored afterwards

        Returns
        -------
        time : ndarray
            Time axis for the measurement
        y : ndarray
            Voltage values, same sequence as sources input

        """
        if acquire_print is not None: # possibility to override acquire_print
            temp = self.acquire_print # store current setting
            self.acquire_print = acquire_print # set temporary setting
        raw, metadata = self.capture_and_read(sources, sourcesstring)
        time, y = process_data(raw, metadata, self.wav_format, acquire_print=self.acquire_print) # capture, read and process data
        if acquire_print is not None: self.acquire_print = temp # restore to previous setting
        return time, y

    def set_options_getTrace(self, channel_nums=[''], source_type='CHANnel',
                                 wav_format=config._waveform_format, acq_type=config._acq_type,
                                 num_averages=config._num_avg, p_mode='RAW', num_points=0):
        """
        Set the options provided by the parameters and obtain one trace.

        Parameters
        ----------
        channel_nums : list, optional, default ['']
            list of the channel numbers to be acquired from.
            Example ['1', '3']
            .. note:: Use channel_nums=[''] to capture all the currently active channels on the oscilloscope.
        source_type : str, optional, default 'CHANnel'
            Selects the source type. Must be 'CHANnel' in current implementation.
            Future version might include { 'MATH' | 'FUNCtion'}.
        wav_format : str, optional, default config._waveform_format
            Select the format of the communication of waveform from the oscilloscope
            possible choices {'WORD' | 'BYTE' | 'ASCii'}
        acq_type : str, optional, default config._acq_type
            Selects the acquisition mode of the oscilloscope
            possible choices {'HRESolution' | 'NORMal' | 'AVERage' | 'AVER<m>'}
            <m> will be used as num_averages if supplied
        num_averages : int, optional, default config._num_avg
            2 to 65536: applies only to the NORMal and AVERage modes
        p_mode : str, optional, default 'RAW'
            possible choices {'RAW' | 'MAXimum'}
            'RAW' gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
        num_points : int, optional, default 0
            possible choices {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000 | 50000 | 100000 | 200000 | 500000 | 1000000}
            optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.

        Returns
        -------
        time : ndarray
            Time axis for the measurement
        y : ndarray
            Voltage values, same sequence as channel_nums
        channel_nums : list of chars
            list of the channels obtained from
            Example ['1', '3']
        """
        ## Connect to instrument and specify acquiring settings
        self.set_acquiring_options(wav_format=wav_format, acq_type=acq_type,
                                   num_averages=num_averages, p_mode=p_mode,
                                   num_points=num_points)
        ## Select sources
        sourcesstring, sources, channel_nums = self.build_sourcesstring(source_type=source_type, channel_nums=channel_nums)
        ## Capture, read and process data
        time, y = self.getTrace(sources, sourcesstring)
        return time, y, channel_nums

    def set_options_getTrace_save(self, fname=config._filename, ext=config._filetype, channel_nums=[''], source_type='CHANnel',
                                  wav_format=config._waveform_format, acq_type=config._acq_type, num_averages=config._num_avg, p_mode='RAW', num_points=0):
        """
        Get trace and save the trace to a file and plot to png.
        Filename is recursively checked to ensure no overwrite.
        The file header is
            id
            time,"+",".join(channel_nums)
            timestamp

        Parameters
        ----------
        fname : str, optional, default config._filename
            Filename of trace
        ext : str, optional, default config._filetype
            Choose the filetype of the saved trace
        channel_nums : list, optional, default ['']
            list of the channel numbers to be acquired from.
            Example ['1', '3']
            .. note::
                Use channel_nums=[''] to capture all the currently active channels on the oscilloscope.
        source_type : str, optional, default 'CHANnel'
            Selects the source type. Must be 'CHANnel' in current implementation.
            Future version might include { 'MATH' | 'FUNCtion'}.
        wav_format : str, optional, default config._waveform_format
            Select the format of the communication of waveform from the oscilloscope
            possible choices {'WORD' | 'BYTE' | 'ASCii'}
        acq_type : str, optional, default config._acq_type
            Selects the acquisition mode of the oscilloscope
            possible choices {'HRESolution' | 'NORMal' | 'AVERage' | 'AVER<m>'}
            <m> will be used as num_averages if supplied
        num_averages : int, optional, default config._num_avg
            2 to 65536: applies only to the NORMal and AVERage modes
        p_mode : str, optional, default 'RAW'
            possible choices {'RAW' | 'MAXimum'}
            'RAW' gives up to 1e6 points. Use MAXimum for sources that are not analogue or digital (functions and math)
        num_points : int, optional, default 0
            possible choices {0 | 100 | 250 | 500 | 1000 | 2000 | 5000 | 10000 | 20000
                                | 50000 | 100000 | 200000 | 500000 | 1000000}
            optional command when p_mode (POINTs:MODE) is specified. Use 0 to let p_mode control the number of points.
        """
        fname = check_file(fname, ext)
        x, y, channel_nums = self.set_options_getTrace(channel_nums=channel_nums, source_type=source_type,
                                                       wav_format=wav_format, acq_type=acq_type, num_averages=num_averages,
                                                       p_mode=p_mode, num_points=num_points)
        plotTrace(x, y, channel_nums, fname=fname)
        head = self.id+"\ntime,"+",".join(channel_nums)+"\n"
        saveTrace(fname, x, y, fileheader=head, ext=ext, acquire_print=self.acquire_print)



##============================================================================##
##                           DATA PROCESSING                                  ##
##============================================================================##

def process_data(raw, metadata, wav_format, acquire_print=True):
    """
    Wrapper function for choosing the correct process_data function according to wav_format
    """
    if wav_format[:3] in ['WOR', 'BYT']:
        return process_data_binary(raw, metadata, acquire_print)
    elif wav_format[:3] == 'ASC':
        return process_data_ascii(raw, metadata, acquire_print)
    else:
        raise Exception("\nError: Could not process data, waveform format \'{}\' is unknown.\nExiting..\n".format(wav_format))
        sys.exit()

def process_data_binary(raw, preambles, acquire_print):
    """
    Process raw 8/16-bit data to time x values and y voltage values.
    Output: numpy array x containing time values, numpy array y containing voltages for captured channels
    """
    preamble = preambles[0].split(',')  # values separated by commas
    # 0 FORMAT : int16 - 0 = BYTE, 1 = WORD, 4 = ASCII.
    # 1 TYPE : int16 - 0 = NORMAL, 1 = PEAK DETECT, 2 = AVERAGE
    num_samples = int(preamble[2])    # POINTS : int32 - number of data points transferred.
    # 3 COUNT : int32 - 1 and is always 1.
    xIncr = float(preamble[4])        # XINCREMENT : float64 - time difference between data points.
    xOrig = float(preamble[5])        # XORIGIN : float64 - always the first data point in memory.
    xRef = int(preamble[6])           # XREFERENCE : int32 - specifies the data point associated with x-origin.
    # 7 YINCREMENT : float32 - voltage diff between data points.
    # 8 YORIGIN : float32 - value is the voltage at center screen.
    # 9 YREFERENCE : int32 - specifies the data point where y-origin occurs.

    if acquire_print: print("Points captured per channel: ", num_samples)
    y = np.empty((len(raw), num_samples))
    for i, data in enumerate(raw):
        preamble = preambles[i].split(',')
        yIncr, yOrig, yRef = float(preamble[7]), float(preamble[8]), int(preamble[9])
        y[i,:] = (data-yRef)*yIncr + yOrig
    y = y.T # convert y to np array and transpose for vertical channel columns in csv file
    x = np.array([(np.arange(num_samples)-xRef)*xIncr + xOrig]) # compute x-values
    x = x.T # make x values vertical
    return x, y

def process_data_ascii(raw, measurement_time, acquire_print):
    """
    Process raw comma separated ascii data to time x values and y voltage values.
    Output: numpy array x containing time values, numpy array y containing voltages for caputred channels
    """
    y = []
    for data in raw:
        data = data.split(data[:10])[1] # remove first 10 characters (is this a quick but not so intuitive way?)
        data = data.split(',') # samples separated by commas
        data = np.array([float(sample) for sample in data])
        y.append(data) # add ascii data for this channel to y array

    y = np.transpose(np.array(y))
    num_samples = np.shape(y)[0] # number of samples captured per channel
    x = np.array([np.linspace(0, measurement_time, num_samples)]) # compute x-values
    x = x.T # make list vertical
    if acquire_print:
        print("Points captured per channel: ", num_samples)
        _log.info("Points captured per channel: ", num_samples)
    return x, y

##============================================================================##
##                           SAVING FILES                                     ##
##============================================================================##

def check_file(fname, ext=config._filetype, num=""):
    """
    Checking if file fname+num+ext exists. If it does the user is prompted
    for a string to append to fname until a unique fname is found.

    Parameters
    ----------
    fname : str
        Base filename to test
    ext : str, optional, default config._filetype
        File extension
    num : str, optional, default ""
        Filename suffix that is tested for, but the appended part to the fname will be placed before it,
        and the suffix will not be part of the returned fname

    Returns
    -------
    fname : str
        New fname base
    """
    while os.path.exists(fname+num+ext):
        append = input("File \'%s\' exists! Append to filename \'%s\' before saving: " % (fname+num+ext, fname))
        fname += append
    return fname

def saveTrace(fname, time, y, fileheader="", ext=config._filetype, acquire_print=True):
    """
    Saves the trace with time values and y values as a txt/csv/dat etc specified by 'ext'.
    Current date and time is automatically added to the header.

    Parameters
    ----------
    fname : str
        Filename of trace
    time : ndarray
        Time axis for the measurement
    y : ndarray
        Voltage values, same sequence as channel_nums
    fileheader : str, optional, default ""
        Optional prefix for current date and time which is automatically added to the header.
    ext : str, optional, default config._filetype
        Choose the filetype of the saved trace
    acquire_print : bool, optional, default True
        True prints the filename it is saved to
    """
    date_time = str(datetime.datetime.now()) # get current date and time
    if acquire_print: print("Saving trace to %s\n" % (fname+ext))
    data = np.append(time, y, axis=1) # make one array with coloumns x y1 y2 ..
    np.savetxt(fname+ext, data, delimiter=",", header=fileheader+date_time)

def plotTrace(time, y, channel_nums, fname="", show=config._show_plot, savepng=config._export_png):
    """
    Plots the trace with oscilloscope channel screen colours according to the
    Keysight colourmap and saves as a png.

    Parameters
    ----------
    time : ndarray
        Time axis for the measurement
    y : ndarray
        Voltage values, same sequence as channel_nums
    channel_nums : list of chars
        list of the channels obtained from
        Example ['1', '3']
    fname : str, optional, default ""
        Filename of possible exported png
    show : bool, optional, default config._show_plot
        True shows the plot (must be closed before the programme proceeds)
    savepng : bool, optional, default config._export_png
        True exports the plot to 'fname'.png
        .. note:: No filename check, can overwrite existing
    """
    for i, vals in enumerate(np.transpose(y)): # for each channel
        plt.plot(time, vals, color=_screen_colors[channel_nums[i]])
    if savepng: plt.savefig(fname+".png", bbox_inches='tight')
    if show: plt.show()
    plt.close()


##============================================================================##
##                           MAIN FUNCTION                                    ##
##============================================================================##

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    fname = sys.argv[1] if len(sys.argv) >= 2 else config._filename
    ext = config._filetype
    scope = Oscilloscope(address='USB0::0x0957::0x1796::MY59125372::INSTR', )
    scope.set_options_getTrace_save(fname, ext, wav_format='WORD')
    scope.close()
