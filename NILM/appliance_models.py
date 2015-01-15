# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:38:02 2015

@author: thibaut
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import AffinityPropagation, DBSCAN

def euclidian_cluster(x1, x2):
    assert x1.shape == x2.shape
    return  np.linalg.norm(x1 + x2)


def simple_association(X, distance_threshold, metric):
    #  Construct the distance matrix D
    D = pairwise_distances(X, metric=metric)

    # Initialization
    d = 0  # Distance between two clusters
    n_appli = 0
    appliances = -1*np.ones_like(D[0])  # appliances set at -1

    while d < distance_threshold:

        # Find the new min > d
        D_masked = D[D > d]
        d = D_masked.min()  # Update d

        # Find coordinates of min
        xx, yy = np.indices(D.shape)
        xxx = xx[D == d]  # array of x
        yyy = yy[D == d]  # array of y

        for (x, y) in zip(xxx, yyy):
            if (appliances[x] == -1) & (appliances[y] == -1):
                # if x and y doesn't have appliance, set them at n_appli
                appliances[x] = n_appli
                appliances[y] = n_appli
                n_appli += 1

    return appliances


def dbscan_association(X, metric=euclidian_cluster, **dbscan_parameters):
    #  Construct the distance matrix D
    D = pairwise_distances(X, metric=euclidian_cluster)
    #  Compute a DBSCAN clustering for a distance matrix
    model = DBSCAN(metric='precomputed', **dbscan_parameters)
    appliances = model.fit_predict(D)
    return appliances


def affinity_propagation_association(X, **dbscan_parameters):
    pass
    


associationsDict = {
    "simple": {
        "model": simple_association,
        "parameters": {
            'distance_threshold': 35,
            'metric': euclidian_cluster
            }
        },
    "dbscan": {
        "model": dbscan_association,
        "parameters": {
            'eps': 35,
            'min_samples': 1,
            'metric': euclidian_cluster
            }
        }   
    }


class BuildApplianceModels(object):

    def __init__(self, name, **parameters):
        # Check name of method for association is valid
        assert name in associationsDict
        self.name = name

        # define model and default parameters from the dict
        Dict = associationsDict[name]

        self.model = Dict['model']

        self.parameters = Dict['parameters']
        # Add the parameters from **parameters in the dict
        for k, v in parameters.iteritems():
            self.parameters[k] = v


class ApplianceModels(pd.DataFrame):

    def __init__(self, name, **parameters):
        super(ApplianceModels, self).__init__()
        self.building_model = BuildApplianceModels(name, **parameters)

    def build_appliance_models(self, meter):
        #  Check that the clustering on meter was done
        try:
            meter.clusters
        except AttributeError:
            raise AttributeError('Cluster before building appliance models!')

        clusters = meter.clusters

        #  Take the list of phases and powers measured by meter
        powers = meter.power_types
        phases = meter.phases

        #  Check that the process is made phase by phase
        assert(meter.phase_by_phase)

        #  Initialization
        appliances = np.array([])

        for phase in phases:
            #  Select the clusters of this phase
            df = clusters.ix[phase]
            # Select the powers
            X = df[powers].values

            # Associate the clusters, the model use and the parameters
            # are stored in the building_model object
            model = self.building_model.model
            parameters = self.building_model.parameters
            appl = model(X, **parameters)
            appliances = np.append(appliances, appl)

        # Add appliances label to meter.clusters
        appliances = np.array(appliances)
        meter.clusters['appliances'] = appliances

        # Construct the pd.DataFrame Appliances Model
        df = meter.clusters.reset_index()
        df = df.set_index(['phase', 'appliances', 'cluster'])
        df = df.sortlevel([0, 1])
        super(ApplianceModels, self).__init__(df)


if __name__ == '__main__':
    appliance_models = ApplianceModels('dbscan')
    appliance_models.build_appliance_models(meter1)

        