# -*- coding: utf-8 -*-

import NILM as nl

hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
user1 = nl.User(hdf_filename)
user1.load()

meter1 = user1[0]
meter1.load_measurements(sampling_period=10)

detection_types = [
    "simple_edge",
    "steady_states"
]
detection_parameters = {
    "simple_edge": {
        "edge_threshold": 100
    },
    "steady_states": {
        "edge_threshold": 100,
        "state_threshold": 15
    }
}

detection_type = detection_types[1]
detection_parameter = detection_parameters[detection_type]


meter1.detect_events(detection_type, **detection_parameter)
