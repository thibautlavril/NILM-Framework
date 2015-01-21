# -*- coding: utf-8 -*-
import os
import pandas as pd
from meter import Meter


class User(object):
    """
    Represent a user of nilm. He is defined by an ID, a location and a file
    on the database where its data is stored. A user can have several meters.

    attributes: store, meters, metadata.
    """

    def __init__(self, hdf_filename):
        assert os.path.isfile(hdf_filename)
        with pd.get_store(hdf_filename) as store:
            metadata = store.root._v_attrs.metadata

        self.ID = hdf_filename.split('/')[-1]
        self.metadata = metadata
        self.filename = hdf_filename

        meters_ID = []
        for meter_ID in metadata['meters'].keys():
            meters_ID.append(meter_ID)
        self.meters_ID = meters_ID

        meters = []
        for meter_ID in metadata['meters'].keys():
            meter = Meter.from_user(self, meter_ID)
            meters.append(meter)
        self.meters = meters
    
    def __repr__(self):
        return str(self.ID)


if __name__ == "__main__":
    hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user_blued.h5'
    user = User(hdf_filename)
