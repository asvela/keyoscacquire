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
          entry_points={
            'console_scripts' : [
                'getTraces_connect_each_time=keysightoscacquire.installed_command_line_funcs:connect_each_time_command_line',
                'getTraces_single_connection=keysightoscacquire.installed_command_line_funcs:single_connection_command_line'
            ],
          },
          install_requires=[
              'visa',
              'argparse',
              'numpy',
              'matplotlib'
              ],
          zip_safe=False)
