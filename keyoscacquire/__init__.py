# -*- coding: utf-8 -*-
"""
Andreas Svela // 2019-2021
"""


import os

current_dir = os.path.abspath(os.path.dirname(__file__))

# Get the version from the version file
with open(os.path.join(current_dir, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

import logging
_log = logging.getLogger(__name__)

import keyoscacquire.oscilloscope as oscilloscope
import keyoscacquire.fileio as fileio
import keyoscacquire.config as config
import keyoscacquire.programmes as programmes
import keyoscacquire.visa_utils as visa_utils

from .oscilloscope import Oscilloscope, _SUPPORTED_SERIES
from .fileio import save_trace, load_trace, _SCREEN_COLORS
