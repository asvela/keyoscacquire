# -*- coding: utf-8 -*-
"""
Visa-related auxiliary functions for the keyoscacquire package

"""

import os
import pyvisa
import logging

import keyoscacquire.config as config

_log = logging.getLogger(__name__)

def interpret_visa_id(idn):
    """Interprets a VISA ID, including finding a oscilloscope model series
    if applicable

    Parameters
    ----------
    idn : str
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
    maker, model, serial, firmware = idn.split(",")
    # Find model_series if applicable
    if model[:3] in ['DSO', 'MSO']:
         # Find the numbers in the model string
        model_number = [c for c in model if c.isdigit()]
        # Pick the first number and add 000 or use not found
        model_series = model_number[0]+'000' if not model_number == [] else "not found"
    else:
        model_series = "N/A"
    return maker, model, serial, firmware, model_series


def obtain_instrument_information(resource_manager, address, num, ask_idn=True):
    """Obtain more information about a VISA resource

    Parameters
    ----------
    resource_manager : :class:`pyvisa.resource_manager`
    address : str
        VISA address of the instrument to be investigated
    num : int
        Sequential numbering of investigated instruments
    ask_idn : bool
        If ``True``: will query the instrument's IDN and interpret it
        if possible

    Returns
    -------
    resource_info : list
        List of information::

            [num, address, alias, maker, model, serial, firmware, model_series]

        when ``ask_idn`` is ``True``, otherwise::

            [num, address, alias]

    """
    resource_info = []
    info_object = resource_manager.resource_info(address)
    alias = info_object.alias if info_object.alias is not None else "N/A"
    resource_info.extend((str(num), address, alias))
    if ask_idn:
        # Open the instrument and get the identity string
        try:
            error_flag = False
            instrument = resource_manager.open_resource(address)
            idn = instrument.query("*IDN?").strip()
            instrument.close()
        except pyvisa.Error as e:
            error_flag = True
            resource_info.extend(["no IDN response"]*5)
            print(f"Instrument #{num}: Did not respond to *IDN?: {e}")
        except Exception as ex:
            error_flag = True
            print(f"Instrument #{num}: Got exception {ex.__class__.__name__} "
                  f"when asking for its identity.")
            resource_info.extend(["Error"]*5)
        if not error_flag:
            try:
                resource_info.extend(interpret_visa_id(idn))
            except Exception as ex:
                print(f"Instrument #{num}: Could not interpret VISA id, got "
                      f"exception {ex.__class__.__name__}: VISA id returned was '{idn}'")
                resource_info.extend(["failed to interpret"]*5)
    return resource_info
