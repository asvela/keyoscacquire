
Known issues and suggested improvements
=======================================

* Issues:

    - Sometimes ``WORD`` or ``BYTE`` waveform does not give the correct trace data, just random noise (but switching to ``ASCii`` gives correct traces). If this happens, open *KeySight BenchVue* and obtain one trace through the software. Now try to obtain a trace through this package -- it should now work again using ``WORD`` or ``BYTE``.

* Improvements:

    - Add acquiring options to file header of saved files
    - Make a dynamic default setting for number of points
