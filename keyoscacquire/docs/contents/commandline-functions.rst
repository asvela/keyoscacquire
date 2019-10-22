Command line functions
**********************


Auxiliary
=========

.. program:: list_visa_devices
    prints a list of the visa devices connected to the computer

.. option:: -h
    show description

.. program:: path_of_config
    prints the full path of the :py:mod:`keysightoscacq.config`

.. option:: -h
    show description


To obtain traces
================

For all the programmes, the filename is checked to ensure no overwrite, if a file exists from before the programme prompts for suffix to the filename. The filename is recursively checked after appending.

The file header in the ascii files saved is

    id of oscilloscope (:attr:`~keysightoscacq.oscacq.Oscilloscope.id`)
    time,<chs>
    timestamp

Where <chs> are the comma separated channels used. For example

    # AGILENT TECHNOLOGIES,DSO-X 2024A,MY57233636,02.42.2017032900
    # time,1,3
    # 2019-09-06 20:01:15.187598


.. program:: get_single_trace

.. option:: -f <filename>
    Set the file name for saving the trace

.. option:: -a <acquisition mode>
    Set the acquiring mode for the trace
