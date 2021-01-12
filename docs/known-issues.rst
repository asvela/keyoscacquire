
Known issues and suggested improvements
=======================================

* Issues:

  - An issue has been reported where the data transfer/interpretation
    where the output waveform is not correct, causing the trace to look nothing
    like on the oscilloscope screen. If this happens, a fix has been to open
    *KeySight BenchVue* and obtain one trace through the
    software. Now try to obtain a trace through this package -- it should now
    work again. Please report this if this happens.

* Improvements:

  - (feature) include capture of MATH waveform
  - (feature) expand API to include

    * waveform measurements

    * trigger settings

    * time and voltage axes settings

  - (feature) pickling trace to disk for later post-processing to give speed-up
    in consecutive measurements
  - (instrument support) expand support for Infiniium oscilloscopes
  - (development) include tests
