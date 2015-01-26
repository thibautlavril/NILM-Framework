# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 12:30:24 2015

@author: thibaut
"""
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import AffinityPropagation, DBSCAN


def euclidian_cluster_metric(x1, x2):
    assert x1.shape == x2.shape
    return np.linalg.norm(x1 + x2)


def simple_association_two_states(X, distance_threshold, metric):
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


def dbscan_association_two_states(X, metric, **dbscan_parameters):
    #  Construct the distance matrix D
    D = pairwise_distances(X, metric)
    #  Compute a DBSCAN clustering for a distance matrix
    model = DBSCAN(metric='precomputed', **dbscan_parameters)
    appliances = model.fit_predict(D)
    return appliances


def affinity_propagation_association_two_states(X, **dbscan_parameters):
    pass
