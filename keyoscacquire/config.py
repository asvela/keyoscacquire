# -*- coding: utf-8 -*-
"""Default options for keyoscacquire"""

#: VISA address of instrument
_visa_address = 'USB0::1234::1234::MY1234567::INSTR'
#: Waveform format transferred from the oscilloscope to the computer
#: WORD formatted data is transferred as 16-bit uint.
#: BYTE formatted data is transferred as 8-bit uint.
#: ASCii formatted data converts the internal integer data values to real Y-axis values. Values are transferred as ASCii digits in floating point notation, separated by commas.
_waveform_format = 'WORD'
#: The acqusition type
#: {HRESolution, NORMal, AVER<m>} where <m> is the number of averages in range [2, 65536]
_acq_type = "HRESolution"
#: Points mode of the oscilloscope: ``'NORMal'`` is limited to 62,500 points,
#: whereas ``'RAW'`` gives up to 1e6 points.
#: {RAW, MAX, NORMal}
_p_mode = 'RAW'
#: Number of points to transfer to the computer
#: zero gives maximum
_num_points = 0
#: Default base filename of all traces and pngs exported, a number is appended to the base
_filename = "data"
#: Delimiter used between :attr:`_filename` and filenumber (before :attr:`_filetype`)
_file_delimiter = " n"
#: filetype of exported data, can also be txt/dat etc.
_filetype = ".csv"
#: export png of plot of obtained trace
_export_png = True
#: show each plot when generated (program pauses until it is closed)
_show_plot = False
#: ms timeout for the instrument connection
_timeout = 15000
