# -*- coding: utf-8 -*-
"""
Install the Keysight oscilloscope acquire library.

Andreas Svela // 2019
"""


import os
from setuptools import setup

current_dir = os.path.abspath(os.path.dirname(__file__))

# Get the version from the version file
with open(os.path.join(current_dir, 'keyoscacquire', 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

# Get the contents of readme
with open(os.path.join(current_dir, "README.rst")) as readme_file:
    README = readme_file.read()
    # To avoid the parts with sphinx markup:
    README, _ = README.split(".. API-use-marker")
    print(README)

if __name__ == '__main__':
    setup(name='keyoscacquire',
          version=__version__,
          description='keyoscacquire is a Python package for acquiring traces from Keysight oscilloscopes through a VISA interface.',
          long_description=README,
          long_description_content_type='text/x-rst',
          # url='https://keyoscacquire.readthedocs.io/',
          project_urls={
            "Documentation": "https://keyoscacquire.readthedocs.io/",
            "Source": "https://github.com/asvela/keyoscacquire",
          },
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
                'get_single_trace=keyoscacquire.installed_cli_programmes:single_trace_cli',
                'get_traces_connect_each_time=keyoscacquire.installed_cli_programmes:connect_each_time_cli',
                'get_traces_single_connection=keyoscacquire.installed_cli_programmes:single_connection_cli',
                'get_num_traces=keyoscacquire.installed_cli_programmes:num_traces_cli',
                'list_visa_devices=keyoscacquire.installed_cli_programmes:list_visa_devices_cli',
                'path_of_config=keyoscacquire.installed_cli_programmes:path_of_config_cli'
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
