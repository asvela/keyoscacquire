.. _data-proc:

Data processing, file saving & loading
**************************************

.. py:currentmodule:: keyoscacquire.oscacq

The :mod:`keyoscacquire.oscacq` module contains function for processing
the raw data captured with :class:`Oscilloscope`, and :mod:`keyoscacquire.traceio`
for saving the processed data to files and plots.

Data processing
---------------

The output from the :func:`Oscilloscope.capture_and_read` function is processed
by :func:`process_data`, a wrapper function that sends the data to the
respective binary or ascii processing function.

.. autofunction:: process_data


File saving (:mod:`keyoscacquire.traceio`)
------------------------------------------

The package has built-in functions for saving traces to npy format
(see :mod:`numpy.lib.format`) files or ascii values (the latter is slower but will
give a header that can be customised, :func:`Oscilloscope.generate_file_header`
is used by default).

.. autofunction:: keyoscacquire.traceio.save_trace
.. autofunction:: keyoscacquire.traceio.plot_trace
.. autofunction:: keyoscacquire.traceio.load_trace
.. autofunction:: keyoscacquire.traceio.load_header
