# Keysight oscilloscope acquire package


v2.1.0 // October 2019 // Andreas Svela

## Overview

keyoscacquire is a Python package for acquiring traces from Keysight oscilloscopes through a VISA interface.

*Documentation available [here](http://).*

Based on [PyVISA](https://pyvisa.readthedocs.io/en/latest/), keyoscacquire provides programmes for acquiring and exporting traces to your choice of ASCII format files (default csv) and a png of the trace plot. The package's :py:class:`Oscilloscope` and data processing functions can also be used in other scrips, for example, to capture the active channels on an oscilloscope connected with VISA address ``USB0::1234::1234::MY1234567::INSTR``

```python
   >>> import keyoscacq as koa
   >>> osc = koa.Oscilloscope(address='USB0::1234::1234::MY1234567::INSTR')
   >>> time, y, channel_numbers = osc.set_options_get_trace()
```

where ``time`` is a vertical numpy vector of time values and ``y`` is a numpy array which columns contain the data from the channels in ``channel_numbers``.

If you need to find the VISA address of your oscilloscope, use the command line function ``list_visa_devices`` provided by this package.

The code has been tested on Windows 7 and 10 with a Keysight DSO2024A model using a USB connection.

### Very quick reference

Command line functions
- `path_of_config`: find the path of the `config.py` file storing default options. Change this to your choice of standard settings.
- `list_visa_devices`: list the available VISA devices
- `get_single_trace`: use with option `-h` for instructions
- `get_num_traces`: get a set number of traces, use with option `-h` for instructions
- `get_traces_single_connection`: get a trace each time enter is pressed, use with option `-h` for instructions


## Installation

Install the package with pip:

```bash
$ pip install keysightoscilloscopeacquire
```

or download locally and install with `$ python setup.py install` or by running `install.bat`.

## Known issues/suggested improvements

- Known issue: Sometimes `WORD` waveform does not give the correct trace data, just random noise (but switching to `ASCii` or `BYTE` gives correct traces). If this happens, open *KeySight BenchVue* and obtain one trace through the software. Now try to obtain a trace through this package -- it should now work again using `WORD`.
- Add optional argument to supply visa address of instrument to command line executables and scripts
