# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 09:30:35 2015

@author: thibaut
"""
import numpy as np
import pandas as pd

trackingDict = {
    "simple": {
        "model": simple_tracking,
        "parameters": {
            }
        }
    }


class TrackApplianceBehavior(object):

    def __init__(self, name, **parameters):
        # Check name of method for association is valid
        assert name in trackingDict
        self.name = name

        # define model and default parameters from the dict
        Dict = trackingDict[name]

        self.model = Dict['model']

        self.parameters = Dict['parameters']
        # Add the parameters from **parameters in the dict
        for k, v in parameters.iteritems():
            self.parameters[k] = v


class ApplianceBehavior(pd.adtaFrame):
    pass
