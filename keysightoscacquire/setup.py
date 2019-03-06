#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Install the KeysightOscilloscopeAcquiring library.

Andreas Svela 2019
"""

__version__ = '0.1'

from setuptools import setup

if __name__ == '__main__':
    setup(name='KeysightOscilloscopeAcquiring',
          version=__version__,
          description='Obtain traces, save to files and export raw plots from Keysight oscilloscopes using pyVISA.',
          url='none',
          author='Andreas Svela',
          author_email='andreas.svela@npl.co.uk',
          license='MIT',
          packages=['keysightoscacquire'],
          scripts=[
          'bin/getTraces_connect_each_time_loop',
          'bin/getTraces_single_connection_loop'
          ],
          install_requires=[
          'visa'
          'numpy',
          'matplotlib'
          ],
          zip_safe=False)
