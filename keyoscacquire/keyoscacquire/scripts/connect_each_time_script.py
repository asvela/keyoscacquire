# -*- coding: utf-8 -*-
"""
Obtain traces, save to files and export raw plots from Keysight oscilloscopes using pyVISA.
Traces are stored as csv files and will by default be accompanied by a png plot too.

This program consists of a loop in which the program connects to the oscilloscope,
a trace from the active channels are captured and stored for each loop. This permits
the active channels to be changing thoughout the measurements, but has larger
overhead due to establishing and closing a new connection every time.

The loop runs each time 'enter' is hit. Alternatively one can input n-1 characters before hitting
'enter' to capture n traces back to back. To quit press 'q'+'enter'.

Optional argument from the command line: string setting the base filename of the output files.
Change the config._visa_address under default options to the desired instrument.
"""

import keyoscacquire.installed_cli_programmes as cli

## Main function, runs only if the script is called from the command line
if __name__ == '__main__':
    cli.connect_each_time_cli()
