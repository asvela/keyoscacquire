.. _data-proc:

Data processing, file saving & loading
**************************************

.. py:currentmodule:: keyoscacquire.oscacq

The :mod:`keyoscacquire.oscacq` module contains a function for processing
the raw data captured with :class:`Oscilloscope`, and :mod:`keyoscacquire.traceio`
for saving the processed data to files and plots.

Data processing
---------------

The output from the :func:`Oscilloscope.capture_and_read` function is processed
by :func:`process_data`, a wrapper function that sends the data to the
respective binary or ascii processing function.

This function is kept outside the Oscilloscope class as one might want to
post-process data after capturing it.

.. autofunction:: process_data


File saving and loading (:mod:`keyoscacquire.traceio`)
------------------------------------------------------

The Oscilloscope class has the method :meth:`Oscilloscope.save_trace()` for
saving the most recently captured trace to disk. This method relies on the
``traceio`` module.

.. automodule:: keyoscacquire.traceio

.. autofunction:: keyoscacquire.traceio.save_trace
.. autofunction:: keyoscacquire.traceio.plot_trace
.. autofunction:: keyoscacquire.traceio.load_trace
.. autofunction:: keyoscacquire.traceio.load_header
