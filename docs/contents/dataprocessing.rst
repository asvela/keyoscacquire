.. _data-proc:

Data processing, file saving & loading
**************************************

The :mod:`keyoscacquire.dataprocessing` module contains a function for processing
the raw data captured with :class:`oscilloscope.Oscilloscope`, and :mod:`keyoscacquire.fileio`
for saving the processed data to files and plots.

Data processing (:mod:`keyoscacquire.dataprocessing`)
-----------------------------------------------------

.. automodule:: keyoscacquire.dataprocessing
  :members:


File saving and loading (:mod:`keyoscacquire.fileio`)
------------------------------------------------------

The Oscilloscope class has the method :meth:`keyoscacquire.Oscilloscope.save_trace()`
for saving the most recently captured trace to disk. This method relies on the
``fileio`` module.

.. automodule:: keyoscacquire.fileio

.. autofunction:: keyoscacquire.fileio.save_trace
.. autofunction:: keyoscacquire.fileio.plot_trace
.. autofunction:: keyoscacquire.fileio.load_trace
.. autofunction:: keyoscacquire.fileio.load_header
