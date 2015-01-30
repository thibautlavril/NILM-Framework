# -*- coding: utf-8 -*-
import pandas as pd
import os

import converter
from measurements import Measurements
from events import Events
from clusters import Clusters
from appliance_models import ApplianceModels
from appliance_consumptions import ApplianceConsumptions


class Store(object):
    """ Adress where the data of a meter is stored.

    Parameters
    ----------
    filename: str
        Path + filename of the HDFS file where the data is stored
        It can be a user or a meter file.
    key: str
        Key used to index the data of the meter inside the HDFS file.
        If the file is a user file the key is "meter_ID/measurements".
        If the file is a meter the key is "measurements".

    Attributes
    ----------
    filename: str
        Path + filename of the HDFS file where the data is stored
        It can be a user or a meter file.
    key: str
        Key used to index the data of the meter inside the HDFS file.
        If the file is a user file the key is "meter_ID/measurements".
        If the file is a meter the key is "measurements".
    """

    def __init__(self, filename=None, key=None):
        self.filename = str(filename)
        self.key = str(key)

    def __repr__(self):
        return self.__dict__.__repr__()


class Meter(object):

    def __init__(self, metadata=None, phases=None, power_types=None,
                 store=None, ID=None):
        self.phases = phases
        self.metadata = metadata
        self.power_types = power_types
        self.store = store
        self.ID = ID

    @staticmethod
    def from_user(user, meter_ID):
        assert meter_ID in user.meters_ID
        metadata = user.metadata['meters'][meter_ID]

        measurements = metadata['measurements']
        phases = measurements['phases']
        power_types = measurements['power_types']

        key = "/".join((meter_ID, 'measurements'))
        store = Store(user.filename, key)

        meter = Meter(metadata, phases, power_types, store, meter_ID)
        return meter

    @staticmethod
    def from_meter_hdf(hdf_filename):
        assert os.path.isfile(hdf_filename)
        with pd.get_store(hdf_filename) as store:
            metadata = store.root._v_attrs.metadata

        meter_ID = hdf_filename.split('/')[-1]
        phases = list(metadata['measurements']['phases'])
        power_types = list(metadata['measurements']['power_types'])

        key = 'measurements'
        store = Store(hdf_filename, key)
        meter = Meter(metadata, phases, power_types, store, meter_ID)
        return meter

    @staticmethod
    def from_dataframe(df, hdf_filename):
        converter.dataframe_to_meter(df, hdf_filename)
        return Meter.from_meter_hdf(hdf_filename)

    def __repr__(self):
        return str(self.ID)

    def load_measurements(self, sampling_period):
        """
        Load the measurments in a pd.DataFrame. The elapsed time between each
        sample is given by sampling_period in seconds
        """
        measurements = Measurements(sampling_period)
        measurements.load_data(self)
        self.measurements_ = measurements
        print "Meter: measurements loaded!"

    @property
    def measurements(self):
        try:
            return self.measurements_
        except AttributeError:
            return AttributeError('Meter: load measurements before!')

    def detect_events(self, detection_type, **detection_parameters):
        events = Events(detection_type, **detection_parameters)
        events.detection(self)
        self.events_ = events
        print "Meter: events detected!"

    @property
    def events(self):
        try:
            return self.events_
        except AttributeError:
            return AttributeError('Meter: detect events before!')

    def cluster_events(self, clustering_type, features=None,
                       **clustering_parameters):
        clusters = Clusters(clustering_type, **clustering_parameters)
        clusters.clustering(self, features)
        self.clusters_ = clusters
        print "Meter: events clustered!"

    @property
    def clusters(self):
        try:
            return self.clusters_
        except AttributeError:
            return AttributeError('Meter: cluster events before!')

    def model_appliances(self, association_two_states_type,
                         **association_two_sates_parameters):
        appliance_models = ApplianceModels(association_two_states_type,
                                           **association_two_sates_parameters)
        appliance_models.modeling(self)
        self.appliance_models_ = appliance_models
        print "Meter: appliances modeled!"

    @property
    def appliance_models(self):
        try:
            return self.appliance_models_
        except AttributeError:
            return AttributeError('Meter: model appliances before!')

    def track_consumptions(self, tracking_type, **tracking_parameters):
        appliance_consumptions = ApplianceConsumptions(tracking_type,
                                                       **tracking_parameters)
        appliance_consumptions.tracking(self)
        self.appliance_consumptions_ = appliance_consumptions
        print "Meter: appliance consumptions tracked!"

    @property
    def appliance_consumptions(self):
        try:
            return self.appliance_consumptions_
        except AttributeError:
            return AttributeError('Meter: track appliances consumptions\
                                   before!')


if __name__ == '__main__':
    from user import User
    hdf_filename = '/Volumes/Stockage/DATA/DATA_BLUED/CONVERTED/user_blued.h5'
    user = User(hdf_filename)
    meter = user.meters[0]

    meter.load_measurements(sampling_period=10)
    meter.detect_events(detection_type='steady_states')
    meter.cluster_events('DBSCAN', eps=35)
    meter.model_appliances('simple')
    meter.track_consumptions('simple')
