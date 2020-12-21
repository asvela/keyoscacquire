import keyoscacquire as koa
import matplotlib.pyplot as plt

def averaged_trace(scope, measurement_number, averages=8):
    # Set the number of averages and get a trace
    time, voltages, _ = scope.set_options_get_trace(acq_type=f"AVER{averages}")
    # Save the trace data as a csv and a png plot, without showing the plot
    # (the averaging mode and the number of averages is also automatically
    # saved inside the file, together with a timestamp and more)
    scope.save_trace(fname=f"measurement{measurement_number}_AVER{averages}",
                     showplot=False)
    return time, voltages


def different_averaging(visa_address, measurement_number):
    # Connect to the scope
    with koa.Oscilloscope(address=visa_address) as scope:
        # Set the channels to view on the scope
        scope.active_channels = [1, 3]
        # Prepare a two panel plot
        fig, ax = plt.subplots(nrows=2, sharex=True)
        # Obtain traces for different numbers of averages
        for averages in [2, 4, 8, 16, 32]:
            time, voltages = averaged_trace(scope, measurement_number, averages=averages)
            # Plot channel 1 to ax[0] and ch 3 to ax[1]
            for a, ch in zip(ax, voltages.T):
                a.plot(time, ch, label=f"{averages}", alpha=0.5)
        # Add legends to and labels to both plots
        for a, ch_num in zip(ax, scope.active_channels):
            a.set_xlabel("Time [s]")
            a.set_ylabel(f"Channel {ch_num} [V]")
            a.legend()
    plt.show()


different_averaging(visa_address="USB0::1234::1234::MY1234567::INSTR",
                    measurement_number=1)
