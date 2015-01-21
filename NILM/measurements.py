# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 17:36:44 2014

@author: thibaut
"""
import pandas as pd
import preprocessing


class Measurements(pd.DataFrame):

    def __init__(self, sampling_period):
        super(Measurements, self).__init__()
        self.sampling_period = float(sampling_period)

    def load_data(self, meter):
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
