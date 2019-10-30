# -*- coding: utf-8 -*-
"""
Andreas Svela // 2019
"""


import os

current_dir = os.path.abspath(os.path.dirname(__file__))

# Get the version from the version file
with open(os.path.join(current_dir, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

import logging; _log = logging.getLogger(__name__)

# local file with default options:
import keyoscacquire.config as config

from keyoscacquire.oscacq import Oscilloscope
