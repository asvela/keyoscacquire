
Data processing and file saving
*******************************

.. py:currentmodule:: keyoscacquire.oscacq

Data processing
---------------

The output from the :func:`Oscilloscope.capture_and_read` function is processed by :func:`process_data`, a wrapper function that sends the data to the respective binary or ascii processing function.

.. autofunction:: process_data
.. autofunction:: process_data_binary
.. autofunction:: process_data_ascii


File saving
-----------

The package has built-in functions for saving traces to ascii values

.. autofunction:: save_trace
.. autofunction:: save_trace_npy
.. autofunction:: plot_trace
.. autofunction:: check_file
