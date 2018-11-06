## pyVISA oscilloscope trace acquiring

6th November 2018

The code in this repository connects to oscilloscopes through a VISA interface and exports traces as a chosen ASCII format file and a png of the trace plot. The python library pyVISA is used and the code has been tested on a Keysight DSO2024A model using a USB connection.

#### Known issues

- The code does not work with the Tektronix oscilloscope in the lab, maybe this is due to the TCPIP connection. USB has not been tried yet for that instrument.
- The Keysight oscilloscope is slow on exporting data (the `query(WAVEFORM?)` command takes a long time to complete)
  - Could try the `WORD` rather than `ASCii` waveform export type 
  - Exporting to a USB stick rather than to the computer has been tried, but it does not speed up the acquisition

#### Usage

The code is structured as a Module `acquire.py`, and two command line programmes `getTraces_connect_each_time_loop.py` and `getTraces_single_connection_loop.py` that loads the module and uses its functions. **In order to connect to a VISA instrument, NI MAX or similar must be running on the computer.** The VISA address of the instrument can be found in NI MAX, and should be set as the  `VISA_ADDRESS` variable, see below. 

Both programmes are loops for which every time enter is hit a trace will be obtained and exported as csv and png files with successive numbering. By default all active channels on the oscilloscope will be captured (this can be changed, see below). The difference between the two is that the first programme is establishing a new connection to the instrument each time a trace is captured, whereas the second opens a connection to start with and does not close the connection until the program is quit. The second programme only checks which channels are active when it connects, i.e. the first programme will save only the currently active channels for each saved trace; the first will each time save the channels that were active at the time of starting the programme.

The command line programmes will by default save traces in the programme folder as `data<n>.csv`and `data<n>.png`; however, the trace file type and base file name and other options can be set in the global[^1] variables in the beginning of each programme file:

[^1]: None of the functions access the global variables directly, but they are feed them as default arguments.

```python
# default options
VISA_ADDRESS = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
CH_NUMS=['']        # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
DEFAULT_FILENAME = "data" # default base filename of all traces and pngs exported, a number is appended to the base
FILETYPE = ".csv"   # filetype of exported data, can also be txt/dat etc.
TIMEOUT = 15000     #ms timeout for the instrument connection
```

Furthermore, both programmes takes in an optional string argument that is set as the base file name, i.e. the command line code `python getTraces_single_connection_loop.py "measurement"` will give output files `measurement<n>.csv` and `measurement<n>.png`.