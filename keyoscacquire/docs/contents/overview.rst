****************************
Overview and getting started
****************************

The code is structured as a module :mod:`keyoscacquire.oscacq` containing the engine doing the `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_ interfacing in a class :class:`~keyoscacquire.oscacq.Oscilloscope`, and support functions for data processing and saving. Programmes are located in :mod:`keyoscacquire.programmes`, and the same programmes can be run directly from the command line as they are installed in the python path, see :ref:`cli-programmes`. Default options are found in :mod:`keyoscacquire.config`.


Quick reference
===============

The package installs the following command line programmes in the python path

* :program:`list_visa_devices`: list the available VISA devices

* :program:`path_of_config`: find the path of :mod:`keyoscacquireuire.config` storing default options. Change this file to your choice of standard settings, see :ref:`default-options`.

* :program:`get_single_trace`: use with option ``-h`` for instructions

* :program:`get_num_traces`: get a set number of traces, use with option ``-h`` for instructions

* :program:`get_traces_single_connection`: get a trace each time enter is pressed, use with option ``-h`` for instructions

See more under :ref:`cli-programmes-short`.

.. todo:: Add info about API

:mod:`keyoscacquire` uses the :py:mod:`logging` module, see :ref:`logging`.


Installation
============

Install the package with pip::

  $ pip install keysightoscilloscopeacquire


or download locally and install with ``$ python setup.py install`` or by running ``install.bat``.


.. include:: ../known-issues.rst
