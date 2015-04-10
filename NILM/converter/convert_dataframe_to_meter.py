# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 11:13:13 2015

@author: thibaut
"""

import pandas as pd
import pprint
import os


def dataframe_to_meter(df, hdf_filename):
    """Converts a pandas.Dataframe into a meter HDFS file.

    The DataFrame needs to have a well determined structure. See Parameters
    The meter is store into a HDFS file so-called meter HDFS file which can
    be used to create a NILM.Meter object.

    Parameters
    ----------
    df: pandas.DataFrame, (n_timestamps, n_power*n_phases)
        index: pandas.DataTimeIndex,
            All timestamps of measurements, timezone aware.
        columns: pandas.MultiIndex
            The columns needs to have two levels.
                level 0: Phases measured by the meters
                level 1: Powers measured by the meters
        values: float
            Value for the power and phase considered at the timestamp.

    hdf_filename: str
        path+name of the file to store the meter HDFS file.
    """

    if os.path.exists(hdf_filename):
        os.remove(hdf_filename)

    try:
        assert isinstance(df.index, pd.DatetimeIndex)
    except AssertionError:
        raise AssertionError('Convertion: the dataframe index needs to be \
                             timestamps')

    # Check that there is two levels for columns:
    try:
        assert len(df.columns.levels) == 2
    except AssertionError:
        raise AssertionError('Convertion: the dataframe columns needs to have \
                             two levels: phases and power_types')

    phases = list(df.columns.levels[0])
    print 'Convertion: the phases are:', phases

    power_types = list(df.columns.levels[1])
    print 'Convertion: the power types measured are:', power_types

    for phase in phases:
        try:
            assert (list(df[phase].columns) == power_types)
        except AssertionError:
            raise AssertionError('Convertion: the phase {:s} of does not have \
                                  all the power types'.format(phase))

    measurements = {}
    measurements['phases'] = phases
    measurements['power_types'] = power_types

    timestamps = {}
    timestamps['tz'] = str(df.index.tz)
    timestamps['start'] = str(pd.Timestamp(df.index[0]))
    timestamps['end'] = str(pd.Timestamp(df.index[-1]))
    timestamps['duration_hours'] = str((pd.Timestamp(df.index[-1]) -
                                        pd.Timestamp(df.index[0]))
                                       .seconds//3600.)

    metadata = {}
    metadata['measurements'] = measurements
    metadata['timestamps'] = timestamps
    print "Convertion: meatadata stored is:"
    pprint.PrettyPrinter(0).pprint(metadata)

    with pd.get_store(hdf_filename) as store:
        store['measurements'] = df
        store.root._v_attrs.metadata = metadata
    print 'Convertion: dataframe stored as meter in {:s}!'.format(hdf_filename)

if __name__ == '__main__':
    hdf_filename = 'meter_blued.h5'
    dataframe_to_meter(df, hdf_filename)
