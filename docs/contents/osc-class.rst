.. _osc-class:

Instrument communication: The Oscilloscope class
************************************************


Class API
=========

.. py:currentmodule:: keyoscacquire.oscacq

.. autoclass:: Oscilloscope
   :members:

Auxiliary to the class
======================

.. autofunction:: interpret_visa_id

.. autodata:: _supported_series
.. autodata:: _screen_colors
.. autodata:: _datatypes


.. _preamble:

The preamble
============

The preamble returned by the capture_and_read functions (i.e. returned by the oscilloscope when querying the VISA command ``:WAV:PREamble?``) is a string of comma separated values, the values have the following meaning:

    0. FORMAT : int16 - 0 = BYTE, 1 = WORD, 4 = ASCII.
    1. TYPE : int16 - 0 = NORMAL, 1 = PEAK DETECT, 2 = AVERAGE
    2. POINTS : int32 - number of data points transferred.
    3. COUNT : int32 - 1 and is always 1.
    4. XINCREMENT : float64 - time difference between data points.
    5. XORIGIN : float64 - always the first data point in memory.
    6. XREFERENCE : int32 - specifies the data point associated with x-origin.
    7. YINCREMENT : float32 - voltage diff between data points.
    8. YORIGIN : float32 - value is the voltage at center screen.
    9. YREFERENCE : int32 - specifies the data point where y-origin occurs.
