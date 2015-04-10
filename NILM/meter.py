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
    """ Reference where the data of a meter is stored.

    Parameters
    ----------
    filename: str
        Path + filename of the HDFS file where the data is stored
        It can be a user or a meter HDFS file. For more informations
        on meter HDFS file, see NILM.converter.dataframe_to_meter function.

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
    """Main object of this disaggregation algorithm.

    Models a real meter. The data is in a HDFS store and can be loaded
    into the Measurements attribute. The data is referenced in the
    NILM.meter.Store object All the actions to disaggregate a meter
    are performed on the Meter object. Meter can be created from
    a NILM.User object, loaded from a meter HDFS file or created from
    a pandas.DataFrame with measurements data well designed.


    Parameters
    ----------
    metadata: dict, optional
        Contains additionnal informations on the meter.
        Example: timezone, start of the measurements etc...

    phases: list of str, optional
        List of phases measured by meter.

    power_types: list of str, optional
        List of power types measured by meter.
        Example: ['P', 'Q'], ['apparent', 'reactive']

    store: NILM.Store object, optional
        Where the data of the meter is stored.

    Attributes
    ----------
    metadata: dict
        Contains additionnal informations on the meter.
        Example: timezone, start of the measurements etc...

    phases: list of str
        List of phases measured by meter.

    power_types: list of str
        List of power types measured by meter.
        Example: ['P', 'Q'], ['apparent', 'reactive']

    store: NILM.Store object
        Where the data of the meter is stored.

    measurements: NILM.Measurements object
        Data of the meter. Measurements of powers for each timestamps. Requires
        to load the measurements of the meter to exist.

    events: NILM.Events object
        Events detected in the measurements. Requires to detect the events of
        the meter to exist.

    clusters: NILM.Clusters object
        Clusters of events detected. Requires to cluster the events of the
        meter to exist.

    appliance_models: NILM.ApplianceModels object
        Appliances models constructed with the clusters. Requires to model the
        appliance of the meter first.

    appliance_consumptions: NILM.ApplianceConsumptions object
        Consumptions of the disaggregated appliances. Requires to track the
        consumptions of the meter before.

    References
    ----------
    Hart, G. W. "Prototype nonintrusive appliance load monitor." (1985).
    """

    def __init__(self, metadata=None, phases=None, power_types=None,
                 store=None, ID=None):
        self.phases = phases
        self.metadata = metadata
        self.power_types = power_types
        self.store = store
        self.ID = ID

    @staticmethod
    def from_user(user, meter_ID):
        """Returns a Meter created from a User object.

        Parameters
        ----------
        user: NILM.User object
            User which own the meter.

        meter_ID: str
            Name of the meter. Needs to a a ID in the User.meters_ID list.
        """
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
        """Returns a Meter created from a meter HDFS file.

        For more informations on meter HDFS file,
        see NILM.converter.dataframe_to_meter function.

        Parameters
        ----------
        hdf_filename: str
            Path + filename of the meter HDFS file. For more informations on
            meter HDFS file, see NILM.converter.dataframe_to_meter function.
        """
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
        """Create a Meter from a dataframe.

        The meter is store in a meter HDFS file. For more informations on
        meter HDFS file, see NILM.converter.dataframe_to_meter function.

        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe containing the measurements of the powers for the
            phases and power types measured by a meter. The format of the
            DataFrame is specified in converter.dataframe_to_meter function.

         hdf_filename: str
            Path + filename of the meter HDFS file. To create a meter
            HDFS file, see NILM.converter.dataframe_to_meter function.
        """

        converter.dataframe_to_meter(df, hdf_filename)
        return Meter.from_meter_hdf(hdf_filename)

    def __repr__(self):
        return str(self.ID)

    def load_measurements(self, sampling_period):
        """ Create a NILM.Measurements object as Meter attribute.

        Parameters
        ----------
        sampling_period: int of float
            Elapse time between two measurements in second.
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
        """Create a NILM.Events object as Meter attribute.

        Parameters
        ----------
        detection_type: string
            Name of a detection function. This function will be used to detect
            events. Needs to be one of the keys of the dictionnary
            'detection_types' of NILM.Events object.

        detection_parameters: dict (optional)
            Arguments to be passed as argument of the function which will be
            used to detect the events. Arguments not informed will take the
            default value defined in the dictionnary 'detection_types'
            of NILM.Events object.
        """
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
        """Create a NILM.Clusters object as Meter attribute.

        Parameters
        ----------
        clustering_type: string
            Name of a clustering function. This function will be used to
            cluster the events. Needs to be one of the keys of the dictionnary
            'clustering_types' of NILM.Clusters object.

        clustering_parameters: dict (optional)
            Arguments to be passed as argument of the function which will be
            used to cluster the events. Arguments not informed will take the
            default value defined in the dictionnary 'clustering_types' of
            NILM.Clusters object.
            """
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
        """Create a NILM.ApplianceModels object as Meter attribute.

        Parameters
        ----------
        association_two_states_type: string
            Name of a function which model two-state appliances with available
            clusters. This function will be used to built tha appliance models.
            Needs to be one of the keys of the dictionnary
            'association_two_states_types' of NILM.ApplianceModels object.

        association_two_states_parameters: dict (optional)
            Parameters to be passed as arguments of the function which will be
            used to model the two-states appliances. Arguments not informed
            will take the default value defined in the dictionnary
            'association_two_states_types' of NILM.Clusters object.
        """
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
        """Create a NILM.ApplianceConsumptions object as Meter attribute.

        Parameters
        ----------
        tracking_type:: string
            Name of a function which track appliances consumptions of available
            appliances. This function will be used to compute the appliance
            mconsumptions. Needs to be one of the keys of the dictionnary
            'tracking_types' of NILM.ApplianceConsumptions object.

        tracking_parameters: dict (optional)
            Parameters to be passed as arguments of the function which will be
            used to track the appliances consumptions. Arguments not informed
            will take the default value defined in the dictionnary
            'tracking_types' of NILM.Consumptions object.
        """
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
