
Known issues and suggested improvements
=======================================

* Issues:

    - Sometimes ``WORD`` waveform does not give the correct trace data, just random noise (but switching to ``ASCii`` or ``BYTE`` gives correct traces). If this happens, open *KeySight BenchVue* and obtain one trace through the software. Now try to obtain a trace through this package -- it should now work again using ``WORD``.

* Improvements:

    - Add optional argument to supply visa address of instrument to command line executables and scripts
