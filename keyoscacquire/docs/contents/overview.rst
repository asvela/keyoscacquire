****************************
Overview and getting started
****************************

The code is structured as a module :mod:`keyoscacquire.oscacq` containing the engine doing the `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_ interfacing in a class :py:class:`Oscilloscope`, and support functions for data processing and saving. Programmes are located in :mod:`keyoscacquire.programmes`. Default options are found in :mod:`keyoscacquire.config`.


Quick reference
===============

The package installs the following command line functions

* :meth:`path_of_config`: find the path of :mod:`keysightoscacquire.config` storing default options. Change this file to your choice of standard settings, see :ref:`default-options`.

* :meth:`list_visa_devices`: list the available VISA devices

* :meth:`get_single_trace`: use with option ``-h`` for instructions

* :meth:`get_num_traces`: get a set number of traces, use with option ``-h`` for instructions

* :meth:`getTraces_single_connection`: get a trace each time enter is pressed, use with option ``-h`` for instructions

See more under :ref:`standalone-programmes`.

.. todo:: Add info about oscilloscope class

keyoscacquire uses the :py:mod:`logging` module, see :ref:`logging`.

Installation
============

Install the package with pip::

  $ pip install keysightoscilloscopeacquire


or download locally and install with ``$ python setup.py install`` or by running ``install.bat``.


Known issues/suggested improvements
===================================

- Known issue: Sometimes ``WORD`` waveform does not give the correct trace data, just random noise (but switching to ``ASCii`` or ``BYTE`` gives correct traces). If this happens, open *KeySight BenchVue* and obtain one trace through the software. Now try to obtain a trace through this package -- it should now work again using ``WORD``.
- Add optional argument to supply visa address of instrument to command line executables and scripts


.. include:: ../changelog.rst
