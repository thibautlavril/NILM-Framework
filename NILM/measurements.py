# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 17:36:44 2014

@author: thibaut
"""
import pandas as pd
import preprocessing


class Measurements(pd.DataFrame):
    """
    Measurements object inherits from pandas.DataFrame. The
    DataFrame is constructed by the method 'load_data'.

    'load_data' method load the data referenced in the NILM.meter.Store object.
    The measurements are resampled with the sampling function implemented
    in preprocessing. Missing measurements are not handled.
    The result is a pandas.DataFrame:
        index: timestamp of the measurement.
        attributes:
            timestamp: timestamp of when the event was detect.
            ['A', 'B', ...]: phase where measurements is done
                (for all phases available)
            ['P', 'Q']: value of each measured power (for all powers
                available).

    TODO: Functions to detect/handle missing measurements.

    Parameters
    ----------
    sampling_period: int of float
        Elapse time between two measurements in second.

    Attributes
    ----------
    sampling_period: float
        Elapse time between two measurements in second.
    """

    def __init__(self, sampling_period):
        super(Measurements, self).__init__()
        self.sampling_period = float(sampling_period)

    def load_data(self, meter):
        """
        'load_data' method load the data referenced in the NILM.meter.Store
        object.
        The measurements are resampled with the sampling function implemented
        in preprocessing. Missing measurements are not handled.
        The result is a pandas.DataFrame:
            index: timestamp of the measurement.
            attributes:
                timestamp: timestamp of when the event was detect.
                ['A', 'B', ...]: phase where measurements is done
                    (for all phases available)
                ['P', 'Q']: value of each measured power (for all powers
                    available).

        TODO: Functions to detect/handle missing measurements.

        Parameters
        ----------
        meter: NILM.Meter
            Meter object which has a Store which references a metering data.
        """
        sampling_period = self.sampling_period

        hdf_filename = meter.store.filename
        key = meter.store.key

        with pd.get_store(hdf_filename) as store:
            df = store[key]

        if sampling_period is not None:
            df = preprocessing.resample(df, sampling_period)

        df = df.sort_index()
        df.index.name = 'timestamps'
        super(Measurements, self).__init__(df)
