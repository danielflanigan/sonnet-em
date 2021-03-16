import numpy as np
import pandas as pd


def read_single(filename):
    """Return a pandas Dataframe containing the contents of a .csv file exported from a plot with a single curve.

    The columns of the DataFrame are extracted from the line just before the beginning of the data

    :param str filename: the file to read, which should be in .csv format.
    :returns: a dataframe and a string containing the first line of the file, which is not yet parsed.
    :rtype: tuple[pandas.DataFrame, str]
    """
    with open(filename) as f:
        line0 = f.readline().strip()
        line1 = f.readline().strip()
        tokens = line1.split(' ')
        # FREQUENCY (GHz) MAG[PZ1] -> frequency_GHz or VARIABLE (Lk_pH_per_square) -> Lk_pH_per_square
        if tokens[0] == 'FREQUENCY':
            independent_variable = f"frequency_{tokens[1].strip('()')}"
        elif tokens[0] == 'VARIABLE':
            independent_variable = tokens[1].strip('()')
        dependent_variable = tokens[2]
    df = pd.read_csv(filename, header=1, names=[independent_variable, dependent_variable])
    return df, line0


def read_multiple(filename):
    """Return a pandas dataframe containing the contents of a .csv file exported from a plot with multiple curves.

    This is significantly slower than :func:`read_single` because it has to parse the file line by line.
    """
    pass