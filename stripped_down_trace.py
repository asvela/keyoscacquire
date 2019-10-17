address =
wav_format = 'WORD'

rm = visa.ResourceManager()
inst = rm.open_resource(address)
inst.write('*CLS')  # clears the status data structures, the device-defined error queue, and the Request-for-OPC flag
id = self.inst.query('*IDN?').strip() # get the id of the connected device
print("Connected to \'%s\'" % id)

inst.write(':WAVeform:FORMat ' +  wav_format) # choose format for the transmitted waveform]

if wav_format == 'WORD':
    preamble = inst.query(':WAVeform:PREamble?')
    print(preamble)
    raw_bin = inst.query_binary_values(':WAVeform:DATA?', datatype='H')
elif wav_format == 'ASCii':
    raw_ascii = inst.query(':WAVeform:DATA?')


inst.close()
