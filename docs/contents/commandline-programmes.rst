.. _cli-programmes:

Command line programmes
***********************

.. |br| raw:: html

    <br>

keyoscacquire installs command line programmes to find VISA devices, find the
path of the :mod:`~keyoscacquire.config` file and obtain single or multiple traces.

For all the trace-obtaining programmes, the filename is checked to ensure no
overwrite, if a file exists from before the programme prompts for suffix to the
filename. The filename is recursively checked after appending.

The file header in the ascii files saved is::

    <id>
    <mode>
    <timestamp>
    time,<chs>

Where ``<id>`` is the :attr:`~keyoscacquire.oscacq.Oscilloscope.id` of the
oscilloscope, and ``<chs>`` are the comma separated channels used. For example::

    # AGILENT TECHNOLOGIES,DSO-X 2024A,MY1234567,12.34.1234567890
    # AVER8
    # 2019-09-06 20:01:15.187598
    # time,1,3



list_visa_devices
-----------------

**list_visa_devices** [*-h*]
    Prints a list of the VISA instruments connected to the computer, including their addresses.

.. program:: list_visa_devices

**Options**
    **-h, \\-\\-help**: Show help


path_of_config
--------------

**path_of_config** [*-h*]
    Prints the full path of the :mod:`~keyoscacquire.config`

.. program:: path_of_config

**Options**
    **-h, \\-\\-help**: Show help

get_single_trace
----------------

**get_single_trace** [*options*]
    Opens a connection to the VISA instrument, obtain one single trace with standard options in :mod:`~keyoscacquire.config` or override with the options below.

.. program:: get_single_trace

**Options**
    **Connection settings:**
      **-v** <visa address>: Visa address of instrument. To find the visa addresses of the instruments connected to the computer run ``list_visa_devices`` in the command line |br|
      **-t** <timeout>: Milliseconds before timeout on the channel to the instrument
    **Acquiring settings:**
      **-c** <channels>: List of the channel numbers to be acquired, for example ``1 3`` or ``active`` to capture all the currently active channels on the oscilloscope |br|
      **-a** <acq_type>: The acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536] |br|
    **Transfer and storage settings:**
      **-w** <wav_format>: The waveform format: {BYTE, WORD, ASCii} |br|
      **-p** <num_points>: Use 0 to get the maximum number of points, or set a smaller number to speed up the acquisition and transfer |br|
      **-f** <filename>: The filename base, (without extension, '.csv' is added) |br|
    **Other:**
      **-h, \\-\\-help**: show help

get_num_traces
--------------

**get_num_traces** [*options*]
    Opens a connection to the VISA instrument, obtains a specific number of traces with standard options in :mod:`~keyoscacquire.config` or override with the options below. Defaults to 1 trace.

.. program:: get_num_traces

**Options**
    **Connection settings:**
      **-v** <visa address>: Visa address of instrument. To find the visa addresses of the instruments connected to the computer run ``list_visa_devices`` in the command line |br|
      **-t** <timeout>: Milliseconds before timeout on the channel to the instrument
    **Acquiring settings:**
      **-c** <channels>: List of the channel numbers to be acquired, for example ``1 3`` or ``active`` to capture all the currently active channels on the oscilloscope |br|
      **-a** <acq_type>: The acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536] |br|
    **Transfer and storage settings:**
      **-w** <wav_format>: The waveform format: {BYTE, WORD, ASCii} |br|
      **-p** <num_points>: Use 0 to get the maximum number of points, or set a smaller number to speed up the acquisition and transfer |br|
      **-f** <filename>: The filename base, (without extension, '.csv' is added) |br|
      **\\-\\-file_delimiter** <file_delimiter>: Delimiter used between filename and filenumber (before filetype)
    **Other:**
      **-h, \\-\\-help**: show help


get_traces_single_connection
----------------------------

**get_traces_connect_each_time** [*options*]
    This program connects to the oscilloscope, sets the default (:mod:`~keyoscacquire.config`) or argument overridden options for the acquisition and then enters a loop in which the program captures and stores traces each time 'enter' is pressed.

    Alternatively one can input `n-1` characters before hitting ``enter`` to capture `n` traces
    back to back. To quit press ``q`` + ``enter``. This programme minimises overhead for each measurement,
    permitting measurements to be taken with quicker succession than if connecting each time
    a trace is captured. The downside is that which channels are being captured cannot be
    changing thoughout the measurements.

.. program:: get_traces_single_connection

**Options**
    **Connection settings:**
      **-v** <visa address>: Visa address of instrument. To find the visa addresses of the instruments connected to the computer run ``list_visa_devices`` in the command line |br|
      **-t** <timeout>: Milliseconds before timeout on the channel to the instrument
    **Acquiring settings:**
      **-c** <channels>: List of the channel numbers to be acquired, for example ``1 3`` or ``active`` to capture all the currently active channels on the oscilloscope |br|
      **-a** <acq_type>: The acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536] |br|
    **Transfer and storage settings:**
      **-w** <wav_format>: The waveform format: {BYTE, WORD, ASCii} |br|
      **-p** <num_points>: Use 0 to get the maximum number of points, or set a smaller number to speed up the acquisition and transfer |br|
      **-f** <filename>: The filename base, (without extension, '.csv' is added) |br|
      **\\-\\-file_delimiter** <file_delimiter>: Delimiter used between filename and filenumber (before filetype)
    **Other:**
      **-h, \\-\\-help**: show help

get_traces_connect_each_time
----------------------------

**get_traces_connect_each_time** [*options*]
    This program consists of a loop in which the program connects to the oscilloscope,
    sets the default (:mod:`~keyoscacquire.config`) or argument overridden options for
    the acquisition, and captures and stores a trace from the active channels
    for each loop.

    This permits the active channels to be changing thoughout the measurements, but has larger
    overhead due to establishing and closing a new connection every time.

    The loop runs each time ``enter`` is hit. Alternatively one can input `n-1` characters before hitting
    ``enter`` to capture `n` traces back to back. To quit press ``q`` + ``enter``.

.. program:: get_traces_connect_each_time

**Options**
    **Connection settings:**
      **-v** <visa address>: Visa address of instrument. To find the visa addresses of the instruments connected to the computer run ``list_visa_devices`` in the command line |br|
      **-t** <timeout>: Milliseconds before timeout on the channel to the instrument
    **Acquiring settings:**
      **-c** <channels>: List of the channel numbers to be acquired, for example ``1 3`` or ``active`` to capture all the currently active channels on the oscilloscope |br|
      **-a** <acq_type>: The acquire type: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536] |br|
    **Transfer and storage settings:**
      **-w** <wav_format>: The waveform format: {BYTE, WORD, ASCii} |br|
      **-p** <num_points>: Use 0 to get the maximum number of points, or set a smaller number to speed up the acquisition and transfer |br|
      **-f** <filename>: The filename base, (without extension, '.csv' is added) |br|
      **\\-\\-file_delimiter** <file_delimiter>: Delimiter used between filename and filenumber (before filetype)
    **Other:**
      **-h, \\-\\-help**: show help
