# -*- coding: utf-8 -*-
"""
This module provides functions for saving traces to ``npy`` format files
(see :mod:`numpy.lib.format`) or ascii files. The latter is slower but permits
a header with metadata for the measurement, see :func:`Oscilloscope.generate_file_header`
which is used when saving directly from the ``Oscilloscope`` class.

"""

import os
import logging; _log = logging.getLogger(__name__)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import keyoscacquire.config as config
import keyoscacquire.oscacq as oscacq


## Trace saving and plotting ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

def save_trace(fname, time, y, fileheader="", ext=config._filetype,
               print_filename=True, nowarn=False):
    """Saves the trace with time values and y values to file.

    Current date and time is automatically added to the header. Saving to numpy
    format with :func:`save_trace_npy()` is faster, but does not include metadata
    and header.

    Parameters
    ----------
    fname : str
        Filename of trace
    time : ~numpy.ndarray
        Time axis for the measurement
    y : ~numpy.ndarray
        Voltage values, same sequence as channel_nums
    fileheader : str, default ``""``
        Header of file, use for instance :meth:`Oscilloscope.generate_file_header`
    ext : str, default :data:`~keyoscacquire.config._filetype`
        Choose the filetype of the saved trace
    print_filename : bool, default ``True``
        ``True`` prints the filename it is saved to

    Raises
    ------
    RuntimeError
        If the file already exists
    """
    if os.path.exists(fname+ext):
        raise RuntimeError(f"{fname+ext} already exists")
    if print_filename:
        print(f"Saving trace to:  {fname+ext}\n")
    data = np.append(time, y, axis=1) # make one array with columns x y1 y2 ..
    if ext == ".npy":
        if fileheader and not nowarn:
            _log.warning(f"(!) WARNING: The file header\n\n{fileheader}\n\nis not saved as file format npy is chosen. "
                          "\nTo suppress this warning, use the nowarn flag.")
        np.save(fname+".npy", data)
    else:
        np.savetxt(fname+ext, data, delimiter=",", header=fileheader)


def save_trace_npy(fname, time, y, print_filename=True, **kwargs):
    """Saves the trace with time values and y values to npy file.

    .. note:: Saving to numpy files is faster than to ascii format files
      (:func:`save_trace`), but no file header is added.

    Parameters
    ----------
    fname : str
        Filename to save to
    time : ~numpy.ndarray
        Time axis for the measurement
    y : ~numpy.ndarray
        Voltage values, same sequence as channel_nums
    print_filename : bool, default ``True``
        ``True`` prints the filename it is saved to
    """
    save_trace(fname, time, y, ext=".npy", nowarn=True, print_filename=print_filename)


def plot_trace(time, y, channels, fname="", showplot=config._show_plot,
               savepng=config._export_png):
    """Plots the trace with oscilloscope channel screen colours according to
    the Keysight colourmap and saves as a png.

    .. Caution:: No filename check for the saved plot, can overwrite
      existing png files.

    Parameters
    ----------
    time : ~numpy.ndarray
        Time axis for the measurement
    y : ~numpy.ndarray
        Voltage values, same sequence as channel_nums
    channels : list of ints
        list of the channels obtained, example [1, 3]
    fname : str, default ``""``
        Filename of possible exported png
    show : bool, default :data:`~keyoscacquire.config._show_plot`
        True shows the plot (must be closed before the programme proceeds)
    savepng : bool, default :data:`~keyoscacquire.config._export_png`
        ``True`` exports the plot to ``fname``.png
    """
    for i, vals in enumerate(np.transpose(y)): # for each channel
        plt.plot(time, vals, color=oscacq._screen_colors[channels[i]])
    if savepng:
        plt.savefig(fname+".png", bbox_inches='tight')
    if showplot:
        plt.show()
    plt.close()


## Trace loading ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

def load_trace(fname, ext=config._filetype, column_names='auto', skip_lines='auto',
               return_as_df=True):
    """Load a trace saved with keyoscacquire.oscacq.save_file()

    What is returned depends on the format of the file (.npy files contain no
    headers), and if a dataframe format is chosen for the return.

    Parameters
    ----------
    fname : str
        Filename of trace, with or without extension
    ext : str, default :data:`~keyoscacquire.config._filetype`
        The filetype of the saved trace (with the period, e.g. '.csv')
    column_names : ``{'auto' or list-like}``, default ``'auto'``
        Only useful if using with ``return_df=True``:
        To infer df column names from the last line of the header, use ``'auto'``
        (expecting '# <comma separated column headers>' as the last line of the
        header), or specify the column names manually
    skip_lines : ``{'auto' or int}``, default ``'auto'``

    return_as_df : bool, default True
        If the loaded trace is not a .npy file, decide to return the data as
        a Pandas dataframe if ``True``, or as an ndarray otherwise

    Returns
    -------
    data : :class:`~pandas.Dataframe` or :class:`~numpy.ndarray`
        If ``return_as_df`` is ``True`` and the filetype is not ``.npy``,
        a Pandas dataframe is returned. Otherwise ndarray. The first column
        is time, then each column is a channel.
    header : list or ``None``
        If ``.npy``, ``None`` is returned. Otherwise, a list of the lines at the
        beginning of the file starting with ``'#'``, stripped off ``'# '`` is returned
    """
    # Remove extenstion if provided in the fname
    if fname[-4:] in ['.npy', '.csv']:
        ext = fname[-4:]
        fname = fname[:-4]
    # Format dependent
    if ext == '.npy':
        return np.load(fname+ext), None
    else:
        return _load_trace_with_header(fname, ext, column_names=column_names,
                                       skip_lines=skip_lines,
                                       return_as_df=return_as_df)


def _load_trace_with_header(fname, ext, skip_lines='auto', column_names='auto',
                            return_as_df=True):
    """Read a trace file that has a header (i.e. not ``.npy`` files).

    See parameter description for :func:`load_trace()`.

    Returns
    -------
    data : :class:`~pandas.Dataframe` or :class:`~numpy.ndarray`
        Pandas dataframe if ``return_as_df`` is ``True``, ndarray otherwise
    header : list
        Lines at the beginning of the file starting with ``'#'``, stripped
        off ``'# '``
    """
    # Load header
    header = load_header(fname, ext)
    # Handle skipping and column names based on the header file
    if skip_lines == 'auto':
        skip_lines = len(header)
    if column_names == 'auto':
        column_names = header[-1].split(",")
    # Load the file
    df = pd.read_csv(fname+ext, delimiter=",", skiprows=skip_lines, names=column_names)
    # Return df or array
    if return_df:
        return df, header
    else:
        return np.array([df[col].values for col in df.columns]), header

def load_header(fname, ext=config._filetype):
    """Open a trace file and get the header

    Parameters
    ----------
    fname : str
        Filename of trace, with or without extension
    ext : str, default :data:`~keyoscacquire.config._filetype`
        The filetype of the saved trace (with the period, e.g. ``'.csv'``)

    Returns
    -------
    header : list
        Lines at the beginning of the file starting with ``'#'``, stripped
        off ``'# '``
    """
    if fname[-4:] in ['.csv']:
        ext = fname[-4:]
        fname = fname[:-4]
    header = []
    with open(fname+ext) as f:
        for line in f: # A few tens of us slower than a 'while True: readline()' approach
            # Check if part of the header
            if line[0] == '#':
                # Add the line without the initial '# ' to the header
                header.append(line.strip()[2:])
            else:
                break
    return header
