# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 18:21:12 2014

@author: thibaut
"""

from DBSCAN import DBSCAN
from MeanShift import MeanShift

clusteringDict = {
    "DBSCAN": DBSCAN,
    "MeanShift": MeanShift
    }

parametersDict = {
    "DBSCAN": {"eps": 35, "min_samples": 1},
    "MeanShift": {}
    }