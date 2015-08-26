# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 12:30:14 2015

@author: thibaut
"""

from association_two_states import euclidian_cluster_metric
from association_two_states import simple_association_two_states
from association_two_states import dbscan_association_two_states
from association_two_states import affinity_propagation_association_two_states


__all__ = {
        "simple": {
            "model": simple_association_two_states,
            "parameters": {
                'distance_threshold': 35,
                'metric': euclidian_cluster_metric}},
        "dbscan": {
            "model": dbscan_association_two_states,
            "parameters": {
                'eps': 35,
                'min_samples': 1,
                'metric': euclidian_cluster_metric}}
}