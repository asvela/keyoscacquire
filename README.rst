keyoscacquire: Keysight oscilloscope acquire
============================================

keyoscacquire is a Python package for acquiring traces from Keysight InfiniiVision oscilloscopes through a VISA interface.

Based on `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_, keyoscacquire provides programmes for acquiring and exporting traces to your choice of ASCII format files (default csv) or `numpy <https://docs.scipy.org/doc/numpy/>`_ npy, and a png of the trace plot. The package provides a class ``Oscilloscope`` and data processing functions that can be used in other scripts. For example, to capture the active channels on an oscilloscope connected with VISA address ``USB0::1234::1234::MY1234567::INSTR`` from command prompt::

  get_single_trace -v USB0::1234::1234::MY1234567::INSTR

or in the python console::

   >>> import keyoscacquire.oscacq as koa
   >>> osc = koa.Oscilloscope(address='USB0::1234::1234::MY1234567::INSTR')
   >>> time, y, channel_numbers = osc.set_options_get_trace()

where ``time`` is a vertical numpy vector of time values and ``y`` is a numpy array which columns contain the data from the active channels listed in ``channel_numbers``.

If you need to find the VISA address of your oscilloscope, use the command line programme ``list_visa_devices`` provided by this package.

The code has been tested on Windows 7 and 10 with a Keysight DSO2024A model using a USB connection.

.. note:: In order to connect to a VISA instrument, NI MAX or similar might need to be running on the computer. Installation of Keysight Connection Expert might also be necessary.


Documentation
-------------

Available `keyoscacquire.rtfd.io <http://keyoscacquire.readthedocs.io/en/latest/>`_.


Contribute
----------

Contributions are welcome, find the project on `github <https://github.com/asvela/keyoscacquire.git>`_. The package is written and maintained by Andreas Svela.
