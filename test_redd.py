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

meter.load_measurements(sampling_period=10)
meter.detect_events(detection_type='simple_edge')
#meter.detect_events(detection_type='steady_states', edge_threshold=30, state_threshold=10)
measures = meter.measurements
events = meter.events
plt.plot(measures.index, measures.values)
plt.plot(events.timestamps.values, events.P.values, 'ro')
plt.show()
meter.cluster_events('DBSCAN', eps=30)
meter.model_appliances('simple', distance_threshold = 100)
meter.track_consumptions('simple')

print len(meter.events)

"""
# Plot appliances
for phase, appliance in meter.appliance_consumptions.columns:
    print appliance
    #meter.measurements[phase][meter.power_types[0]].plot()
    #meter.appliance_consumptions[phase][appliance].plot(color='r')
    df0 = meter.measurements[phase][meter.power_types[0]]
    df = meter.appliance_consumptions[phase][appliance]
    plt.plot(df0.index, df0.values)
    plt.plot(df.index, df.values, 'r')
    plt.show()


phases = meter.phases
for phase in phases:
    print 'phase :', phase
    #meter.measurements[phase][meter.power_types[0]].plot()
    meter.appliance_consumptions[phase].sum(axis=1).plot(color='r')
    plt.show()

"""


