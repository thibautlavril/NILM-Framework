# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 17:36:44 2014

@author: thibaut
"""

import pandas as pd
from load import load_meter


class Measurements(pd.DataFrame):

    def __init__(self, meter):
        super(Measurements, self).__init__()
        self.meter = meter

    @property
    def key(self):
        meter_id = self.meter.metadata['meter_id']
        key = "/meter{:d}/measurements".format(meter_id)
        return key

    def _load(self, meter, sampling=None):
        hdf_filename = meter.store
        with pd.get_store(hdf_filename) as store:
            df = store[self.key]
        if sampling is not None:
            raise NotImplementedError
        super(Measurements, self).__init__(df)


if __name__ == "__main__":
    meter = load_meter()
    p = Measurements(meter)
    p._load(meter, sampling=1)
