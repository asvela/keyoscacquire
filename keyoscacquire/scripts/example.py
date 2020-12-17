import keyoscacquire.oscacq as koa
import matplotlib.pyplot as plt

def get_averaged(osc_address, averages=8):
    with koa.Oscilloscope(address=osc_address) as scope:
        time, volts, channels = scope.set_options_get_trace(acq_type='AVER'+str(averages))
    return time, volts, channels

time, volts, channels = get_averaged('USB0::1234::1234::MY1234567::INSTR')
for y, ch in zip(volts.T, channels): # need to transpose volts: each row is one channel
    plt.plot(time, y, label=ch, color=koa._screen_colors[ch])
plt.legend()
plt.show()
