.. Keysight Oscilloscope Acquire documentation master file, created by
   sphinx-quickstart on Mon Oct 21 05:06:26 2019.

keyoscacquire: Keysight Oscilloscope Acquire
============================================

keyoscacquire is a Python package for acquiring traces from Keysight oscilloscopes through a VISA interface.

Based on `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_, keyoscacquire provides programmes for acquiring and exporting traces to your choice of ASCII format files (default csv) and a png of the trace plot. The package's :py:class:`Oscilloscope` and data processing functions can also be used in other scrips, for example, to capture the active channels on an oscilloscope connected with VISA address ``USB0::1234::1234::MY1234567::INSTR``::

   >>> import keyoscacq as koa
   >>> osc = koa.Oscilloscope(address='USB0::1234::1234::MY1234567::INSTR')
   >>> time, y, channel_numbers = osc.set_options_getTrace()

where ``time`` is a vertical numpy vector of time values and ``y`` is a numpy array which columns contain the data from the channels in ``channel_numbers``.

If you need to find the VISA address of your oscilloscope, use the command line function ``list_visa_devices`` provided by this package.

The code has been tested on Windows 7 and 10 with a Keysight DSO2024A model using a USB connection.

.. note:: In order to connect to a VISA instrument, NI MAX or similar might need to be running on the computer.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   usage
   oscacq-module


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Contribute
----------

Contributions are welcome, find the project on github **INSERT LINK**


License
-------

The project is licensed under the MIT license.
