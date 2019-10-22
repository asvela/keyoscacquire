**********
How to use
**********

The VISA addresses of connected instruments can be found with the installed command line function :meth:`list_visa_devices` or can be found in NI MAX. The address should be set as the ``_visa_address`` in :mod:`keyoscacquire.config`

.. note:: In order to connect to a VISA instrument, NI MAX or similar might need to be running on the computer.


.. _standalone-programmes:

Standalone programmes for trace export
======================================

Four command line programmes for trace exporting, can be ran directly from the command line after installation (i.e. from whatever folder
and no need for ``$ python [...].py``):

* :meth:`get_single_trace`

* :meth:`get_num_traces`

* :meth:`get_traces_connect_each_time` and

* :meth:`get_traces_single_connection`

They all have options, the manuals are available using the flag ``-h``.

The two first programmes will obtain one and a specified number of traces, respectively. The two latter programmes are loops for which every time ``enter`` is hit a trace will be obtained and exported as csv and png files with successive numbering. By default all active channels on the oscilloscope will be captured (this can be changed, see :ref:`default-options`).

The difference between the two latter programmes is that the first programme is establishing a new connection to the instrument each time a trace is to be captured, whereas the second opens a connection to start with and does not close the connection until the program is quit. The second programme only checks which channels are active when it connects, i.e. the first programme will save only the currently active channels for each saved trace; the second will each time save the channels that were active at the time of starting the programme.


Optional command line arguments
-------------------------------

The programmes takes optional arguments, the manuals are available using the flag ``-h``. Here are three examples

* ``-f "custom filename"`` set as the base filename to "custom filename"

* ``-a AVER8``  sets acquiring type to average with eight traces

* ``-n 10`` sets number of traces to obtain (only for `get_num_traces`)

.. highlight:: console

For example::

    $ get_traces_single_connection_loop -f measurement

will give output files ``measurement n<n>.csv`` and ``measurement n<n>.png``.  The programmes will check if the file ``"measurement"+_file_delimiter+num+_filetype)`` exists, and if it does, prompt the user for something to append to ``measurement`` until ``"measurement"+appended+"0"+_filetype`` is not an existing file. The same checking procedure applies also when no base filename is supplied and ``config._default_filename`` is used.

.. highlight:: python


Using the API
=============

The package can also be used in python scripts. For example

.. literalinclude :: ../../keyoscacquire/scripts/example.py

See :ref:`osc-class` and :ref:`data-proc` for more. There are also some programmes that can be integrated in python scripts or used as examples, see :ref:`py-programmes`.



Note on obtaining traces when the scope is running vs when stopped
==================================================================

When the scope **is running** the ``capture_and_read`` functions will obtain a trace by the ``:DIGitize`` VISA command, causing the instrument to acquire a trace and then stop the oscilloscope. When the scope **is stopped** the current trace on the screen of the oscilloscope will be captured.

.. warning:: The settings specified with VISA commands under ``:ACQuire``, i.e. acquiring mode and number of points to be captured, will not be applied to the acquisition if the scope already is stopped while in a different mode.

The scope will always be set to running after a trace is captured.


.. _default-options:

Default options in :mod:`keyoscacquire.config`
================================================================

.. py:module:: keyoscacquire.config

The package is installed with a set of default options found in :mod:`keyoscacquire.config` (to find the location of the file run :program:`path_to_config` from the command line):

.. literalinclude :: ../../keyoscacquire/config.py

.. note:: None of the functions access the global variables directly, but they are feed them as default arguments.

The ``_waveform_format`` dictates whether 16/8-bit raw values or comma separated ascii voltage values should be transferred when the waveform is queried for (the output file will be ascii anyway, this is simply a question of how the data is transferred to and processed on the computer). 16-bit values format is approx. 10x faster than ascii. See :attr:`~keyoscacquire.oscacq.Oscilloscope.wav_format`, as well as :func:`~keyoscacquire.oscacq.Oscilloscope.capture_and_read` and :func:`~keyoscacquire.oscacq.process_data`.

The command line programmes will save traces in the folder from where they are ran as ``_filename+_file_delimiter+<n>+_filetype``, i.e. by default as ``data n<n>.csv`` and ``data n<n>.png``.


.. _logging:

Logging
=======

The module gives output for debugging through :mod:`logging`. The output can be directed to the terminal by adding the following to the top level file using the keyoscacquire package::

    import logging
    logging.basicConfig(level=logging.DEBUG)

or directed to a file ``mylog.log`` with::

    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)


Misc
====

Executing the module
--------------------

Running the module with ``$ python -m keyoscacquire`` obtains and saves a trace with default options being used. Alternatively, the filename and acquisition type can be specified as per the paragraph above using the executable, e.g. ``$ get_single_trace -f "fname" -a "AVER"``.


Scripts in ./scripts
--------------------

These can be ran as command line scripts from the folder with ``$ python [script].py``. Optional arguments for filename and acquisition mode can be used, such as ``$ python [script].py "otherFileName"``, or ``$ python [script].py "otherFileName" "AVER8"``. Note, no flag specifiers are needed (or allowed) and the sequence of arguments is fixed.
