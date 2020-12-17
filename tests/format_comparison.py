# -*- coding: utf-8 -*-
"""
Script to test obtaining data with different waveform formats for Keysight DSO2024A

Andreas Svela // 2019
"""

visa_path = 'C:\\Program Files\\IVI Foundation\\VISA\\Win64\\agvisa\\agbin\\visa32.dll'
visa_address = 'USB0::0x0957::0x1796::MY59125372::INSTR'


import pyvisa
import numpy as np
import matplotlib.pyplot as plt

import keyoscacquire as koa

format_dict = {0: "BYTE", 1: "WORD", 4: "ASCii"}
formats = ['BYTE', 'WORD', 'ASCii']


print("\n## ~~~~~~~~~~~~~~~~~ KEYOSCAQUIRE ~~~~~~~~~~~~~~~~~~ ##")

scope = koa.Oscilloscope(address=visa_address)
scope.set_acquiring_options(num_points=2000)
scope.set_channels_for_capture(channel_nums=['1'])
scope.stop()

times, values = [[], []], [[], []]
for wav_format in formats:
    print("\nWaveform format", wav_format)
    scope.set_acquiring_options(wav_format=wav_format)
    scope.capture_and_read(set_running=False)
    time, vals = koa.process_data(scope.raw, scope.metadata, wav_format, acquire_print=True)
    times[0].append(time)
    values[0].append(vals)

scope.close(set_running=False)


print("\n## ~~~~~~~~~~~~~~~~~~~ PYVISA ~~~~~~~~~~~~~~~~~~~~~ ##")

# use Keysight VISA and connect to instrument
rm = pyvisa.ResourceManager(visa_path)
inst = rm.open_resource(visa_address)
inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
id = inst.query('*IDN?').strip() # get the id of the connected device
print("Connected to\n\t\'%s\'" % id)

# obtain trace from channel 1
inst.write(':WAVeform:SOURce CHAN1')

for wav_format in formats:
    inst.write(':WAVeform:FORMat ' +  wav_format) # choose format for the transmitted waveform
    inst.write(':WAVeform:BYTeorder LSBFirst') # MSBF is default, must be overridden for WORD to work
    inst.write(':WAVeform:UNSigned OFF') # make sure the scope is sending signed ints

    preamble = inst.query(':WAVeform:PREamble?')
    preamble = preamble.split(',')
    print("\nWaveform format", format_dict[int(preamble[0])])

    if wav_format in ['WORD', 'BYTE']:
        num_samples = int(preamble[2])  # 2 POINTS : int32 - number of data points transferred.
        yIncr = float(preamble[7])      # 7 YINCREMENT : float32 - voltage diff between data points.
        yOrig = float(preamble[8])      # 8 YORIGIN : float32 - value is the voltage at center screen.
        yRef = int(preamble[9])         # 9 YREFERENCE : int32 - specifies the data point where y-origin occurs.
        print(" y increment %e\n y origin    %e\n y reference %i" % (yIncr, yOrig, yRef))

        # choose right datatype for interpreting query
        # according to https://docs.python.org/3/library/struct.html#format-characters
        # h is uint16 (nsigned short), b is int8 (signed char)
        datatype = 'h' if wav_format == 'WORD' else 'b'
        raw_bin = inst.query_binary_values(':WAVeform:DATA?', datatype=datatype, container=np.array)
        print("raw values", raw_bin)

        # calulate values from raw data
        processed = (raw_bin-yRef)*yIncr + yOrig
        print("processed values", processed)
        values[1].append(processed)
    elif wav_format == 'ASCii':
        raw = inst.query(':WAVeform:DATA?')
        raw = raw[10:] # removing IEEE block header
        raw = raw.split(',') # samples separated by commas
        processed = np.array([float(sample) for sample in raw])
        print("processed values", processed)
        values[1].append(processed)

    num_samples = int(preamble[2])    # POINTS : int32 - number of data points transferred.
    xIncr = float(preamble[4])        # XINCREMENT : float64 - time difference between data points.
    xOrig = float(preamble[5])        # XORIGIN : float64 - always the first data point in memory.
    xRef = int(preamble[6])           # XREFERENCE : int32 - specifies the data point associated with x-origin.
    time = (np.arange(num_samples)-xRef)*xIncr + xOrig # compute x-values
    times[1].append(time)


# Plotting the signals obtained for visual comparison
fig, axs = plt.subplots(nrows=len(formats), ncols=2, sharex=True, sharey=True)
for i, (time, value, ax) in enumerate(zip(times, values, axs.T)):
    for j, (t, v, a, format) in enumerate(zip(time, value, ax, formats)):
        try:
            a.plot(t, v*1000)
        except ValueError as err:
            print("Could not plot, check dimensions:", err)
        a.set_title(format)
        if i == 0: a.set_ylabel("signal [v]")
        if j == len(axs)-1: a.set_xlabel("time [s]")
fig.suptitle("keyoscacquire      pure pyvisa")

print("\nCalculating the difference between same waveform formats")
diffs = [values[0][i].T-values[1][i].T for i in range(3)]
for diff, format in zip(diffs, formats):
    print("Difference in "+format+" signals: "+str(sum(sum(diff))))

plt.show()

# close instrument connection
inst.write(':RUN')
inst.close()
