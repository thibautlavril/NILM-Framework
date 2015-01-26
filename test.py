# -*- coding: utf-8 -*-

import NILM as nilm
import matplotlib.pyplot as plt

hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user_blued.h5'
user = nilm.User(hdf_filename)
meter = user.meters[0]

meter.load_measurements(sampling_period=10)
meter.detect_events(detection_type='steady_states')
meter.cluster_events('DBSCAN', eps=35)
meter.model_appliances('simple')
meter.track_consumptions('simple')

# Plot appliances
for phase, appliance in meter.appliance_consumptions.columns:
    print appliance
    meter.measurements[phase][meter.power_types[0]].plot()
    meter.appliance_consumptions[phase][appliance].plot(color='r')
    plt.show()

phases = meter.phases
for phase in phases:
    print 'phase :', phase
    meter.measurements[phase][meter.power_types[0]].plot()
    meter.appliance_consumptions[phase].sum(axis=1).plot(color='r')
    plt.show()
