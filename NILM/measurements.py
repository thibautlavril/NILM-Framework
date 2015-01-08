# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 17:36:44 2014

@author: thibaut
"""
import os
import sys
import pandas as pd
from utils import sampling



class Measurements(pd.DataFrame):

    def __init__(self, meter):
        super(Measurements, self).__init__()
        self._meter = meter

    @property
    def meter(self):
        return self._meter

    @property
    def key(self):
        meter_id = self.meter.metadata['meter_id']
        key = "/meter{:d}/measurements".format(meter_id)
        return key

    def load_data(self, sampling_period=None, start=None,
                  end=None, chunk=None):
        hdf_filename = self.meter.store
        key = self.key
        if (start is not None) or (end is not None):
            raise NotImplementedError
        if chunk is not None:
            raise NotImplementedError
        with pd.get_store(hdf_filename) as store:
            df = store[key]
        if sampling_period is not None:
            float(sampling_period)
            df = sampling.resample(df, sampling_period)
        super(Measurements, self).__init__(df)


if __name__ == "__main__":
    from tools import create_meter
    meter1 = create_meter()
    p = Measurements(meter1)
    p.load_data(sampling_period=1)
