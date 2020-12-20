keyoscacquire: Keysight oscilloscope acquire
============================================

keyoscacquire is a Python package for acquiring traces from Keysight
InfiniiVision oscilloscopes through a VISA interface.

Based on `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_, keyoscacquire
provides programmes for acquiring and exporting traces to your choice of ASCII
format files (default csv) or numpy `npy <https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html>`_,
and a png of the trace plot. The package also provides an API for integration
in other Python code.

keyoscacquire uses the :py:mod:`logging` module, see :ref:`logging`.

The code has been tested on Windows 7 and 10 with a Keysight DSO2024A model
using a USB connection.

.. note:: In order to connect to a VISA instrument, NI MAX or similar might
  need to be running on the computer. Installation of Keysight Connection
  Expert might also be necessary.

.. documentation-marker

Documentation
-------------

Available at `keyoscacquire.rtfd.io <http://keyoscacquire.readthedocs.io/en/latest/>`_.
A few examples below, but formatting and links are broken as the snippet is intended
for the documentation parser.

.. command-line-use-marker

Command line use
----------------

Capture the active channels on an oscilloscope connected with VISA address
from command prompt

.. prompt:: bash

  get_single_trace -v "USB0::1234::1234::MY1234567::INSTR"

The ``get_single_trace`` programme takes several other arguments too, see them with

.. prompt:: bash

  get_single_trace -h


If you need to find the VISA address of your oscilloscope, simply use the
command line programme ``list_visa_devices`` provided by this package

.. prompt:: bash

  list_visa_devices

The package installs the following command line programmes in the Python path

* ``list_visa_devices``: list the available VISA devices
* ``path_of_config``: find the path of :mod:`keyoscacquire.config`
  storing default options. Change this file to your choice of standard
  settings, see :ref:`default-options`.
* ``get_single_trace``: use with option ``-h`` for instructions
* ``get_num_traces``: get a set number of traces, use with
  option ``-h`` for instructions
* ``get_traces_single_connection``: get a trace each time enter is
  pressed, use with option ``-h`` for instructions

See more under :ref:`cli-programmes-short`.


Python console/API
------------------

In the Python console::

   >>> import keyoscacquire.oscacq as koa
   >>> osc = koa.Oscilloscope(address='USB0::1234::1234::MY1234567::INSTR')
   >>> time, y, channel_numbers = osc.set_options_get_trace()
   >>> osc.close()

where ``time`` is a vertical numpy (2D) array of time values and ``y`` is a numpy
array which columns contain the data from the active channels listed in
``channel_numbers``.

Explore the Reference section (particularly :ref:`osc-class`) to get more
information about the API.

.. contribute-marker

Contribute
----------

Contributions are welcome, find the project on
`github <https://github.com/asvela/keyoscacquire.git>`_.
The package is written and maintained by Andreas Svela.
