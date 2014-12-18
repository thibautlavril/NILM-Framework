# -*- coding: utf-8 -*-
import os
import pandas as pd


class User(object):
    """
    Represent a user of nilm. He is defined by an ID, a location and a file
    on the database where its data is stored. A user can have several meters.

    attributes: file, meters, metadata.
    """

    def __init__(self, hdf_filename):
        assert os.path.isfile(hdf_filename)
        self.file = hdf_filename
        self.meters = dict()
        self.metadata = dict()

    def load(self):
        """"
        Load the metadata of the file to create the meters and the metadata of
        our user
        """
        with pd.get_store(self.file) as store:
            self.metadata = store.root._v_attrs.metadata


if __name__ == "__main__":
    hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
    user1 = User(hdf_filename)
    user1.load()
    print user1.metadata
