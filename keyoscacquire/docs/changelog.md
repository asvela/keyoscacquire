# Changelog

- v2.0.0: When using set_options_getTrace_save(), channels are now comma separated in the csv to provide channel headings according to the data columns. This is not directly compatible with previous versions as these had two lines of preamble in csvs, whereas it is now three (Instrument info, columns descriptions, date and time). Also added a known issue to README
- v1.1.1: Logging gives elapsed time in milliseconds, change in logging level for elapsed time
- v1.1.0: Extra command line function, logging enabled, order of magnitude speed-up in data processing
  - Added command line function for obtaining a given number of traces consecutively
  - Former debugging print is now directed to logging.debug()
  - process_data_binary() is approx an order of magnitude faster
  - Added license file
  - Changes in README
- v1.0.0: First release
