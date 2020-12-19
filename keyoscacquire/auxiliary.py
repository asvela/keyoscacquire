# -*- coding: utf-8 -*-
"""
Auxiliary functions for the keyoscacquire package

"""

import os
import logging; _log = logging.getLogger(__name__)
import keyoscacquire.config as config


def interpret_visa_id(id):
    """Interprets VISA ID, finds oscilloscope model series if applicable

    Parameters
    ----------
    id : str
        VISA ID as returned by the ``*IDN?`` command

    Returns
    -------
    maker : str
        Maker of the instrument, e.g. Keysight Technologies
    model : str
        Model of the instrument
    serial : str
        Serial number of the instrument
    firmware : str
        Firmware version
    model_series : str
        "N/A" unless the instrument is a Keysight/Agilent DSO and MSO oscilloscope.
        Returns the model series, e.g. '2000'. Returns "not found" if the model name cannot be interpreted.
    """
    maker, model, serial, firmware = id.split(",")
    # Find model_series if applicable
    if model[:3] in ['DSO', 'MSO']:
         # Find the numbers in the model string
        model_number = [c for c in model if c.isdigit()]
        # Pick the first number and add 000 or use not found
        model_series = model_number[0]+'000' if not model_number == [] else "not found"
    else:
        model_series = "N/A"
    return maker, model, serial, firmware, model_series


def check_file(fname, ext=config._filetype, num=""):
    """Checking if file ``fname+num+ext`` exists. If it does, the user is
    prompted for a string to append to fname until a unique fname is found.

    Parameters
    ----------
    fname : str
        Base filename to test
    ext : str, default :data:`~keyoscacquire.config._filetype`
        File extension
    num : str, default ""
        Filename suffix that is tested for, but the appended part to the fname
        will be placed before it,and the suffix will not be part of the
        returned fname

    Returns
    -------
    fname : str
        New fname base
    """
    while os.path.exists(fname+num+ext):
        append = input(f"File '{fname+num+ext}' exists! Append to filename '{fname}' before saving: ")
        fname += append
    return fname
