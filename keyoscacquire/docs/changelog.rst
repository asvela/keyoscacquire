Changelog
=========


v3.0.0 (2019-10-XX)
-------------------

- Camel case in function names is no more (no compatibility measures introduced)

  * ``getTrace`` -> ``get_trace``
  * ``saveTrace`` -> ``save_trace``
  * ``plotTrace`` -> ``plot_trace``
  * and others

- Wrote comprehensive documentation



v2.1.1 (2019-10-18)
-------------------

- Added command line function ``list_visa_devices`` to list the addresses of the VISA instruments available

- Added command line function ``path_of_config`` to show the path of config.py

- Explicitly setting scope to transfer in unsigned ints when doing ``BYTE`` and ``WORD`` waveform formats

- Changed dependency from visa to pyvisa (the package called visa on pypi is not pyvisa..!), and added tqdm dependency

- ``get_n_traces`` now called ``get_num_traces``

- And minor cosmetic changes


v2.0.1 (2019-09-13)
-------------------
- Cosmetic change in README, clarifying changelog for previous version


v2.0.0 (2019-08-29)
-------------------
- When using ``set_options_get_trace_save()``, channels are now comma separated in the csv to provide channel headings according to the data columns. This is not directly compatible with previous versions as these had two lines of preamble in csvs, whereas it is now three (Instrument info, columns descriptions, date and time)

- Added BYTE/WORD issue to README


v1.1.1 (2019-08-14)
-------------------
- Logging gives elapsed time in milliseconds

- Change in logging level for elapsed time


v1.1.0 (2019-04-04)
-------------------
Extra command line function, logging enabled, order of magnitude speed-up in data processing

  - Added command line function for obtaining a given number of traces consecutively

  - Former debugging print is now directed to ``logging.debug()``

  - ``process_data_binary()`` is approx an order of magnitude faster

  - Added license file

  - Changes in README


v1.0.0 (2019-03-07): First release
----------------------------------
