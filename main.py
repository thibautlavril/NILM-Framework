# -*- coding: utf-8 -*-

import NILM as nilm
import matplotlib.pyplot as plt

hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user1.h5'
user1 = nilm.User(hdf_filename)
user1.load()

meter1 = user1[0]

meter1.load_measurements(sampling_period=1)
meter1.detect_events(detection_type='steady_states', edge_threshold=100)
meter1.cluster_events(clustering_type='DBSCAN', phases_separation=True,
                      features=None, eps=35)
meter1.model_appliances(modeling_type='simple')
meter1.track_behaviors()

# Plot appliances
for phase, appliance in meter1.appliance_behaviors.columns:
    print appliance
    meter1.measurements[phase][meter1.power_types[0]].plot()
    meter1.appliance_behaviors[phase][appliance].plot(color='r')
    plt.show()
