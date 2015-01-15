# -*- coding: utf-8 -*-
import pandas as pd
from measurements import Measurements
from events import Events
from clusters import Clusters


class Meter(object):

    def __init__(self, user, meter_name):
        self._user = user
        assert meter_name in user.metadata['meters']
        self.name = meter_name
        self.metadata = user.metadata['meters'][meter_name]
        self.state = dict()
        self.state['data_loaded'] = False
        self.state['event_detected'] = False
        self.measurements = Measurements(self)
        self.events = Events(self)
    
    @property
    def features(self):
        columns = self.metadata['measurements']
        features = pd.MultiIndex.from_tuples(columns)
        return features
    
    @property
    def phases(self):
        return self.features.levels[0]

    @property
    def store(self):
        """ Get the store"""
        return self._user.store

    @property
    def user(self):
        """ Get the user"""
        return self._user

    def __repr__(self):
        dict_repr = dict()
        dict_repr["meter_id"] = self.metadata['meter_id']
        dict_repr["disaggregation_state"] = self.state
        g = dict_repr.__repr__()
        return g


    def load_measurements(self, sampling_period=1):
        """
        Load the measurments in a pd.DataFrame. The elapsed time between each
        sample is given by sampling_period in seconds
        """
        self.measurements.load_data(sampling_period)
        self.state['data_loaded'] = True
        self.state['sampling'] = '{:d}s'.format(sampling_period)

    def detect_events(self, detection_type='steady_states', **kwargs):
        assert self.state["data_loaded"]
        self.events.detection(detection_type, **kwargs)
        self.state['event_detected'] = True
        self.state['detection_type'] = detection_type
    
    def cluster_events(self, clustering_type='DBSCAN', phases_separation=True,
                       features=None, **clustering_parameters):
        assert self.state['event_detected']
        self.clusters = Clusters(self, 'DBSCAN',
                                 phases_separation=True, features=None,
                                 **clustering_parameters)

        self.clusters.clustering()
        self.state['clustering'] = True
    


if __name__ == '__main__':
    from utils.tools import create_user
    user1 = create_user()
    meter1_name = user1.metadata['meters'].keys()[0]
    meter1 = Meter(user1, meter1_name)
    meter1.load_measurements(sampling_period=1)
    meter1.detect_events(detection_type='steady_states', edge_threshold=100)
    meter1.cluster_events(clustering_type='DBSCAN', phases_separation=True,
                       features=None, eps=35)
