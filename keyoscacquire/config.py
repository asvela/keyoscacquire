# -*- coding: utf-8 -*-
"""Default options for keyoscacquire"""

#: VISA address of instrument
_visa_address = 'USB0::1234::1234::MY1234567::INSTR'
#: waveform format transferred from the oscilloscope to the computer
#: WORD formatted data is transferred as 16-bit uint.
#: BYTE formatted data is transferred as 8-bit uint.
#: ASCii formatted data converts the internal integer data values to real Y-axis values. Values are transferred as ASCii digits in floating point notation, separated by commas.
_waveform_format = 'WORD'
#: list of chars, e.g. ['1', '3'], or 'active' to capture all currently displayed channels
_ch_nums = 'active'
#: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536]
_acq_type = "HRESolution"
#: default number of averages used if only AVER is given as acquisition type
_num_avg = 2
#: default base filename of all traces and pngs exported, a number is appended to the base
_filename = "data"
#: delimiter used between :attr:`_filename` and filenumber (before _filetype)
_file_delimiter = " n"
#: filetype of exported data, can also be txt/dat etc.
_filetype = ".csv"
#: export png of plot of obtained trace
_export_png = True
#: show each plot when generated (program pauses until it is closed)
_show_plot = False
#: ms timeout for the instrument connection
_timeout = 15000
