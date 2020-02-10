Changelog
=========

v3.0: Docs are overrated
------------------------
Comprehensive documentation now available on read the docs, added more command line programme options, some function name changes without compatibility, and bug fixes.

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

    * *Connection settings*: visa_address, timeout
    * *Acquiring settings*: channels, acq_type
    * *Transfer and storage settings*: wav_format, num_points, filename, file_delimiter

  - Added ``Oscilloscope.generate_file_header()`` to generate file header with structure::

          <id>
          <mode>,<averages>
          <timestamp>
          time,<chs>

    Now used by ``save_trace()``

  -  *(No compatibility measures introduced)*: Camel case in function names is no more

    * ``getTrace`` -> ``get_trace``
    * ``saveTrace`` -> ``save_trace``
    * ``plotTrace`` -> ``plot_trace``
    * and others

  - *(No compatibility measures introduced)*: ``Oscilloscope.build_sourcesstring()`` -> ``Oscilloscope.determine_channels()`` and changed return sequence

  - *(No compatibility measures introduced)*: module ``installed_commandline_funcs`` -> ``installed_cli_programmes``

  - *(No compatibility measures introduced)*: functions ending with ``_command_line()`` -> ``_cli()``

  - Fixed issue when setting number of points to transfer

  - Fixed issue (hopefully) with sometimes getting wrong traces exported. Have now set communication to signed ints, and setting least significant bit first

  - Fixed issue where ``ASCii`` wave format would set zero time to the beginning of the trace

  - Wrote comprehensive documentation on read the docs


v2.1: May I have your address?
------------------------------
New command line programmes for listing visa devices and finding config

v2.1.0 (2019-10-18)
  - Added command line programme ``list_visa_devices`` to list the addresses of the VISA instruments available

  - Added command line programme ``path_of_config`` to show the path of config.py

  - Explicitly setting scope to transfer in unsigned ints when doing ``BYTE`` and ``WORD`` waveform formats

  - Added functions for setting oscilloscope to running and stopped, and for direct VISA command write and query

  - Changed dependency from visa to pyvisa (the package called visa on pypi is not pyvisa..!), and added tqdm dependency

  - *(No compatibility measures introduced)*: ``get_n_traces`` now called ``get_num_traces``

  - And minor cosmetic changes


v2.0: Labels for everyone
-------------------------

v2.0.1 (2019-09-13)
  - Cosmetic change in README, clarifying changelog for previous version


v2.0.0 (2019-08-29)
  - When using ``Oscilloscope.set_options_get_trace_save()``, channels are now comma separated in the csv to provide channel headings according to the data columns. This is not directly compatible with previous versions as these had two lines of preamble in csvs, whereas it is now three (Instrument info, columns descriptions, date and time)

  - Added BYTE/WORD issue to README


v1.1: Need for speed
--------------------

v1.1.1 (2019-08-14)
  - Logging gives elapsed time in milliseconds

  - Change in logging level for elapsed time


v1.1.0 (2019-04-04)
  Extra command line programme, logging enabled, order of magnitude speed-up in data processing

    - Added command line programme for obtaining a given number of traces consecutively

    - Former debugging print is now directed to ``logging.debug()``

    - ``Oscilloscope.process_data_binary()`` is approx an order of magnitude faster

    - Added license file

    - Changes in README


v1.0: Hello world
-----------------

v1.0 (2019-03-07)
  - First release on pypi
