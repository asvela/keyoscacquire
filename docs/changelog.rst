Changelog
=========

v4.0: Extreme (API) makeover
----------------------------
Big makeover with many no compatible changes. When writing the base of this back
in 2019 I had very limited Python development experience, so it was time to make
a few better choices now to make the API easier to use.

That means that there are quite a few non-compatible changes to previous versions,
all of which are detailed below.

v4.0.0 (2020-12)
  - More attributes are used to make the information accessible not only through returns

    * Captured data stored to ``Oscilloscope.time`` and ``Oscilloscope.y``
    * Fname used (not the argument as it might be updated duing saving process)
      stored in ``Oscilloscope.fname``
    * ``Oscilloscope.raw`` and ``Oscilloscope.metadata`` are now available

  - More active use of attributes that are carried forward rather than always
    setting the arguments of methods in the ``Oscilloscope`` class. This
    affects some functions as their arguments have changed (see below), but
    for most functions the arguments stay the same as before. The arguments
    can now be used to change attributes of the ``Oscilloscope`` instance.

  - Bugfixes and docfixes for the number of points to be transferred from the
    instrument (``num_points`` argument). Zero will set the to the
    maximum number of points available.

  - New ``keyoscacquire.traceio.load_trace()`` function for loading saved a trace

  - Moved save and plot functions to ``keyoscacquire.traceio``, but are imported
    in ``oscacq`` to keep compatibility

  - ``Oscilloscope.read_and_capture()`` will now try to read the error from the
    instrument if pyvisa fails

  - Importing ``keyoscacquire.programmes`` in module ``init.py`` to make it accessible

  - Changes in ``list_visa_devices`` and cli programme: now displaying different
    errors more clearly; cli programme now has ``-n`` flag that can be set to not
    ask for instrument IDNs; and the cli programme will display the instrument's
    firmware rather than Keysight model series.

  - Indicating functions for internal and external use by prefix ``_``

  - Documentation updates, including moving from read-the-docs theme to Furo theme

  - PEP8 improvements

  - *(New methods)*:

    * ``Oscilloscope.get_error()``
    * ``Oscilloscope.set_waveform_export_options()``
    * ``Oscilloscope.save_trace()`` (``Oscilloscope.savepng`` and
      ``Oscilloscope.showplot`` can be set to contol its behaviour)
    * ``Oscilloscope.plot_trace()``

  - *No compatibility*: Several functions no longer take ``sources`` and
    ``sourcesstring`` as arguments, rather ``Oscilloscope.sources`` and
    ``Oscilloscope.sourcesstring`` must be set by
    ``Oscilloscope.set_channels_for_capture()``

    * ``Oscilloscope.capture_and_read()`` and its ``Oscilloscope._read_ascii()``
      and ``Oscilloscope._read_binary()``
    * ``Oscilloscope.get_trace()``

  - *No compatibility*: Name changes

    * ``Oscilloscope.determine_channels()`` -> ``Oscilloscope.set_channels_for_capture()``
    * ``Oscilloscope.acquire_print`` -> ``Oscilloscope.verbose_acquistion``
    * ``Oscilloscope.set_acquire_print()`` set ``Oscilloscope.verbose_acquistion``
      attribute instead
    * ``Oscilloscope.capture_and_read_ascii()`` -> ``Oscilloscope._read_ascii()``
      (also major changes in the function)
    * ``Oscilloscope.capture_and_read_binary()`` -> ``Oscilloscope._read_binary()``
      (also major changes in the function)

  - *No compatibility*: Moved functions

    * ``interpret_visa_id()`` from ``oscacq`` to ``auxiliary``
    * ``check_file()`` from ``oscacq`` to ``auxiliary``

  - *No compatibility*: ``Oscilloscope.get_trace()`` now also returns
    also ``Oscilloscope.num_channels``



v3.0: Docs are overrated
------------------------
Comprehensive documentation now available on read the docs, added more command
line programme options, some function name changes without compatibility, and bug fixes.

v3.0.2 (2020-02-10)
  - Context manager compatibility (``__enter__`` and ``__exit__`` functions implemented)
  - Adding the function ``get_active_channels`` to query the scope of its active channels
  - Adding ``verbose`` attribute

v3.0.1 (2019-10-31)
  - Some adaptation for using Infiniium oscilloscopes with limited functionality
  - Expanding the contents of the ``list_visa_devices`` table
  - Bugfix for ascii data processing (originating in v3.0.0)

v3.0.0 (2019-10-28)
  - Expanded command line programmes to take many more options:

    - *Connection settings*: visa_address, timeout
    - *Acquiring settings*: channels, acq_type
    - *Transfer and storage settings*: wav_format, num_points, filename, file_delimiter

  - Added ``Oscilloscope.generate_file_header()`` to generate file header with structure::

      <id>
      <mode>,<averages>
      <timestamp>
      time,<chs>

    Now used by ``save_trace()``

  - *No compatibility*: Camel case in function names is no more

    * ``getTrace`` -> ``get_trace``
    * ``saveTrace`` -> ``save_trace``
    * ``plotTrace`` -> ``plot_trace``
    * and others

  - *No compatibility*: ``Oscilloscope.build_sourcesstring()`` ->
    ``Oscilloscope.determine_channels()`` and changed return sequence

  - *No compatibility*: module ``installed_commandline_funcs`` -> ``installed_cli_programmes``

  - *No compatibility*: functions ending with ``_command_line()`` -> ``_cli()``

  - Fixed issue when setting number of points to transfer

  - Fixed issue (hopefully) with sometimes getting wrong traces exported. Have
    now set communication to signed ints, and setting least significant bit first

  - Fixed issue where ``ASCii`` wave format would set zero time to the beginning of the trace

  - Wrote comprehensive documentation on read the docs



v2.1: May I have your address?
------------------------------
New command line programmes for listing visa devices and finding config

v2.1.0 (2019-10-18)
  - Added command line programme ``list_visa_devices`` to list the addresses
    of the VISA instruments available
  - Added command line programme ``path_of_config`` to show the path of ``config.py``
  - Explicitly setting scope to transfer in unsigned ints when doing ``BYTE``
    and ``WORD`` waveform formats
  - Added functions for setting oscilloscope to running and stopped, and for
    direct VISA command write and query
  - Changed dependency from visa to pyvisa (the package called visa on pypi is
    not pyvisa..!), and added tqdm dependency
  - *No compatibility*: ``get_n_traces`` now called ``get_num_traces``
  - And minor cosmetic changes



v2.0: Labels for everyone
-------------------------

v2.0.1 (2019-09-13)
  - Cosmetic change in README, clarifying changelog for previous version


v2.0.0 (2019-08-29)
  - When using ``Oscilloscope.set_options_get_trace_save()``, channels are now
    comma separated in the csv to provide channel headings according to the data
    columns. This is not directly compatible with previous versions as these had
    two lines of preamble in csvs, whereas it is now three (Instrument info,
    columns descriptions, date and time)
  - Added BYTE/WORD issue to README



v1.1: Need for speed
--------------------
Order of magnitude speed-up in data processing, logging enabled, new command
line programme

v1.1.1 (2019-08-14)
  - Logging gives elapsed time in milliseconds
  - Change in logging level for elapsed time


v1.1.0 (2019-04-04)
  - Added command line programme for obtaining a given number of traces consecutively
  - Former debugging print is now directed to ``logging.debug()``
  - ``Oscilloscope.process_data_binary()`` is approx an order of magnitude faster
  - Added license file
  - Changes in README



v1.0: Hello world
-----------------

v1.0 (2019-03-07)
  - First release on pypi
