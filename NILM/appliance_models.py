# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:38:02 2015

@author: thibaut
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import AffinityPropagation, DBSCAN

  
def metric_cluster(x1, x2):
    assert x1.shape == x2.shape
    return  np.linalg.norm(x1 + x2)
        
    
def construct_distance_matrix(clusters, threshold_distance):
    """
    Construct a distance matrix between each clusters

    Parameters
    ----------
    clusters: NILM.clusters.Cluster object

    Returns
    -------
    distance_matrix_list = dict
        key: phase
        value: distance matrix between clusters for this phase
    """
    assert clusters.phase_by_phase
    phases = clusters.index.levels[0]
    power_types = clusters._features
    d_dict = {}
    for phase in phases:
        df = clusters.ix[phase]
        X = df[power_types].values
        d = pairwise_distances(X, metric=metric_cluster)
        d_dict[phase] = d
    return d_dict


def simple_association(X, threshold_distance):

    #  Construct the distance matrix D
    D = pairwise_distances(X, metric=metric_cluster)

    # Initialization
    d = 0  # Distance between two clusters
    n_appli = 0
    appliances = -1*np.ones_like(D[0])  # appliances set at -1

    while d < threshold_distance:

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
                n_appli += 1
                appliances[x] = n_appli
                appliances[y] = n_appli

    return appliances


class BuildApplianceModels(object):

    def __init__(self, kind, **parameters):
        self.kind = kind
        self.parameters = parameters
        self.model = None


class ApplianceModels(pd.DataFrame):

    def __init__(self, kind, parameters):
        super(ApplianceModels, self).__init__()
        self.building_model = BuildApplianceModels(kind, parameters)

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
        appliances = []

        for phase in phases:
            #  Select the clusters of this phase
            df = clusters.ix[phase]
            # Select the powers
            X = df[powers].values

            # Associate the clusters
            # TO DO replace by building_model.model
            appl = simple_association(X, threshold_distance)
            appliances.append(appl)

        # Add appliances label to meter.clusters
        appliances = np.array(appliances)
        self.clusters_appliances_ = appliances
        meter.clusters['appliances'] = appliances
        
        # Construct the pd.DataFrame Appliances Model
        df = meter.clusters.reset_index()
        df = df.set_index(['phase', 'appliances'])
        super(ApplianceModels, self).__init__(df)
            
            
            
            
            
            
            
            
            
            
            
        

if __name__ == '__main__':
    clusters = meter1.clusters
    dd = construct_distance_matrix(clusters, distance)
    D = dd['B']
    model = DBSCAN(eps = 50, min_samples=1, metric='precomputed')
    print model.fit_predict(D)
        