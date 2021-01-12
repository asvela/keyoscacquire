keyoscacquire: Keysight oscilloscope acquire
============================================

.. image:: https://img.shields.io/pypi/v/keyoscacquire?style=flat-square
  :target: https://pypi.org/project/keyoscacquire/
  :alt: PyPI

.. image:: https://img.shields.io/codefactor/grade/github/asvela/keyoscacquire?style=flat-square
  :target: https://www.codefactor.io/repository/github/asvela/keyoscacquire
  :alt: CodeFactor

.. image:: https://img.shields.io/readthedocs/keyoscacquire?style=flat-square
  :target: https://keyoscacquire.rtfd.io
  :alt: Read the Docs Building

.. image:: https://img.shields.io/pypi/l/keyoscacquire?style=flat-square
  :target: https://keyoscacquire.readthedocs.io/en/dev-v4.0.0/contents/license.html
  :alt: License

keyoscacquire is a Python package for acquiring traces from Keysight
InfiniiVision oscilloscopes through a VISA interface.

Based on `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_, keyoscacquire
provides programmes for acquiring and exporting traces to your choice of ASCII
format files (default csv) or numpy `npy <https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html>`_,
and a png of the trace plot. The package also provides an API for integration
in other Python code.

The code has been tested on Windows 7 and 10 with a Keysight DSO2024A model
using a USB connection.

.. documentation-marker

Documentation
-------------

Available at `keyoscacquire.rtfd.io <http://keyoscacquire.readthedocs.io/en/latest/>`_.
A few examples below, but formatting and links are broken as this file is intended
for the documentation parser.


Installation
------------

Install the package with pip::

  pip install keyoscacquire

or download locally and install with ``$ python setup.py install`` or
by running ``install.bat``.

.. API-use-marker

Python console/API
------------------

The Reference/API section (particularly :ref:`osc-class`) gives all the necessary
information about the API.

As an example of API usage/use in the Python console::

  >>> import keyoscacquire as koa
  >>> scope = koa.Oscilloscope(address='USB0::1234::1234::MY1234567::INSTR')
  Connected to:
     AGILENT TECHNOLOGIES
     DSO-X 2024A (serial MY1234567)
  >>> scope.acq_type = 'AVER8'
  >>> print(scope.num_points)
  7680
  >>> time, y, channel_numbers = scope.get_trace(channels=[2, 1, 4])
  Acquisition type: AVER
  # of averages:    8
  From channels:    [1, 2, 4]
  Acquiring ('WORD').. done
  Points captured per channel: 7,680
  >>> print(channel_numbers)
  [1, 2, 4]
  >>> scope.save_trace(showplot=True)
  Saving trace to:  data.csv
  >>> scope.close()

where ``time`` is a vertical numpy (2D) array of time values and ``y`` is a numpy
array which columns contain the data from the active channels listed in
``channel_numbers``. The trace saved to ``data.csv`` also contains metadata
(can be further customised) in the first lines::

  # AGILENT TECHNOLOGIES,DSO-X 2024A,MY1234567,02.50.2019022736
  # AVER,8
  # 2020-12-21 03:13:18.184028
  # time,1,2,4
  -5.000063390000000080e-03,-4.853398528000013590e-03,-5.247737759999995810e-03,-5.247737759999995810e-03
  ...

The trace can be easily loaded from disk to a Pandas dataframe with::

  >>> df, metadata = koa.fileio.load_trace("data")
  >>> df.head()
      time         1         2         4
  0 -0.005 -0.004853 -0.005248 -0.005248
  1 -0.005 -0.005406 -0.005017 -0.005248
  2 -0.005 -0.004964 -0.005190 -0.005248
  3 -0.005 -0.005185 -0.005363 -0.005248
  4 -0.005 -0.005517 -0.005074 -0.005248
  >>> metadata
  ['AGILENT TECHNOLOGIES,DSO-X 2024A,MY1234567,02.50.2019022736', 'AVER,8', '2020-12-21 03:13:18.184028', 'time,1,2,4']


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

.. contribute-marker

Contribute/report issues
------------------------

Please report any issues with the package with the
`issue tracker on Github <https://github.com/asvela/keyoscacquire/issues>`_.

Contributions are welcome via
`github <https://github.com/asvela/keyoscacquire.git>`_.


The package is written and maintained by Andreas Svela.
