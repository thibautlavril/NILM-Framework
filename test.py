# -*- coding: utf-8 -*-

import NILM as nilm
import matplotlib.pyplot as plt
import numpy as np

hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user_blued.h5'
user = nilm.User(hdf_filename)
meter = user.meters[0]


# meter.load_measurements?
meter.load_measurements(sampling_period=1)
phases = meter.phases
for phase in phases:
    print 'phase :', phase
    meter.measurements[phase].plot()

# meter.detect_events?
# nilm.Events?
# nilm.Events.detection_types
meter.detect_events(detection_type='steady_states', edge_threshold=70,
                    state_threshold=15)
#meter.detect_events(detection_type='simple_edge')
indexed_events = meter.events.set_index(['timestamps'])
for phase in phases:
    print 'phase :', phase
    meter.measurements[phase].plot()
    indexed_events.P[indexed_events.phase == phase].plot(style='o')
    plt.show()


# meter.cluster_events?
# nilm.Clusters?
# nilm.Clusters.clustering_types
meter.cluster_events('DBSCAN', eps=100, min_samples=1)
for phase in phases:
    ev = meter.events[meter.events.phase == phase]
    labels = ev.cluster.values
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = ev[meter.power_types].values[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=10)
    plt.show()



# meter.model_appliances?
# nilm.ApplianceModels?
# nilm.ApplianceModels.association_two_states_types
meter.model_appliances('simple', distance_threshold=80)

# meter.track_consumptions?
# nilm.ApplianceConsumptions
# nilm.ApplianceConsumptions.tracking_types
meter.track_consumptions('simple')

# Plot appliances
#for phase, appliance in meter.appliance_consumptions.columns:
#    print appliance
#    meter.measurements[phase][meter.power_types[0]].plot()
#    meter.appliance_consumptions[phase][appliance].plot(color='r')
#    plt.show()

phases = meter.phases
for phase in phases:
    print 'phase :', phase
    meter.measurements[phase][meter.power_types[0]].plot()
    meter.appliance_consumptions[phase].sum(axis=1).plot(color='r')
    plt.show()
