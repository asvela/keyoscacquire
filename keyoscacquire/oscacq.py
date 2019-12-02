# -*- coding: utf-8 -*-
"""The PyVISA communication with the oscilloscope.

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

#: Supported Keysight DSO/MSO InfiniiVision series
_supported_series = ['1000', '2000', '3000', '4000', '6000']
#: Keysight colour map for the channels
_screen_colors = {'1':'C1', '2':'C2', '3':'C0', '4':'C3'}
#: Datatype is ``'h'`` for 16 bit signed int (``WORD``), ``'b'`` for 8 bit signed bit (``BYTE``).
#: Same naming as for structs `docs.python.org/3/library/struct.html#format-characters`
_datatypes = {'BYTE':'b', 'WORD':'h'}


##============================================================================##

class Oscilloscope():
    """PyVISA communication with the oscilloscope.

    Creator opens a connection to an instrument and chooses settings for the connection.

    Parameters
    ----------
    address : str, optional, default :data:`~keyoscacquire.config._visa_address`
        Visa address of instrument. To find the visa addresses of the instruments
        connected to the computer run ``list_visa_devices`` in the command line.
        Example address ``'USB0::1234::1234::MY1234567::INSTR'``
    timeout : int, optional, default :data:`~keyoscacquire.config._timeout`
        Milliseconds before timeout on the channel to the instrument
    verbose : bool, optional, default True
        Whether or not to allow print() output. False will suppress everything except errors.

    Raises
    ------
    :class:`pyvisa.errors.Error`
        if no successful connection is made.

    Attributes
    ----------
    inst : pyvisa.resources.Resource
        The oscilloscope PyVISA resource
    id : str
        The maker, model, serial and firmware version of the scope. Examples::

            'AGILENT TECHNOLOGIES,DSO-X 2024A,MY1234567,12.34.567891234'
            'KEYSIGHT TECHNOLOGIES,MSO9104A,MY12345678,06.30.00609'

    model : str
        The instrument model name
    model_series : str
        The model series, e.g. '2000' for a DSO-X 2024A. See :func:`interpret_visa_id`.
    address : str
        Visa address of instrument
    timeout : int
        Milliseconds before timeout on the channel to the instrument
    acq_type : {'HRESolution', 'NORMal', 'AVERage', 'AVER<m>'}
        Acquisition mode of the oscilloscope. <m> will be used as :attr:`num_averages` if supplied.

        * ``'NORMal'`` — sets the oscilloscope in the normal mode.

        * ``'AVERage'`` — sets the oscilloscope in the averaging mode. You can set the count by :attr:`num_averages`.

        * ``'HRESolution'`` — sets the oscilloscope in the high-resolution mode (also known as smoothing). This mode is used to reduce noise at slower sweep speeds where the digitizer samples faster than needed to fill memory for the displayed time range.

            For example, if the digitizer samples at 200 MSa/s, but the effective sample rate is 1 MSa/s
            (because of a slower sweep speed), only 1 out of every 200 samples needs to be stored.
            Instead of storing one sample (and throwing others away), the 200 samples are averaged
            together to provide the value for one display point. The slower the sweep speed, the greater
            the number of samples that are averaged together for each display point.
    num_averages : int, 2 to 65536
        The number of averages applied (applies only to the ``'AVERage'`` :attr:`acq_type`)
    p_mode : {``'NORMal'``, ``'RAW'``, ``'MAXimum'``}
        ``'NORMal'`` is limited to 62,500 points, whereas ``'RAW'`` gives up to 1e6 points. Use ``'MAXimum'`` for sources that are not analogue or digital.
    num_points : int
        Use 0 to let :attr:`p_mode` control the number of points, otherwise override with a lower number than maximum for the :attr:`p_mode`
    wav_format : {'WORD', 'BYTE', 'ASCii'}
        Select the data transmission mode for waveform data points, i.e. how the data is formatted when sent from the oscilloscope.

        * ``'ASCii'`` formatted data converts the internal integer data values to real Y-axis values. Values are transferred as ascii digits in floating point notation, separated by commas.

        * ``'WORD'`` formatted data transfers signed 16-bit data as two bytes.

        * ``'BYTE'`` formatted data is transferred as signed 8-bit bytes.

    acquire_print : bool
        ``True`` prints that the capturing starts and the number of points captured
    """

    def __init__(self, address=config._visa_address, timeout=config._timeout, verbose=True):
        """See class docstring"""
        self.address = address
        self.timeout = timeout
        self.acquire_print = True
        if not verbose: self.acquire_print = False
        self.verbose = verbose

        try:
            rm = pyvisa.ResourceManager()
            self.inst = rm.open_resource(address)
        except pyvisa.Error as err:
            print('\nVisaError: Could not connect to \'%s\'.' % address)
            raise
        self.inst.timeout = self.timeout
        # For TCP/IP socket connections enable the read Termination Character, or reads will timeout
        if self.inst.resource_name.endswith('SOCKET'):
            self.inst.read_termination = '\n'
        # Clear the status data structures, the device-defined error queue, and the Request-for-OPC flag
        self.inst.write('*CLS')
        # Make sure WORD and BYTE data is transeferred as signed ints and lease significant bit first
        self.inst.write(':WAVeform:UNSigned OFF')
        self.inst.write(':WAVeform:BYTeorder LSBFirst') # MSBF is default, must be overridden for WORD to work
        # Get information about the connected device
        self.id = self.inst.query('*IDN?').strip() # get the id of the connected device
        if verbose: print("Connected to \'%s\'" % self.id)
        _, self.model, _, _, self.model_series = interpret_visa_id(self.id)
        if not self.model_series in _supported_series:
                if self.verbose: print("(!) WARNING: This model (%s) is not yet fully supported by keyoscacquire," % self.model)
                if self.verbose: print("             but might work to some extent. keyoscacquire supports Keysight's")
                if self.verbose: print("             InfiniiVision X-series oscilloscopes.")


    def write(self, command):
        """Write a VISA command to the oscilloscope.

        Parameters
        ----------
        command : str
            VISA command to be written"""
        self.inst.write(command)

    def query(self, command):
        """Query a VISA command to the oscilloscope.

        Parameters
        ----------
        command : str
            VISA query"""
        return self.inst.query(command)

    def run(self):
        """Set the ocilloscope to running mode."""
        self.inst.write(':RUN')

    def stop(self):
        """Stop the oscilloscope."""
        self.inst.write(':STOP')

    def is_running(self):
        """Determine if the oscilloscope is running.

        Returns
        -------
        bool
            ``True`` if running, ``False`` otherwise
        """
        reg = int(self.inst.query(':OPERegister:CONDition?')) # The third bit of the operation register is 1 if the instrument is running
        return (reg & 8) == 8

    def close(self, set_running=True):
        """Closes the connection to the oscilloscope.

        Parameters
        ----------
        set_running : bool, optional, default ``True``
            ``True`` sets the oscilloscope to running before closing the connection, ``False`` leaves it in its current state
        """
        # Set the oscilloscope running before closing the connection
        if set_running: self.run()
        self.inst.close()
        _log.debug("Closed connection to \'%s\'" % self.id)

    def set_acquire_print(self, value):
        """Control attribute which decides whether to print information while acquiring.

        Parameters
        ----------
        value : bool
            ``True`` to print information to info level in log
        """
        self.acquire_print = value

    def set_acquiring_options(self, wav_format=config._waveform_format, acq_type=config._acq_type,
                              num_averages=config._num_avg, p_mode='RAW', num_points=0, acq_print=None):
        """Sets the options for acquisition from the oscilloscope.

        Parameters
        ----------
        wav_format : {``'WORD'``, ``'BYTE'``, ``'ASCii'``}, optional, default :data:`~keyoscacquire.config._waveform_format`
            Select the format of the communication of waveform from the oscilloscope, see :attr:`wav_format`
        acq_type : {``'HRESolution'``, ``'NORMal'``, ``'AVERage'``, ``'AVER<m>'``}, optional, default :data:`~keyoscacquire.config._acq_type`
            Acquisition mode of the oscilloscope. <m> will be used as num_averages if supplied, see :attr:`acq_type`
        num_averages : int, 2 to 65536, optional, default :data:`~keyoscacquire.config._num_avg`
            Applies only to the ``'AVERage'`` mode: The number of averages applied
        p_mode : {``'NORMal'``, ``'RAW'``, ``'MAXimum'``}, optional, default ``'RAW'``
            ``'NORMal'`` is limited to 62,500 points, whereas ``'RAW'`` gives up to 1e6 points. Use ``'MAXimum'`` for sources that are not analogue or digital
        num_points : int, optional, default 0
            Use 0 to let :attr:`p_mode` control the number of points, otherwise override with a lower number than maximum for the :attr:`p_mode`
        acq_print : bool or ``None``, optional, default ``None``
            Temporarily control attribute which decides whether to print information while acquiring: bool sets it to the bool value, ``None`` leaves as the it is in the Oscilloscope object

        Raises
        ------
        ValueError
            if num_averages are outside of the range or <m> in acq_type cannot be converted to int
        """
        self.wav_format = wav_format; self.acq_type = acq_type[:4]
        self.p_mode = p_mode; self.num_points = num_points

        if acq_print is not None:
            self.acquire_print = acq_print #set acquiring_print only if not None

        self.inst.write(':ACQuire:TYPE ' + self.acq_type)
        if self.verbose: print("  Acquiring type:", self.acq_type)
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
                raise ValueError("\nThe number of averages {} is out of range.".format(self.num_averages))
        else:
            self.num_averages = num_averages

        # now set the number of averages parameter if relevant
        if self.acq_type[:4] == 'AVER': # averaging applies AVERage modes only
            self.inst.write(':ACQuire:COUNt ' + str(self.num_averages))
            if self.verbose: print("  # of averages: ", self.num_averages)

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
        #_log.debug("Max number of points for mode %s: %s" % (self.p_mode, self.inst.query(':ACQuire:POINts?')))
        if self.num_points > 0: # if number of points has been specified
            if self.model_series in _supported_series:
                self.inst.write(':WAVeform:POINts ' + str(self.num_points))
            elif self.model_series in ['9000']:
                self.inst.write(':ACQuire:POINts ' + str(self.num_points))
            else:
                self.inst.write(':WAVeform:POINts ' + str(self.num_points))
            _log.debug("Number of points set to: ", self.num_points)

    def determine_channels(self, source_type='CHANnel', channel_nums=config._ch_nums):
        """Decide the channels to be acquired, or determine by checking active channels on the oscilloscope.

        .. note:: Use ``channel_nums='active'`` to capture all the currently active channels on the oscilloscope.

        Parameters
        ----------
        source_type : str, optional, default ``'CHANnel'``
            Selects the source type. Must be ``'CHANnel'`` in current implementation.
            Future version might include {'MATH', 'FUNCtion'}.
        channel_nums : list or ``'active'``, optional, default :data:`~keyoscacquire.config._ch_nums`
            list of the channel numbers to be acquired, example ``['1', '3']``.
            Use ``'active'`` or ``['']`` to capture all the currently active channels on the oscilloscope.

        Returns
        -------
        sources : list of str
            list of the sources, example ``['CHAN1', 'CHAN3']``
        sourcesstring : str
            String of comma separated sources, example ``'CHANnel1, CHANnel3'``
        channel_nums : list of chars
            list of the channels, example ``['1', '3']``
        """
        if channel_nums in [[''], ['active'], 'active']: # if no channels specified, find the channels currently active and acquire from those
            channels = np.array(['1', '2', '3', '4'])
            displayed_channels = [self.inst.query(':CHANnel'+channel+':DISPlay?')[0] for channel in channels] # querying DISP for each channel to determine which channels are currently displayed
            channel_mask = np.array([bool(int(i)) for i in displayed_channels]) # get a mask of bools for the channels that are on [need the int() as int('0') = True]
            channel_nums = channels[channel_mask] # apply mask to the channel list
        sources = [source_type+channel for channel in channel_nums] # build list of sources
        sourcesstring = ", ".join(sources) # make string of sources
        if self.acquire_print: print("Acquire from sources", sourcesstring)
        return sources, sourcesstring, channel_nums

    def capture_and_read(self, sources, sourcestring, set_running=True):
        """This is a wrapper function for choosing the correct capture_and_read function according to :attr:`wav_format`, :func:`capture_and_read_binary` or :func:`capture_and_read_ascii`.

        Acquire raw data from selected channels according to acquring options currently set with :func:`set_acquiring_options`.
        The parameters are provided by :func:`determine_channels`.

        The output should be processed by :func:`process_data`.

        Parameters
        ----------
        sources : list of str
            list of sources, example ``['CHANnel1', 'CHANnel3']``
        sourcesstring : str
            String of comma separated sources, example ``'CHANnel1, CHANnel3'``
        set_running : bool, optional, default ``True``
            ``True`` leaves oscilloscope running after data capture

        Returns
        -------
        See respective
            Depends on the capture_and_read function used

        Raises
        ------
        ValueError
            If :attr:`wav_format` is not {'BYTE', 'WORD', 'ASCii'}

        See also
        --------
        :func:`process_data`
        """
        if self.wav_format[:3] in ['WOR', 'BYT']:
            return self.capture_and_read_binary(sources, sourcestring, datatype=_datatypes[self.wav_format], set_running=set_running)
        elif self.wav_format[:3] == 'ASC':
            return self.capture_and_read_ascii(sources, sourcestring, set_running=set_running)
        else:
            raise ValueError("Could not capture and read data, waveform format \'{}\' is unknown.\n".format(self.wav_format))

    def capture_and_read_binary(self, sources, sourcesstring, datatype='standard', set_running=False):
        """Capture and read data and metadata from sources of the oscilloscope when waveform format is ``'WORD'`` or ``'BYTE'``.

        The parameters are provided by :func:`determine_channels`.
        The output should be processed by :func:`process_data_binary`.

        Parameters
        ----------
        sources : list of str
            list of sources, example ``['CHANnel1', 'CHANnel3']``
        sourcesstring : str
            String of comma separated sources, example ``'CHANnel1, CHANnel3'``
        datatype : char or ``'standard'``, optional but must match waveform format used
            To determine how to read the values from the oscilloscope depending on :attr:`wav_format`. Datatype is ``'h'`` for 16 bit signed int (``'WORD'``), for 8 bit signed bit (``'BYTE'``) (same naming as for structs, `https://docs.python.org/3/library/struct.html#format-characters`).
            ``'standard'`` will evaluate :data:`oscacq._datatypes[self.wav_format]` to automatically choose according to the waveform format
        set_running : bool, optional, default ``True``
            ``True`` leaves oscilloscope running after data capture

        Returns
        -------
        raw : :class:`~numpy.ndarray`
            Raw data to be processed by :func:`process_data_binary`.
            An ndarray of ints that can be converted to voltage values using the preamble.
        preamble : str
            Preamble metadata (comma separated ascii values)
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
                self.close()
                raise
        if self.acquire_print:
            _log.info("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        else:
            _log.debug("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        if set_running: self.inst.write(':RUN') # set the oscilloscope running again
        return raw, preambles

    def capture_and_read_ascii(self, sources, sourcesstring, set_running=True):
        """Capture and read data and metadata from sources of the oscilloscope when waveform format is ASCii.

        The parameters are provided by :func:`determine_channels`.
        The output should be processed by :func:`process_data_ascii`.

        Parameters
        ----------
        sources : list of str
            list of sources, example ``['CHANnel1', 'CHANnel3']``
        sourcesstring : str
            String of comma separated sources, example ``'CHANnel1, CHANnel3'``
        set_running : bool, optional, default ``True``
            ``True`` leaves oscilloscope running after data capture

        Returns
        -------
        raw : str
            Raw data to be processed by :func:`process_data_ascii`.
            The raw data is a list of one IEEE block per channel with a head and then comma separated ascii values.
        metadata : tuple of str
            Tuple of the preamble for one of the channels to calculate time axis (same for all channels) and the model series
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
                self.close()
                raise
        if self.acquire_print:
            _log.info("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        else:
            _log.debug("Elapsed time capture and read: %.1f ms" % ((time.time()-start_time)*1e3))
        preamble = self.inst.query(':WAVeform:PREamble?') # preamble (used for calculating time axis, which is the same for all channels)
        metadata = (preamble, self.model_series)
        if set_running: self.inst.write(':RUN') # set the oscilloscope running again
        return raw, metadata

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    def get_trace(self, sources, sourcesstring, acquire_print=None):
        """Obtain one trace with current settings.

        Parameters
        ----------
        sources : list of str
            list of sources, example ``['CHANnel1', 'CHANnel3']``
        sourcesstring : str
            String of comma separated sources, example ``'CHANnel1, CHANnel3'``
        acquire_print : bool or ``None``, optional, default ``None``
            Possibility to override :attr:`acquire_print` temporarily, but the current
            setting will be restored afterwards

        Returns
        -------
        time : :class:`~numpy.ndarray`
            Time axis for the measurement
        y : :class:`~numpy.ndarray`
            Voltage values, same sequence as sources input, each row represents one channel

        """
        if acquire_print is not None: # possibility to override acquire_print
            temp = self.acquire_print # store current setting
            self.acquire_print = acquire_print # set temporary setting
        raw, metadata = self.capture_and_read(sources, sourcesstring)
        time, y = process_data(raw, metadata, self.wav_format, acquire_print=self.acquire_print) # capture, read and process data
        if acquire_print is not None: self.acquire_print = temp # restore to previous setting
        return time, y

    def set_options_get_trace(self, channel_nums=config._ch_nums, source_type='CHANnel',
                                 wav_format=config._waveform_format, acq_type=config._acq_type,
                                 num_averages=config._num_avg, p_mode='RAW', num_points=0):
        """Set the options provided by the parameters and obtain one trace.

        Parameters
        ----------
        channel_nums : list or ``'active'``, optional, default :data:`~keyoscacquire.config._ch_nums`
            list of the channel numbers to be acquired from, example ``['1', '3']``.
            Use ``'active'`` to capture all the currently active channels on the oscilloscope.
        source_type : str, optional, default ``'CHANnel'``
            Selects the source type. Must be ``'CHANnel'`` in current implementation.
            Future version might include {'MATH', 'FUNCtion'}.
        wav_format : {``'WORD'``, ``'BYTE'``, ``'ASCii'``}, optional, default :data:`~keyoscacquire.config._waveform_format`
            Select the format of the communication of waveform from the oscilloscope, see :attr:`wav_format`
        acq_type : {``'HRESolution'``, ``'NORMal'``, ``'AVERage'``, ``'AVER<m>'``}, optional, default :data:`~keyoscacquire.config._acq_type`
            Acquisition mode of the oscilloscope. <m> will be used as num_averages if supplied, see :attr:`acq_type`
        num_averages : int, 2 to 65536, optional, default :data:`~keyoscacquire.config._num_avg`
            Applies only to the ``'AVERage'`` mode: The number of averages applied
        p_mode : {``'NORMal'``, ``'RAW'``, ``'MAXimum'``}, optional, default ``'RAW'``
            ``'NORMal'`` is limited to 62,500 points, whereas ``'RAW'`` gives up to 1e6 points. Use ``'MAXimum'`` for sources that are not analogue or digital
        num_points : int, optional, default 0
            Use 0 to let :attr:`p_mode` control the number of points, otherwise override with a lower number than maximum for the :attr:`p_mode`

        Returns
        -------
        time : :class:`~numpy.ndarray`
            Time axis for the measurement
        y : :class:`~numpy.ndarray`
            Voltage values, same sequence as ``channel_nums``, each row represents one channel
        channel_nums : list of chars
            list of the channels obtained from, example ``['1', '3']``
        """
        ## Connect to instrument and specify acquiring settings
        self.set_acquiring_options(wav_format=wav_format, acq_type=acq_type,
                                   num_averages=num_averages, p_mode=p_mode,
                                   num_points=num_points)
        ## Select sources
        sources, sourcesstring, channel_nums = self.determine_channels(source_type=source_type, channel_nums=channel_nums)
        ## Capture, read and process data
        time, y = self.get_trace(sources, sourcesstring)
        return time, y, channel_nums

    def set_options_get_trace_save(self, fname=config._filename, ext=config._filetype, channel_nums=config._ch_nums, source_type='CHANnel',
                                  wav_format=config._waveform_format, acq_type=config._acq_type, num_averages=config._num_avg, p_mode='RAW', num_points=0):
        """Get trace and save the trace to a file and plot to png.

        Filename is recursively checked to ensure no overwrite.
        The file header is::

            self.id+"\\n"+
            "time,"+",".join(channel_nums)+"\\n"+
            timestamp

        Parameters
        ----------
        fname : str, optional, default :data:`~keyoscacquire.config._filename`
            Filename of trace
        ext : str, optional, default :data:`~keyoscacquire.config._filetype`
            Choose the filetype of the saved trace
        channel_nums : list or ``'active'``, optional, default :data:`~keyoscacquire.config._ch_nums`
            list of the channel numbers to be acquired from, example ``['1', '3']``.
            Use ``'active'`` to capture all the currently active channels on the oscilloscope
        source_type : str, optional, default ``'CHANnel'``
            Selects the source type. Must be ``'CHANnel'`` in current implementation.
            Future version might include {'MATH', 'FUNCtion'}
        wav_format : {``'WORD'``, ``'BYTE'``, ``'ASCii'``}, optional, default :data:`~keyoscacquire.config._waveform_format`
            Select the format of the communication of waveform from the oscilloscope, see :attr:`wav_format`
        acq_type : {``'HRESolution'``, ``'NORMal'``, ``'AVERage'``, ``'AVER<m>'``}, optional, default :data:`~keyoscacquire.config._acq_type`
            Acquisition mode of the oscilloscope. <m> will be used as num_averages if supplied, see :attr:`acq_type`
        num_averages : int, 2 to 65536, optional, default :data:`~keyoscacquire.config._num_avg`
            Applies only to the ``'AVERage'`` mode: The number of averages applied
        p_mode : {``'NORMal'``, ``'RAW'``, ``'MAXimum'``}, optional, default ``'RAW'``
            ``'NORMal'`` is limited to 62,500 points, whereas ``'RAW'`` gives up to 1e6 points. Use ``'MAXimum'`` for sources that are not analogue or digital
        num_points : int, optional, default 0
            Use 0 to let :attr:`p_mode` control the number of points, otherwise override with a lower number than maximum for the :attr:`p_mode`
        """
        fname = check_file(fname, ext)
        x, y, channel_nums = self.set_options_get_trace(channel_nums=channel_nums, source_type=source_type,
                                                       wav_format=wav_format, acq_type=acq_type, num_averages=num_averages,
                                                       p_mode=p_mode, num_points=num_points)
        plot_trace(x, y, channel_nums, fname=fname)
        head = self.generate_file_header(channel_nums)
        save_trace(fname, x, y, fileheader=head, ext=ext, print_filename=self.acquire_print)

    def generate_file_header(self, channels, additional_line=None, timestamp=True):
        """Generate string to be used as file header for saved files

        The file header has this structure::

            <id>
            <mode>,<averages>
            <timestamp>
            additional_line
            time,<chs>

        Where ``<id>`` is the :attr:`~keyoscacquire.oscacq.Oscilloscope.id` of the oscilloscope,
        ``<mode>`` is the :attr:`~keyoscacquire.oscacq.Oscilloscope.acq_type`, ``<averages>`` :attr:`~keyoscacquire.oscacq.Oscilloscope.num_averages` (``"N/A"`` if not applicable)
        and ``<chs>`` are the comma separated channels used.

        .. note:: If ``additional_line`` is not supplied the fileheader will be four lines. If ``timestamp=False`` the timestamp line will not be present.

        Parameters
        ----------
        channels : list of str
            Any list of identifies for the channels used for the measurement to be saved.
        additional_line : str or ``None``, optional, default ``None``
            No additional line if set to ``None``, otherwise the value of the argument will be used
            as an additonal line to the file header
        timestamp : bool
            ``True`` gives a line with timestamp, ``False`` removes the line

        Returns
        -------
        str
            string to be used as file header

        Example
        -------
        If the oscilloscope is acquiring in ``'AVER'`` mode with eight averages::

            Oscilloscope.generate_file_header(['1', '3'], additional_line="my comment")

        gives::

            # AGILENT TECHNOLOGIES,DSO-X 2024A,MY1234567,12.34.1234567890
            # AVER,8
            # 2019-09-06 20:01:15.187598
            # my comment
            # time,1,3

        """
        num_averages = str(self.num_averages) if self.acq_type[:3] == 'AVE' else "N/A"
        mode_line = self.acq_type+","+num_averages+"\n"
        timestamp_line = str(datetime.datetime.now())+"\n" if timestamp else ""
        add_line = additional_line+"\n" if additional_line is not None else ""
        channels_line = "time,"+",".join(channels)
        return self.id+"\n"+mode_line+timestamp_line+add_line+channels_line


##============================================================================##
##                           DATA PROCESSING                                  ##
##============================================================================##

def process_data(raw, metadata, wav_format, acquire_print=True):
    """Wrapper function for choosing the correct process_data function according to :attr:`wav_format` for the data obtained from :func:`Oscilloscope.capture_and_read`

    Parameters
    ----------
    raw : ~numpy.ndarray or str
        From :func:`~Oscilloscope.capture_and_read`: Raw data, type depending on :attr:`wav_format`
    metadata : list or tuple
        From :func:`~Oscilloscope.capture_and_read`: List of preambles or tuple of preamble and model series depending on :attr:`wav_format`. See :ref:`preamble`.
    wav_format : {``'WORD'``, ``'BYTE'``, ``'ASCii'``}
        Specify what waveform type was used for acquiring to choose the correct processing function.
    acquire_print : bool
        True prints the number of points captured per channel

    Returns
    -------
    time : :class:`~numpy.ndarray`
        Time axis for the measurement
    y : :class:`~numpy.ndarray`
        Voltage values, each row represents one channel

    Raises
    ------
    ValueError
        If ``wav_format`` is not {'BYTE', 'WORD', 'ASCii'}

    See also
    --------
    :func:`Oscilloscope.capture_and_read`
    """
    if wav_format[:3] in ['WOR', 'BYT']:
        return process_data_binary(raw, metadata, acquire_print)
    elif wav_format[:3] == 'ASC':
        return process_data_ascii(raw, metadata, acquire_print)
    else:
        raise ValueError("Could not process data, waveform format \'{}\' is unknown.".format(wav_format))

def process_data_binary(raw, preambles, acquire_print=True):
    """Process raw 8/16-bit data to time values and y voltage values as received from :func:`Oscilloscope.capture_and_read_binary`.

    Parameters
    ----------
    raw : ~numpy.ndarray
        From :func:`~Oscilloscope.capture_and_read_binary`: An ndarray of ints that is converted to voltage values using the preamble.
    preambles : list of str
        From :func:`~Oscilloscope.capture_and_read_binary`: List of preamble metadata for each channel (list of comma separated ascii values, see :ref:`preamble`)
    acquire_print : bool
        True prints the number of points captured per channel

    Returns
    -------
    time : :class:`~numpy.ndarray`
        Time axis for the measurement
    y : :class:`~numpy.ndarray`
        Voltage values, each row represents one channel
    """
    # pick one preamle and use for calculating the time values (same for all channels)
    preamble = preambles[0].split(',')  # values separated by commas
    num_samples = int(float(preamble[2]))
    xIncr, xOrig, xRef = float(preamble[4]), float(preamble[5]), float(preamble[6])
    x = np.array([(np.arange(num_samples)-xRef)*xIncr + xOrig]) # compute x-values
    x = x.T # make x values vertical
    if acquire_print:
        print("Points captured per channel: ", num_samples)
        _log.info("Points captured per channel: ", num_samples)
    y = np.empty((len(raw), num_samples))
    for i, data in enumerate(raw): # process each channel individually
        preamble = preambles[i].split(',')
        yIncr, yOrig, yRef = float(preamble[7]), float(preamble[8]), float(preamble[9])
        y[i,:] = (data-yRef)*yIncr + yOrig
    y = y.T # convert y to np array and transpose for vertical channel columns in csv file
    return x, y

def process_data_ascii(raw, metadata, acquire_print=True):
    """Process raw comma separated ascii data to time values and y voltage values as received from :func:`Oscilloscope.capture_and_read_ascii`

    Parameters
    ----------
    raw : str
        From :func:`~Oscilloscope.capture_and_read_ascii`: A string containing a block header and comma separated ascii values
    metadata : tuple
        From :func:`~Oscilloscope.capture_and_read_ascii`: Tuple of the preamble for one of the channels to calculate time axis (same for all channels) and the model series. See :ref:`preamble`.
    acquire_print : bool
        True prints the number of points captured per channel

    Returns
    -------
    time : :class:`~numpy.ndarray`
        Time axis for the measurement
    y : :class:`~numpy.ndarray`
        Voltage values, each row represents one channel
    """
    preamble, model_series = metadata
    preamble = preamble.split(',')  # values separated by commas
    num_samples = int(float(preamble[2]))
    xIncr, xOrig, xRef = float(preamble[4]), float(preamble[5]), float(preamble[6])
    x = np.array([(np.arange(num_samples)-xRef)*xIncr + xOrig]) # compute x-values
    x = x.T # make list vertical
    if acquire_print:
        print("Points captured per channel: ", num_samples)
        _log.info("Points captured per channel: ", num_samples)
    y = []
    for data in raw:
        if model_series in ['2000']:
            data = data.split(data[:10])[1] # remove first 10 characters (IEEE block header)
        elif model_series in ['9000']:
            data = data.strip().strip(",") # remove newline character at the end of the string
        data = data.split(',') # samples separated by commas
        data = np.array([float(sample) for sample in data])
        y.append(data) # add ascii data for this channel to y array
    y = np.transpose(np.array(y))
    return x, y


##============================================================================##
##                           SAVING FILES                                     ##
##============================================================================##

def check_file(fname, ext=config._filetype, num=""):
    """Checking if file ``fname+num+ext`` exists. If it does, the user is prompted for a string to append to fname until a unique fname is found.

    Parameters
    ----------
    fname : str
        Base filename to test
    ext : str, optional, default :data:`~keyoscacquire.config._filetype`
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

def save_trace(fname, time, y, fileheader="", ext=config._filetype, print_filename=True):
    """Saves the trace with time values and y values to file.

    Current date and time is automatically added to the header. Saving to numpy format with :func:`save_trace_npy` is faster, but does not include metadata and header.

    Parameters
    ----------
    fname : str
        Filename of trace
    time : ~numpy.ndarray
        Time axis for the measurement
    y : ~numpy.ndarray
        Voltage values, same sequence as channel_nums
    fileheader : str, optional, default ``""``
        Header of file, use :func:`generate_file_header`
    ext : str, optional, default :data:`~keyoscacquire.config._filetype`
        Choose the filetype of the saved trace
    print_filename : bool, optional, default ``True``
        ``True`` prints the filename it is saved to
    """
    if print_filename: print("Saving trace to %s\n" % (fname+ext))
    data = np.append(time, y, axis=1) # make one array with coloumns x y1 y2 ..
    np.savetxt(fname+ext, data, delimiter=",", header=fileheader)

def save_trace_npy(fname, time, y, print_filename=True):
    """Saves the trace with time values and y values to npy file.

    .. note:: Saving to numpy files is faster than to ascii format files (:func:`save_trace`), but no file header is added.

    Parameters
    ----------
    fname : str
        Filename to save to
    time : ~numpy.ndarray
        Time axis for the measurement
    y : ~numpy.ndarray
        Voltage values, same sequence as channel_nums
    print_filename : bool, optional, default ``True``
        ``True`` prints the filename it is saved to
    """
    if print_filename: print("Saving trace to %s\n" % (fname+ext))
    data = np.append(time, y, axis=1)
    np.save(pathfname_no_ext+".npy", data)

def plot_trace(time, y, channel_nums, fname="", show=config._show_plot, savepng=config._export_png):
    """Plots the trace with oscilloscope channel screen colours according to the Keysight colourmap and saves as a png.

    .. Caution:: No filename check for the saved plot, can overwrite existing png files.

    Parameters
    ----------
    time : ~numpy.ndarray
        Time axis for the measurement
    y : ~numpy.ndarray
        Voltage values, same sequence as channel_nums
    channel_nums : list of chars
        list of the channels obtained, example ['1', '3']
    fname : str, optional, default ``""``
        Filename of possible exported png
    show : bool, optional, default :data:`~keyoscacquire.config._show_plot`
        True shows the plot (must be closed before the programme proceeds)
    savepng : bool, optional, default :data:`~keyoscacquire.`config._export_png`
        ``True`` exports the plot to ``fname``.png
    """
    for i, vals in enumerate(np.transpose(y)): # for each channel
        plt.plot(time, vals, color=_screen_colors[channel_nums[i]])
    if savepng: plt.savefig(fname+".png", bbox_inches='tight')
    if show: plt.show()
    plt.close()


def interpret_visa_id(id):
    """Interprets VISA ID, finds oscilloscope model series if applicable

    Parameters
    ----------
    id : str
        VISA ID as returned by the ``*IDN?`` command

    Returns
    -------
    maker : str
        Maker of the instrument, e.g. Keysight Technologies
    model : str
        Model of the instrument
    serial : str
        Serial number of the instrument
    firmware : str
        Firmware version
    model_series : str
        "N/A" unless the instrument is a Keysight/Agilent DSO and MSO oscilloscope.
        Returns the model series, e.g. '2000'. Returns "not found" if the model name cannot be interpreted.
    """
    maker, model, serial, firmware = id.split(",")
    # find model_series if applicable
    if model[:3] in ['DSO', 'MSO']:
        model_number = [c for c in model if c.isdigit()] # find the numbers in the model string
        model_series = model_number[0]+'000' if not model_number == [] else "not found"  # pick the first number and add 000 or use not found
    else:
        model_series = "N/A"
    return maker, model, serial, firmware, model_series


##============================================================================##
##                           MAIN FUNCTION                                    ##
##============================================================================##

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    fname = sys.argv[1] if len(sys.argv) >= 2 else config._filename
    ext = config._filetype
    scope = Oscilloscope()
    scope.set_options_get_trace_save(fname, ext)
    scope.close()
