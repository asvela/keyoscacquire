.. _data-proc:

Data processing and file saving
*******************************

.. py:currentmodule:: keyoscacquire.oscacq

The :mod:`keyoscacquire.oscacq` module contains function for processing the raw data captured with :class:`Oscilloscope`, and for saving the processed data to files and plots.

Data processing
---------------

The output from the :func:`Oscilloscope.capture_and_read` function is processed by :func:`process_data`, a wrapper function that sends the data to the respective binary or ascii processing function.

.. autofunction:: process_data
.. autofunction:: process_data_binary
.. autofunction:: process_data_ascii


File saving
-----------

The package has built-in functions for saving traces to :mod:`numpy.lib.format` files or ascii values (the latter is slower but will give a header that can be customised, for instance :func:`Oscilloscope.generate_file_header` can be used).

.. autofunction:: save_trace
.. autofunction:: save_trace_npy
.. autofunction:: plot_trace
.. autofunction:: check_file
