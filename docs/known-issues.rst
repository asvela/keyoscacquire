
Known issues and suggested improvements
=======================================

* Issues:

  - There has previously been an issue with the data transfer/interpretation
    where the output waveform is not as it is on the oscilloscope screen. If
    this happens, open *KeySight BenchVue* and obtain one trace through the
    software. Now try to obtain a trace through this package -- it should now
    work again. Please report this if this happens.

* Improvements:

  - (feature) capture MATH waveform
  - (feature) measurements provided by the scope
  - (feature) Build functionality for pickling measurement to disk and then
    post-processing for speed-up in consecutive measurements
  - (instrument support) expand support for Infiniium oscilloscopes
  - (docs) Write tutorial page for documentation
  - (housekeeping) PEP8 compliance and code audit
