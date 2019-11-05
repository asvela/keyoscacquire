# Keysight oscilloscope acquire package

<br>
<br>
<br>
<br>

## This package has now moved to [keyoscacquire](https://pypi.org/project/keyoscacquire/), and the new package's documentation can be found on [read the docs](https://keyoscacquire.rtfd.io). The source is on [github](https://github.com/asvela/keyoscacquire/).

<br>
<br>
<br>
<br>
<br>

# Readme for this version

v2.0.1 // August 2019 // Andreas Svela

## Overview

This package gives functionality for acquiring traces from Keysight oscilloscopes through a VISA interface, and exports traces as a chosen ASCII format file (default csv) and a png of the trace plot. The Python library `pyvisa` is used for communication. The code has been tested on a Keysight DSO2024A model using a USB connection.

The code is structured as a module `keyoscacquire/oscacq.py` containing the engine doing `pyvisa` interfacing in a class `Oscilloscope`, and support functions for data processing/saving. Programmes are located in `keyoscacquire/programmes.py`.  Default options are found in `keyoscacq/config.py`, the files in `/scripts` can be ran from the command line and are essentially the same running the installed executables.

## Installation

Install the package with pip:

```bash
$ pip install keysightoscilloscopeacquire
```

or download locally and install with `$ python setup.py install` or by running `install.bat`.

#### Default options

The package is installed with a set of default options found in `keyoscacq/config.py`:

```python
# Default options in config.py
_visa_address = 'USB0::XXXX::XXXX::MYXXXXXXXX::INSTR' # address of instrument
_waveform_format = 'WORD' # WORD formatted data is transferred as 16-bit uint.
                          # BYTE formatted data is transferred as 8-bit uint.
                          # ASCii formatted data converts the internal integer data values to real Y-axis values.
                          #       Values are transferred as ASCii digits in floating point notation, separated by commas.
_ch_nums = ['']           # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
_acq_type = "HRESolution" # {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [1, 65536]
_num_avg = 2              # default number of averages used if only AVER is given as acquisition type
_filename = "data"        # default base filename of all traces and pngs exported, a number is appended to the base
_file_delimiter = " n"    # delimiter used between _filename and filenumber (before _filetype)
_filetype = ".csv"        # filetype of exported data, can also be txt/dat etc.
_export_png = True        # export png of plot of obtained trace
_show_plot = False        # show each plot when generated (program pauses until it is closed)
_timeout = 15000          # ms timeout for the instrument connection
```

For changes to these defaults to take effect, the package must be reinstalled locally after doing the changes in `config.py`, simply by navigating to the directory containing `setup.py` and running `$ python setup.py install` or `install.bat`. **Note** that none of the functions access the global variables directly, but they are feed them as default arguments.

The `_waveform_format` dictates whether 16/8 bit raw values or comma separated ascii voltage values should be transferred when the waveform is queried for (the output file will be ascii anyway, this is simply a question of how the data is transferred to and processed on the computer). Raw values format is approx. 10x faster than ascii.

The command line programmes will save traces in the folder from where they are ran as`_filename+_file_delimiter+<n>+_filetype`, i.e. by default as `data n<n>.csv`and `data n<n>.png`.

## Known issues/suggested improvements

- Known issue: Sometimes `WORD` waveform does not give the correct trace data, just random noise (but switching to `ASCii` or `BYTE` gives correct traces). If this happens, open *KeySight BenchVue* and obtain one trace through the software. Now try to obtain a trace through this package -- it should now work again using `WORD`.
- Add optional argument to supply visa address of instrument to command line executables and scripts

## Usage

**In order to connect to a VISA instrument, NI MAX or similar might need to be running on the computer.** The VISA address of the instrument can be found in NI MAX, and should be set as the `_visa_address` variable, see below, before installation.

Four command line programmes `get_single_trace`, `get_num_traces`, `getTraces_connect_each_time` and `getTraces_single_connection` can be ran directly from the command line after installation (i.e. from whatever folder and no need for `$ python [...].py`).

The two first programmes will obtain one and a specified number of traces, respectively. The two latter programmes are loops for which every time `enter` is hit a trace will be obtained and exported as csv and png files with successive numbering. By default all active channels on the oscilloscope will be captured (this can be changed, see below). The difference between the two latter programmes is that the first programme is establishing a new connection to the instrument each time a trace is to be captured, whereas the second opens a connection to start with and does not close the connection until the program is quit. The second programme only checks which channels are active when it connects, i.e. the first programme will save only the currently active channels for each saved trace; the second will each time save the channels that were active at the time of starting the programme.


### Optional command line argument sets base filename, acquiring mode or number of traces to obtain

Furthermore, both programmes takes up to two optional arguments:
`-f "custom filename"` set as the base filename to "custom filename"
`-a AVER8`  sets acquiring type to average with eight traces
`-n 10` sets number of traces to obtain (only for `get_num_traces`)

For example
```bash
$ getTraces_single_connection_loop -f measurement
```
will give output files `measurement n<n>.csv` and `measurement n<n>.png`.  The programmes will check if the file `"measurement"+_file_delimiter+num+_filetype)` exists, and if it does, prompt the user for something to append to `measurement` until `"measurement"+appended+"0"+_filetype` is not an existing file. *The same checking procedure applies also when no base filename is supplied and `DEFAULT_FILENAME` is used.*

### Obtaining single traces

Running the module with `$ python -m keyoscacquire` obtains and saves a trace with default options being used. Alternatively, the filename and acquisition type can be specified as per the paragraph above using the  executable, e.g. `$ get_single_trace -f "fname" -a "AVER"`.

### Obtaining traces when the scope is running vs when stopped

When the scope **is running** the `capture_and_read` functions will obtain a trace by running `:DIGitize`, causing the instrument to acquire a trace and then stop the oscilloscope. When the scope **is stopped** the current trace on the screen of the oscilloscope will be captured (*Warning:* This might mean the settings specified with `:ACQuire` are not used, i.e. acquiring mode and number of points to be captured).

The scope will always be set to running after a trace is captured.


### Scripts in ./scripts

These can be ran as command line scripts from the folder with `$ python [script].py`. Optional arguments for filename and acquisition mode can be used, such as `$ python [script].py "otherFileName"`, or `$ python [script].py "otherFileName" "AVER8"`. Note, no flag specifiers are needed (or allowed) and the sequence of arguments is fixed.


### Logging

The module gives output for debugging through `logging`. The output can be directed to the terminal by adding the following to the top level file using the keyoscacquire package
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
or directed to a file `mylog.log` with
```python
import logging
logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
```
