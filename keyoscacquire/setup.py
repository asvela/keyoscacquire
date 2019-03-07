#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Install the Keysight Oscilloscope Acquire library.

Andreas Svela // 2019
"""

__version__ = '0.5.0'

import os
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md")) as fid:
    README = fid.read()


if __name__ == '__main__':
    setup(name='keysightoscilloscopeacquire',
          version=__version__,
          description='Obtain traces, save to files and export raw plots from Keysight oscilloscopes using pyVISA.',
          long_description=README,
          long_description_content_type="text/markdown",
          url='none',
          author='Andreas Svela',
          author_email='andreas.svela@npl.co.uk',
          license='MIT',
          packages=['keyoscacquire'],
          entry_points={
            'console_scripts' : [
                'get_single_trace=keyoscacquire.installed_command_line_funcs:single_trace_command_line',
                'getTraces_connect_each_time=keyoscacquire.installed_command_line_funcs:connect_each_time_command_line',
                'getTraces_single_connection=keyoscacquire.installed_command_line_funcs:single_connection_command_line'
            ],
          },
          install_requires=[
              'visa',
              'argparse',
              'numpy',
              'matplotlib'
              ],
          zip_safe=False)
