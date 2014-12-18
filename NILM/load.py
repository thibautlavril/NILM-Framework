# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:24:21 2014

@author: thibaut
"""

from user import User


def load_file(hdf_filename=
              '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'):
    user = User()
    user.load(hdf_filename)
    return user


def load_meter(hdf_filename=
               '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'):
    user = User()
    user.load(hdf_filename)
    meters_list = user.metadata['meters'].keys()
    meter = user.meters[meters_list[0]]
    return meter
