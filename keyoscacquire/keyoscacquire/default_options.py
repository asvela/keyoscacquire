# Default options
VISA_ADDRESS = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
WAVEFORM_FORMAT = 'WORD'        # WORD formatted data is transferred as 16-bit uint.
                                # BYTE formatted data is transferred as 8-bit uint.
                                # ASCii formatted data converts the internal integer data values to real Y-axis values.
                                #       Values are transferred as ASCii digits in floating point notation, separated by commas.
CH_NUMS = ['']                  # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
ACQ_TYPE = "HRESolution"# {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [1, 65536]
NUM_AVG = 2             # default number of averages used if only AVER is given as acquisition type
FILENAME = "data"       # default base filename of all traces and pngs exported, a number is appended to the base
FILE_DELIMITER = " n"   # delimiter used between FILENAME and filenumber (before FILETYPE)
FILETYPE = ".csv"       # filetype of exported data, can also be txt/dat etc.
EXPORT_PNG = True       # export png of plot of obtained trace
SHOW_PLOT = False       # show each plot when generated (program pauses until it is closed)
TIMEOUT = 15000         #ms timeout for the instrument connection
