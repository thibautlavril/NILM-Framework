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

    def __init__(self):
        self.store = str()
        self.meters = dict()
        self.metadata = dict()

    def load(self, hdf_filename):
        """"
        Load the metadata of the file to create the meters and the metadata of
        our user
        """
        assert os.path.isfile(hdf_filename)
        self.store = hdf_filename
        with pd.get_store(self.store) as store:
            self.metadata = store.root._v_attrs.metadata
        for meter_name in self.metadata['meters'].keys():
            meter = Meter(self, meter_name)
            self.meters[meter_name] = meter

if __name__ == "__main__":
    hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
    user1 = User()
    user1.load(hdf_filename)
    print user1.metadata['meters'].keys()
