# -*- coding: utf-8 -*-
from collections import OrderedDict
from store import Store


class Meter(object):

    def __init__(self):
        self.metadata = dict()
        self.store = str()

    def load(self, user, meter_name):
            self.store = user.store
            assert meter_name in user.metadata['meters']
            self.metadata = user.metadata['meters'][meter_name]

if __name__ == '__main__':
    from user import User
    hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
    user1 = User()
    user1.load(hdf_filename)
    meter1_name = user1.metadata['meters'].keys()[0]
    meter1 = Meter()
    meter1.load(user1, meter1_name)
