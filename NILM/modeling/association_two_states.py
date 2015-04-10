# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 12:30:24 2015

@author: thibaut

Algorithms which associate clusters to model two states appliances
"""
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import AffinityPropagation, DBSCAN


def euclidian_cluster_metric(x1, x2):
    """Distance to measure the similarity between two clusters
    with OPPOSITE SIGN (to detect 'on' and 'off')
    """
    assert x1.shape == x2.shape
    return np.linalg.norm(x1 + x2)


def simple_association_two_states(X, distance_threshold, metric):
    """Associate clusters 2 by 2.

    Compute the distance between clusters of different signs.
    Associate the cluster 2 by 2 beginning by the clusters the nearest
    (with opposite sign). Continues until the distance (with opposite sign)
    between the nearest clusters are more than the threshold.

    Parameters
    ----------
    X: np.array of float (n_clusters, n_powers)
        matrix containg the different mean powers of the clusters
        (positions of centroids of clusters)

    distance_threshold: float
        maximum distance between clusters tollerated to associate two clusters

    metric: function
        metric used to measure the distance between two clusters. If clusters
        have same means with opposite signs the distance should be near 0.

    Returns
    -------
    appliances: numpy.array of int (n_clusters, )
        array containg the appliance choosen for each cluster.
    """
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
    """Associate clusters by density

    Proceed to DBSCAN algorith on pairwise distance matrix betwwen clusters.
    This matrix is computed with the metric given.
    Therefore more than 2 clusters can defined an appliance if they
    are very close.

    Parameters
    ----------
    X: np.array of float (n_clusters, n_powers)
        matrix containg the different mean powers of the clusters
        (positions of centroids of clusters)

    metric: function
        metric used to measure the distance between two clusters. If clusters
        have same means with opposite signs the distance should be near 0.

    dbscan_parameters: dict, optional
        Arguments to pass to the sklearn dbscan function.

    Returns
    -------
    appliances: numpy.array of int (n_clusters, )
        array containg the appliance choosen for each cluster.
    """
    #  Construct the distance matrix D
    D = pairwise_distances(X, metric)
    #  Compute a DBSCAN clustering for a distance matrix
    model = DBSCAN(metric='precomputed', **dbscan_parameters)
    appliances = model.fit_predict(D)
    return appliances


def affinity_propagation_association_two_states(X, **dbscan_parameters):
    pass
