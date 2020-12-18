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

import keyoscacquire.oscacq as oscacq
import keyoscacquire.traceio as traceio
import keyoscacquire.config as config
import keyoscacquire.programmes as programmes
import keyoscacquire.auxiliary as auxiliary


from keyoscacquire.oscacq import Oscilloscope
