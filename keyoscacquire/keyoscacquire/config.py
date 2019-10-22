# -*- coding: utf-8 -*-
# Default options for keyoscacquire
_visa_address = 'USB0::2391::6038::MY57233636::INSTR' # address of instrument
_waveform_format = 'WORD' # WORD formatted data is transferred as 16-bit uint.
                          # BYTE formatted data is transferred as 8-bit uint.
                          # ASCii formatted data converts the internal integer data values to real Y-axis values.
                          #       Values are transferred as ASCii digits in floating point notation, separated by commas.
_ch_nums = ['']           # list of chars, e.g. ['1', '3']. Use a list with an empty string [''] to capture all currently displayed channels
_acq_type = "HRESolution" # {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536]
_num_avg = 2              # default number of averages used if only AVER is given as acquisition type
_filename = "data"        # default base filename of all traces and pngs exported, a number is appended to the base
_file_delimiter = " n"    # delimiter used between _filename and filenumber (before _filetype)
_filetype = ".csv"        # filetype of exported data, can also be txt/dat etc.
_export_png = True        # export png of plot of obtained trace
_show_plot = False        # show each plot when generated (program pauses until it is closed)
_timeout = 15000          # ms timeout for the instrument connection
