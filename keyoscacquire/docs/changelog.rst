Changelog
=========


v3.0.0 (2019-10-XX)
-------------------

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

- Camel case in function names is no more *(no compatibility measures introduced)*

  * ``getTrace`` -> ``get_trace``
  * ``saveTrace`` -> ``save_trace``
  * ``plotTrace`` -> ``plot_trace``
  * and others

- Fixed issue when setting number of points to transfer

- Wrote comprehensive documentation

- *(No compatibility measures introduced)*: ``Oscilloscope.build_sourcesstring()`` -> ``Oscilloscope.determine_channels()`` and changed return sequence

- Fixed issue with unreliable data transfer from scope. Have now set communication to signed ints

- Fixed issue where ``ASCii`` wave format would set zero time to the beginning of the trace


v2.1.1 (2019-10-18)
-------------------

- Added command line programme ``list_visa_devices`` to list the addresses of the VISA instruments available

- Added command line programme ``path_of_config`` to show the path of config.py

- Explicitly setting scope to transfer in unsigned ints when doing ``BYTE`` and ``WORD`` waveform formats

- Added functions for setting oscilloscope to running and stopped, and for direct VISA command write and query

- Changed dependency from visa to pyvisa (the package called visa on pypi is not pyvisa..!), and added tqdm dependency

- ``get_n_traces`` now called ``get_num_traces``

- And minor cosmetic changes


v2.0.1 (2019-09-13)
-------------------
- Cosmetic change in README, clarifying changelog for previous version


v2.0.0 (2019-08-29)
-------------------
- When using ``Oscilloscope.set_options_get_trace_save()``, channels are now comma separated in the csv to provide channel headings according to the data columns. This is not directly compatible with previous versions as these had two lines of preamble in csvs, whereas it is now three (Instrument info, columns descriptions, date and time)

- Added BYTE/WORD issue to README


v1.1.1 (2019-08-14)
-------------------
- Logging gives elapsed time in milliseconds

- Change in logging level for elapsed time


v1.1.0 (2019-04-04)
-------------------
Extra command line programme, logging enabled, order of magnitude speed-up in data processing

  - Added command line programme for obtaining a given number of traces consecutively

  - Former debugging print is now directed to ``logging.debug()``

  - ``Oscilloscope.process_data_binary()`` is approx an order of magnitude faster

  - Added license file

  - Changes in README


v1.0.0 (2019-03-07): First release
----------------------------------
