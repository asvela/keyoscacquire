# -*- coding: utf-8 -*-
"""
Install the Keysight oscilloscope acquire library.

Andreas Svela // 2019
"""

__version__ = '3.0.0'

import os
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.rst")) as fid:
    README = fid.read()


if __name__ == '__main__':
    setup(name='keyoscacquire',
          version=__version__,
          description='Obtain traces, save to files and export raw plots from Keysight oscilloscopes using PyVISA.',
          long_description=README,
          long_description_content_type="text/x-rst",
          url='https://github.com/asvela/keyoscacquire.git',
          author='Andreas Svela',
          author_email='asvela@ic.ac.uk',
          license='MIT',
          packages=['keyoscacquire'],
          classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Operating System :: Microsoft :: Windows",
            ],
          entry_points={
            'console_scripts' : [
                'get_single_trace=keyoscacquire.installed_command_line_funcs:single_trace_command_line',
                'get_traces_connect_each_time=keyoscacquire.installed_command_line_funcs:connect_each_time_command_line',
                'get_traces_single_connection=keyoscacquire.installed_command_line_funcs:single_connection_command_line',
                'get_num_traces=keyoscacquire.installed_command_line_funcs:num_traces_command_line',
                'list_visa_devices=keyoscacquire.installed_command_line_funcs:list_visa_devices_command_line',
                'path_of_config=keyoscacquire.installed_command_line_funcs:path_of_config_command_line'
            ],
          },
          install_requires=[
              'pyvisa',
              'argparse',
              'numpy',
              'matplotlib',
              'tqdm',
              ],
          include_package_data=True,
          zip_safe=False,
          command_options={
              'build_sphinx': {
                'version': ('setup.py', __version__),
                'release': ('setup.py', __version__),
                'source_dir': ('setup.py', 'doc')}},
           )
