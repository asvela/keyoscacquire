**********
How to use
**********

The VISA addresses of connected instruments can be found running ``list_visa_devices``
in cmd or the terminal (this programme is installed with keyoscacquire),
or can be found in NI MAX or the
`PyVISA shell <https://pyvisa.readthedocs.io/en/latest/introduction/shell.html>`_.

Setting the address of your oscilloscope in
:data:`~keyoscacquire.config._visa_address` in :mod:`keyoscacquire.config`
will make all the installed command line programmes talk to your by default.
The config file can be found with cmd/terminal by ``path_of_config`` (see :ref:`default-options`).

.. note:: In order to connect to a VISA instrument, NI MAX or similar might
  need to be running on the computer.

.. _cli-programmes-short:

Command line programmes for trace export
========================================

Four command line programmes for trace exporting can be ran directly from the
command line after installation (i.e. from whatever folder and no need for
``$ python [...].py``):

* :program:`get_single_trace`
* :program:`get_num_traces`
* :program:`get_traces_connect_each_time` and
* :program:`get_traces_single_connection`

They all have options, the manuals are available using the flag ``-h``.

The two first programmes will obtain one and a specified number of traces,
respectively. The two latter programmes are loops for which every time ``enter``
is hit a trace will be obtained and exported as csv and png files with successive
numbering. By default all active channels on the oscilloscope will be captured
(this can be changed, see :ref:`default-options`).

The difference between the two latter programmes is that the first programme is
establishing a new connection to the instrument each time a trace is to be captured,
whereas the second opens a connection to start with and does not close the
connection until the program is quit. The second programme only checks which
channels are active when it connects, i.e. the first programme will save only
the currently active channels for each saved trace; the second will each time
save the channels that were active at the time of starting the programme.


Optional command line arguments
-------------------------------

The programmes takes optional arguments, the manuals are available using the
flag ``-h`` (see also :ref:`cli-programmes` for more details). Here are three examples

* ``-v USB0::1234::1234::MY1234567::INSTR`` set the visa address of the instrument
* ``-f "custom filename"`` sets the base filename to "custom filename"
* ``-a AVER8``  sets acquiring type to average with eight traces

.. highlight:: console

For example

.. prompt:: bash

    get_traces_single_connection_loop -f "measurement"

will give output files ``measurement n<n>.csv`` and ``measurement n<n>.png``.
The programmes will check if the file ``"measurement"+_file_delimiter+num+_filetype)``
exists, and if it does, prompt the user for something to append to ``measurement``
until ``"measurement"+appended+"0"+_filetype`` is not an existing file. The same
checking procedure applies also when no base filename is supplied and
``config._default_filename`` is used.

.. highlight:: python


Waveform formats
================

The oscilloscope can transfer the waveform to the computer in three different ways

* Comma separated ASCII values
* 8-bit integers
* 16-bit integers

Keysight call these ASCii, BYTE and WORD, respectively. The two latter integer
types must be post-processed on the computer using a preamble that can be queried
for from the ocilloscope. The keyoscacquire package supports all three formats
and does the conversion for the integer transfer types, i.e. the output files
will be ASCII format anyway, it is simply a question of how the data is
transferred to and processed on the computer
(see :func:`~keyoscacquire.oscilloscope.Oscilloscope.capture_and_read` and
:func:`~keyoscacquire.dataprocessing.process_data`).

The 16-bit values format is approximately 10x faster than ascii and gives the
same vertical resolution. 8-bit has significantly lower vertical resolution
than the two others, but gives an even higher speed-up.

The default waveform type can be set in with
:const:`~keyoscacquire.config._waveform_format`, see :ref:`default-options`,
or using the API :attr:`~keyoscacquire.oscilloscope.Oscilloscope.wav_format`.


Using the API
=============

The package provides an API for use with your Python code. For example

.. literalinclude :: ../../keyoscacquire/scripts/example.py
  :linenos:

See :ref:`osc-class` and :ref:`data-proc` for more. The command line programmes
have a Python backend that can integrated in Python scripts or used as
examples, see :ref:`py-programmes`.

.. todo :: Expand examples



Note on obtaining traces when the scope is running vs when stopped
==================================================================

When the scope **is running** the ``capture_and_read`` functions will obtain a
trace by the ``:DIGitize`` VISA command, causing the instrument to acquire a
trace and then stop the oscilloscope. When the scope **is stopped** the current
trace on the screen of the oscilloscope will be captured.

.. warning:: The settings specified with VISA commands under ``:ACQuire``, i.e.
  acquiring mode and number of points to be captured, will not be applied to
  the acquisition if the scope already is stopped while in a different mode.

The scope will always be set to running after a trace is captured.


.. _default-options:

Default options in :mod:`keyoscacquire.config`
================================================================

The package takes its default options from :mod:`keyoscacquire.config`
(to find the location of the file run ``$ path_to_config`` in the command line):

.. literalinclude :: ../../keyoscacquire/config.py
  :linenos:

.. note:: Changing these after importing the module with an ``import`` statement
  will not have any effect.

The command line programmes will save traces in the folder from where they are
ran as ``_filename+_file_delimiter+<n>+_filetype``, i.e. by default as
``data n<n>.csv`` and ``data n<n>.png``.


.. _logging:

Logging
=======

The module gives output for debugging through :mod:`logging`. The output can be
directed to the terminal by adding the following to the top level file using
the keyoscacquire package::

    import logging
    logging.basicConfig(level=logging.DEBUG)

or directed to a file ``mylog.log`` with::

    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)


Miscellaneous
=============

Executing the module
--------------------

Running the module with

.. prompt:: bash

    python -m keyoscacquire

obtains and saves a trace with default options being used. Alternatively, the
filename and acquisition type can be specified as per the paragraph above using
the executable, e.g.

.. prompt:: bash

    get_single_trace -f "fname" -a "AVER"


Scripts in ``./scripts``
------------------------

These can be ran as command line programmes from the scripts folder with
``$ python [script].py [options]``, where the options are as for the installed
command line programmes, and can be displayed with the flag ``-h``.
