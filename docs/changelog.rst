Changelog
=========

v4.0: Extreme (API) makeover
----------------------------
Big makeover with many non-compatible changes (sorry).

When writing the base of this package back in 2019, I had very limited Python
development experience, and some not so clever choices were made. It was time
to make clear these up and make the API easier to use.

That means that there are quite a few non-compatible changes to previous versions,
all of which are detailed below. I am not planning further extensive revisions
like this.

v4.0.0 (2021-01)
  - More attributes are used to make the information accessible not only through
    returns

    * Captured data stored to ``Oscilloscope._time`` and ``Oscilloscope._values``
    * The filename finally used when saving (which might not be the same as the
      the argument passed as a filename check happens to avoid overwrite) is
      stored in ``Oscilloscope.fname``
    * ``Oscilloscope._raw`` and ``Oscilloscope._metadata`` with unprocessed data

  - More active use of attributes that are carried forward rather than always
    setting the arguments of methods in the ``Oscilloscope`` class. This
    affects some functions as their arguments have changed (see below), but
    for most functions the arguments stay the same as before. The arguments
    can now be used to change attributes of the ``Oscilloscope`` instance.

  - ``Oscilloscope.__init__`` and other functions will no longer use default
    settings in ``keyoscacquire.config`` that changes the settings of the
    *Oscilloscope*, like active channels and acquisition type, but only set
    default connection and transfer settings

  - Changed the name of the module ``oscacq`` to ``oscilloscope`` and moved
    functions not within the ``Oscilloscope`` class to other modules, see
    details below

  - Bugfixes and docfixes for the number of points to be transferred from the
    instrument (previously ``num_points`` argument, now a property). Zero will
    set the to the maximum number of points available, and the number of
    points can be queried.

  - Moved save and plot functions to ``keyoscacquire.fileio``, but are imported
    in the ``oscilloscope`` (prev ``oscacq``) module to keep compatibility

  - New ``keyoscacquire.fileio.load_trace()`` function for loading saved a trace
    from disk to pandas dataframe or numpy array

  - ``Oscilloscope.query()`` will now try to read the error from the
    instrument if pyvisa fails

  - Importing ``keyoscacquire.programmes`` in module ``init.py`` to make it
    accessible after importing the module

  - Changes in ``list_visa_devices`` and cli programme: now displaying different
    errors more clearly; cli programme now has ``-n`` flag that can be set to not
    ask for instrument IDNs; and the cli programme will display the instrument's
    serial rather than Keysight model series.

  - Indicating functions for internal use only and read only attributes with
    prefix ``_``, see name changes below

  - Documentation updates, including moving from read-the-docs theme to Furo theme

  - PEP8 improvements

  - *New methods*:

    * ``Oscilloscope.get_error()``
    * ``Oscilloscope.set_waveform_export_options()``
    * ``Oscilloscope.save_trace()`` (``Oscilloscope.savepng`` and
      ``Oscilloscope.showplot`` can be set to control its behaviour)
    * ``Oscilloscope.plot_trace()``

  - *New properties*: New properties getters querying the instrument for the
    current state and setters to change the state

    * ``Oscilloscope.active_channels``
    * ``Oscilloscope.acq_type``
    * ``Oscilloscope.num_averages``
    * ``Oscilloscope.p_mode``
    * ``Oscilloscope.num_points``
    * ``Oscilloscope.wav_format``
    * ``Oscilloscope.timeout`` (this affects the pyvisa resource, not the scope
      itself)

  - *No compatibility*: Name changes

    * module ``oscacq`` to ``oscilloscope``
    * ``Oscilloscope.determine_channels()`` -> ``Oscilloscope.set_channels_for_capture()``
    * ``Oscilloscope.acquire_print`` -> ``Oscilloscope.verbose_acquistion``
    * ``Oscilloscope.set_acquire_print()`` set ``Oscilloscope.verbose_acquistion``
      attribute instead
    * ``Oscilloscope.capture_and_read_ascii()`` -> ``Oscilloscope._read_ascii()``
      (also major changes in the function)
    * ``Oscilloscope.capture_and_read_binary()`` -> ``Oscilloscope._read_binary()``
      (also major changes in the function)
    * ``Oscilloscope.inst`` -> ``Oscilloscope._inst``
    * ``Oscilloscope.id`` -> ``Oscilloscope._id``
    * ``Oscilloscope.address`` -> ``Oscilloscope._address``
    * ``Oscilloscope.model`` -> ``Oscilloscope._model``
    * ``Oscilloscope.model_series`` -> ``Oscilloscope._model_series``
    * ``oscacq._screen_colors`` -> ``fileio._SCREEN_COLORS``

  - *No compatibility*: Moved functions and attributes

    * ``check_file()`` from ``oscacq`` to ``fileio``
    * ``interpret_visa_id()`` from ``oscacq`` to ``visa_utils``
    * ``process_data()`` (as well as ``_process_data_ascii`` and
      ``_process_data_binary``) from ``oscacq`` to ``dataprocessing``
    * ``_SCREEN_COLORS`` (prev. ``_screen_colors``) from ``oscacq`` to ``fileio``

  - *No compatibility*: Some functions no longer take ``sources`` and
    ``sourcesstring`` as arguments, rather ``Oscilloscope._sources`` must be set by
    ``Oscilloscope.set_channels_for_capture()`` and ``sourcesstring`` is not in
    use anymore

    * ``Oscilloscope.capture_and_read()``, and its associated
      ``Oscilloscope._read_ascii()`` and ``Oscilloscope._read_binary()``
    * ``Oscilloscope.get_trace()``

  - *No compatibility*: Misc

    * ``Oscilloscope.get_trace()`` now also returns ``Oscilloscope.num_channels``
    * ``Oscilloscope.get_active_channels()`` is now a property ``active_channels``
      and returns a list of ints, not chars
    * ``keyoscacquire.config`` does not have the ``_acq_type``, ``_num_avg``,
      and ``_ch_nums`` static variables anymore as these will not be used
    * ``keyoscacquire.config`` has two new static variables, ``_num_points``
      and ``_p_mode``



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
