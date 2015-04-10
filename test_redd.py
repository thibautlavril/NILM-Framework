# -*- coding: utf-8 -*-

import pandas as pd
from os.path import isfile
import NILM as nilm
import matplotlib.pyplot as plt


redd_file = '/Volumes/Stockage/DATA/DATA_REDD/RAW/low_freq/house_1/channel_1.dat'
assert isfile(redd_file)

col = pd.MultiIndex.from_tuples([('A', 'P')])
df = pd.read_csv(redd_file, names=col, header=None, index_col=0, sep=' ', nrows=50000)
df.index = pd.to_datetime(df.index, unit='s', utc=True)

hdf_filename = '/Volumes/Stockage/DATA/Meters/meter_redd_1.h5'
meter = nilm.Meter.from_dataframe(df, hdf_filename)

meter.load_measurements(sampling_period=100)
meter.detect_events(detection_type='steady_states')
meter.cluster_events('DBSCAN', eps=10)
meter.model_appliances('simple', distance_threshold = 100)
meter.track_consumptions('simple')

"""
# Plot appliances
for phase, appliance in meter.appliance_consumptions.columns:
    print appliance
    #meter.measurements[phase][meter.power_types[0]].plot()
    meter.appliance_consumptions[phase][appliance].plot(color='r')
    plt.show()

phases = meter.phases
for phase in phases:
    print 'phase :', phase
    #meter.measurements[phase][meter.power_types[0]].plot()
    meter.appliance_consumptions[phase].sum(axis=1).plot(color='r')
    plt.show()

"""


