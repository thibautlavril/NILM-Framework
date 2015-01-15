# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:38:02 2015

@author: thibaut
"""

import pandas as pd

class BuildApplianceModels(object):
    
    def __init__(self, kind, parameters):
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
        