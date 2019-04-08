#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Andreas Svela // 2019
"""

__version__ = '1.1.0'

import logging; _log = logging.getLogger(__name__)

# local file with default options:
import keyoscacquire.config as config

from keyoscacquire.oscacq import Oscilloscope
