****************************
Overview and getting started
****************************

The code is structured as a module :mod:`keyoscacquire.oscacq` containing the
engine doing the `PyVISA <https://pyvisa.readthedocs.io/en/latest/>`_
interfacing in a class :class:`~keyoscacquire.oscacq.Oscilloscope`, and
support functions for data processing. Programmes are located
in :mod:`keyoscacquire.programmes`, and the same programmes can be run
directly from the command line as they are installed in the Python path,
see :ref:`cli-programmes`. Default options are found in :mod:`keyoscacquire.config`,
and the :mod:`keyoscacquire.traceio` provides functions for plotting, saving,
and loading traces from disk.


Quick reference
===============

.. include:: ../../README.rst
  :start-after: command-line-use-marker
  :end-before: contribute-marker


Installation
============

Install the package with pip

.. prompt:: bash

  pip install keyoscacquire


or download locally and install with ``$ python setup.py install`` or
by running ``install.bat``.


Building the docs
-----------------
To build a local copy of the sphinx docs make sure the necessary packages
are installed

.. prompt:: bash

    pip install sphinx sphinx-prompt furo recommonmark

Then build by executing ``make html`` in the ``docs`` folder.


.. include:: ../known-issues.rst
