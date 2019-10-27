# -*- coding: utf-8 -*-
"""
Script to test obtaining data with differentwaveform formats for Keysight DSO2024A


Andreas Svela // 2019
"""

visa_path = 'C:\\Program Files\\IVI Foundation\\VISA\\Win64\\agvisa\\agbin\\visa32.dll'
# Oxford
visa_address = 'USB0::0x0957::0x1796::MY59125372::INSTR'
# NPL
# visa_address = 'USB0::0x0957::0x1796::MY57233636::INSTR'


import pyvisa
import numpy as np
import matplotlib.pyplot as plt

format_dict = {0: "BYTE", 1: "WORD", 4: "ASCii"}


# use Keysight VISA and connect to instrument
rm = pyvisa.ResourceManager(visa_path)
inst = rm.open_resource(visa_address)
inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
id = inst.query('*IDN?').strip() # get the id of the connected device
print("Connected to\n\t\'%s\'" % id)

# obtain trace from channel 1
inst.write(':DIGitize CHAN1')
inst.write(':WAVeform:SOURce CHAN1')

formats = ['BYTE', 'WORD', 'ASCii']
values = []
for wav_format in formats:
    inst.write(':WAVeform:FORMat ' +  wav_format) # choose format for the transmitted waveform
    inst.write(':WAVeform:BYTeorder MSB') # this should be default anyway

    preamble = inst.query(':WAVeform:PREamble?')
    preamble = preamble.split(',')
    print("\nWaveform format", format_dict[int(preamble[0])])


    if wav_format in ['WORD', 'BYTE']:
        num_samples = int(preamble[2])  # 2 POINTS : int32 - number of data points transferred.
        yIncr = float(preamble[7])      # 7 YINCREMENT : float32 - voltage diff between data points.
        yOrig = float(preamble[8])      # 8 YORIGIN : float32 - value is the voltage at center screen.
        yRef = int(preamble[9])         # 9 YREFERENCE : int32 - specifies the data point where y-origin occurs.
        print(" y increment %e\n y origin    %e\n y reference %i" % (yIncr, yOrig, yRef))

        inst.write(':WAVeform:UNSigned ON') # make sure the scope is sending UNsigned ints
        # choose right datatype for interpreting query
        # according to https://docs.python.org/3/library/struct.html#format-characters
        # H is uint16 (unsigned short), B is uint8 (unsigned char)
        datatype = 'H' if wav_format == 'WORD' else 'B'
        raw_bin = inst.query_binary_values(':WAVeform:DATA?', datatype=datatype, container=np.array)
        print("raw values", raw_bin)

        # calulate values from raw data
        processed = (raw_bin-yRef)*yIncr + yOrig
        print("processed values", processed)
        values.append(processed)
    elif wav_format == 'ASCii':
        # use standard query function
        # according to documentation gives ascii without header:
        # "The ASCii format does not send out the header information indicating the number of bytes being downloaded."
        # Keysight Infiniium Oscilloscopes Programmer's guide Version 06.40.00904, page 1503
        print("First, try not explicitly expecting ASCII with \'query(..)\' ..")
        raw = inst.query(':WAVeform:DATA?')
        print("The raw data should not contain a block header according to the manual")
        print("raw ", raw[:100])
        if raw[0] == '#':
            print("..but it turns out is has a header block. Remove it and process the data")
            raw = raw[10:]
            print("After removing block header", raw[:50])
        raw = raw.split(',') # samples separated by commas
        processed = np.array([float(sample) for sample in raw])
        print("processed values", processed)
        values.append(processed)
        # Now try to explicitly expect ascii
        print("\nSecondly, explicitly expect ASCII with \'query_ascii_values(..)\' ..")
        try:
            raw_ascii = inst.query_ascii_values(':WAVeform:DATA?')
            print("Returns", raw_ascii[:50])
        except ValueError as e:
            print("(!) ValueError:")
            print("\t", e)

# plotting the values obtained
fig, ax = plt.subplots(nrows=len(formats), sharex=True, sharey=False)
for val, a, format in zip(values, ax, formats):
    a.plot(val*1000)
    a.set_title(format)
    a.set_ylabel("milli volts")
ax[2].set_xlabel("point number")
plt.show()

#close instrument connection
inst.write(':RUN')
inst.close()
