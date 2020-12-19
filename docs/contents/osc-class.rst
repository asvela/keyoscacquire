.. _osc-class:

Instrument communication: The Oscilloscope class
************************************************


Oscilloscope API
================

.. py:currentmodule:: keyoscacquire.oscacq

.. autoclass:: Oscilloscope

High-level functions
--------------------

.. automethod:: Oscilloscope.get_trace
.. automethod:: Oscilloscope.save_trace
.. automethod:: Oscilloscope.plot_trace
.. automethod:: Oscilloscope.set_options_get_trace
.. automethod:: Oscilloscope.set_options_get_trace_save


Connection and VISA commands
----------------------------

.. automethod:: Oscilloscope.close
.. autoproperty:: Oscilloscope.timeout
.. automethod:: Oscilloscope.write
.. automethod:: Oscilloscope.query
.. automethod:: Oscilloscope.get_error

Oscilloscope state control
--------------------------

.. automethod:: Oscilloscope.run
.. automethod:: Oscilloscope.stop
.. automethod:: Oscilloscope.is_running
.. autoproperty:: Oscilloscope.active_channels

Acquisition and transfer options
--------------------------------

.. automethod:: Oscilloscope.set_channels_for_capture
.. automethod:: Oscilloscope.set_acquiring_options
.. automethod:: Oscilloscope.set_waveform_export_options


--------------

.. automethod:: Oscilloscope.capture_and_read
.. automethod:: Oscilloscope.generate_file_header


Auxiliary to the class
======================

.. autodata:: _supported_series
.. autodata:: _screen_colors
.. autodata:: _datatypes


.. _preamble:

The preamble
============

The preamble returned by the :meth:`capture_and_read` method (i.e. returned by the
oscilloscope when querying the VISA command ``:WAVeform:PREamble?``) is a string of
comma separated values, the values have the following meaning::

  0. FORMAT : int16 - 0 = BYTE, 1 = WORD, 4 = ASCII.
  1. TYPE : int16 - 0 = NORMAL, 1 = PEAK DETECT, 2 = AVERAGE
  2. POINTS : int32 - number of data points transferred.
  3. COUNT : int32 - 1 and is always 1.
  4. XINCREMENT : float64 - time difference between data points.
  5. XORIGIN : float64 - always the first data point in memory.
  6. XREFERENCE : int32 - specifies the data point associated with x-origin.
  7. YINCREMENT : float32 - voltage diff between data points.
  8. YORIGIN : float32 - value is the voltage at centre of the screen.
  9. YREFERENCE : int32 - specifies the data point where y-origin occurs.
