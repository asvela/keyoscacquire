# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from Keysight oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

This program captures a single trace and stores it.

Optional argument from the command line: string setting the base filename of the output files.
Change the config._visa_address under default options to the desired instrument.
"""

import keyoscacquire.installed_command_line_funcs as cli

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    cli.single_trace_command_line()
