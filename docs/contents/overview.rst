****************************
Overview and getting started
****************************

The code is structured as a module :mod:`keyoscacquire.oscilloscope` containing the
engine doing the `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_
interfacing in a class :class:`~keyoscacquire.oscilloscope.Oscilloscope`, and
support functions for data processing. Programmes are located
in :mod:`keyoscacquire.programmes`, and the same programmes can be run
directly from the command line as they are installed in the Python path,
see :ref:`cli-programmes`. Default options are found in :mod:`keyoscacquire.config`,
and the :mod:`keyoscacquire.fileio` provides functions for plotting, saving,
and loading traces from disk.

keyoscacquire uses the :py:mod:`logging` module, see :ref:`logging`.


Installation
============

Install the package with pip

.. prompt:: bash

  pip install keyoscacquire


or download locally and install with ``$ python setup.py install`` or
by running ``install.bat``.


Quick reference
===============

.. include:: ../../README.rst
  :start-after: API-use-marker
  :end-before: contribute-marker


.. include:: ../known-issues.rst
