## KeysightOscilloscopeAcquiring package

22th November 2018

The code in this repository connects to (Keysight) oscilloscopes through a VISA interface and exports traces as a chosen ASCII format file and a png of the trace plot. The python library pyVISA is used and the code has been tested on a Keysight DSO2024A model using a USB connection.

#### Known issues

- The code does not work with the Tektronix oscilloscope in the lab as Tektronix uses slightly different VISA commands :no_good:

#### Usage

The code is structured as a module `acquire.py`, and two command line programmes `getTraces_connect_each_time_loop.py` and `getTraces_single_connection_loop.py` that loads the module and uses its functions. **In order to connect to a VISA instrument, NI MAX or similar must be running on the computer.** The VISA address of the instrument can be found in NI MAX, and should be set as the  `VISA_ADDRESS` variable, see below.

Both programmes are loops for which every time enter is hit a trace will be obtained and exported as csv and png files with successive numbering. By default all active channels on the oscilloscope will be captured (this can be changed, see below). The difference between the two is that the first programme is establishing a new connection to the instrument each time a trace is captured, whereas the second opens a connection to start with and does not close the connection until the program is quit. The second programme only checks which channels are active when it connects, i.e. the first programme will save only the currently active channels for each saved trace; the first will each time save the channels that were active at the time of starting the programme.

##### Default options

The command line programmes will by default save traces in the programme folder as `data<n>.csv`and `data<n>.png`; however, the trace file type and base file name and other options can be set in the global[^1] variables in the beginning of each programme file:

[^1]: None of the functions access the global variables directly, but they are feed them as default arguments.

```python
# default options
VISA_ADDRESS = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
WAVEFORM_FORMAT = 'WORD'    # WORD formatted data is transferred as 16-bit uint.
                            # BYTE formatted data is transferred as 8-bit uint.
                            # ASCii formatted data converts the internal integer data values to real Y-axis values.
                            #       Values are transferred as ASCii digits in floating point notation, separated by commas.
CH_NUMS=['']        # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
DEFAULT_FILENAME = "data" # default base filename of all traces and pngs exported, a number is appended to the base
FILETYPE = ".csv"   # filetype of exported data, can also be txt/dat etc.
TIMEOUT = 15000     #ms timeout for the instrument connection
```

The `WAVEFORM_FORMAT` dictates whether 16/8 bit raw values or comma separated ascii voltage values should be transferred when the waveform is queried for (the output file will be ascii anyway, this is simply a question of how the data is transferred to and processed on the computer). Raw values format is approx. 10x faster than ascii.

##### Optional argument sets file name, check if file already exists

Furthermore, both programmes takes in an optional string argument that is set as the base file name, i.e. the command line code

```bash
$ python getTraces_single_connection_loop.py "measurement"
```
will give output files `measurement<n>.csv` and `measurement<n>.png`.  The programmes will check if the file `"measurement0"+FILETYPE` exists, and if it does, prompt the user for something to append to `measurement` until `"measurement"+appended+"0"+FILETYPE` is not an existing file. *The same checking procedure applies also when no base filename is supplied and `DEFAULT_FILENAME` is used.*

##### Obtaining single traces

Also `acquire.py` can be run from the command line, resulting in one trace being obtained from the active channels. This provides a way to specify directly the filename of each trace, rather than having consecutive numbering appended to a base filename. The filename check is used here as well, but now without appending the zero to the base name before checking.

##### Obtaining traces when the scope is running vs when stopped

When the scope **is running** the `capture_and_read`functions will obtain a trace by running `:DIGitize`, causing the instrument to acquire a trace and then stop the oscilloscope. When the scope **is stopped** the current trace on the screen of the oscilloscope will be captured (*Warning:* This might mean the settings specified with `:ACQire` are not used, i.e. acquiring mode and number of points to be captured).

The scope will always be set to running after a trace is captured.
