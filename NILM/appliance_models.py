# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:38:02 2015

@author: thibaut
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import AffinityPropagation, DBSCAN

  
def distance(x1, x2):
    assert x1.shape == x2.shape
    return  np.linalg.norm(x1 + x2)
        
    
def construct_distance_matrix(clusters, distance):
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
        d = pairwise_distances(X, metric=distance)
        d_dict[phase] = d
    return d_dict

def simple_association(D, threshold_similarity):
    d = 0
    distance = D.argmin(0)
    n_appli = 0
    associations = -1*np.ones_like(D[0])
    while d < threshold_similarity:
        xx, yy = np.indices(D.shape)
        D_masked = np.ma.array(D, mask = (D<=d))
        d = D_masked.min()
        mask_position = (D == d)
        xxx = xx[mask_position]
        yyy = yy[mask_position]

        for (x, y) in zip(xxx, yyy):
            if (associations[x] == -1) & (associations[y] == -1):
                n_appli += 1
                associations[x] = n_appli
                associations[y] = n_appli


class BuildApplianceModels(object):

    def __init__(self, kind, **parameters):
        self.kind = kind
        self.parameters = parameters


class ApplianceModels(pd.DataFrame):

    def __init__(self, kind, parameters):
        super(ApplianceModels, self).__init__()
        self.building = BuildApplianceModels(kind, parameters)
    
    def build_appliance_models(self, meter):
        try: meter.clusters
        except AttributeError: 
            raise AttributeError('Cluster before building appliance models!')

if __name__ == '__main__':
    clusters = meter1.clusters
    dd = construct_distance_matrix(clusters, distance)
    D = dd['B']
    model = DBSCAN(eps = 50, min_samples=1, metric='precomputed')
    print model.fit_predict(D)
        