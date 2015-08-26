# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 18:21:12 2014

@author: thibaut
"""

from dbscan import DBSCAN
from mean_shift import MeanShift

__all__ = {
        "DBSCAN": {
            "model": DBSCAN,
            "parameters": {
                "eps": 35,
                "min_samples": 1}},
            "MeanShift": {
                "model": MeanShift,
                "parameters": {}}}
