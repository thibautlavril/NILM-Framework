# -*- coding: utf-8 -*-
import os
import pandas as pd
from meter import Meter


class User(object):
    """ Represent a user.

    Each user is composed by a user metadata and a list of NILM.Meter.
    NILM.User are useful to store a dataset with severals meters.

    Parameters
    ----------
    hdf_filename: str
        Name (with relative or absolute path) of the HDFS file "*.h5" where
        the user is store. To create such files see NILM.converter module.

    ID: str, optional
        Name of the user. It is the name of the hdf_filename by default.


    Attributes
    ----------
    ID: str
        Name of the user. It is the name of the hdf_filename by default.

    metadata: dict of str
        Metadata stored in the HDFS file. It has informations on the user,
        the meters belonging to the user: meters ID, measurements of the meters
        etc ...

    filename: str
        Name of the file (with path) where the user is stored.

    meters_ID: list of str
        List with the meters_ID of the NILM.Meter belonging to the user.

    meters: list of NILM.Meter
        List containing the NILM.Meter objects.
    """

    def __init__(self, hdf_filename, ID=None):
        assert os.path.isfile(hdf_filename)
        with pd.get_store(hdf_filename) as store:
            metadata = store.root._v_attrs.metadata

        if ID is None:
            self.ID = hdf_filename.split('/')[-1]
        else:
            self.ID = ID
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
