# -*- coding: utf-8 -*-

import NILM as nl

hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
user1 = nl.User(hdf_filename)
user1.load()

meter1 = user1[0]
meter1.load_measurements(sampling_period=10)
meter1.detect_events(detection_type='simple_edge')
