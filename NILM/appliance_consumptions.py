# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 09:30:35 2015

@author: thibaut
"""
import numpy as np
import pandas as pd
import tracking


class ApplianceConsumptions(pd.DataFrame):
    """
    This class inherits from a pandas.DataFrame.

    The main method is the tracking of appliances. The tracking
    of appliances method take as input a meter
    (where the appliance models are already constructed). It
    will track the behaviour appliances defined in ApplianceModels
    class. The tracking construct a pd.dataFrame where the columns
    are the appliance detected and the rows consumption tracked for each
    timestamps. This method can diffent tracking functions. These functions
    are implemented in the submodule 'tracking'. The function used is choosed
    in the __init__ of ApplianceConsumptions.

    The pandas.DataFrame constructed allows therefore to know all the
    consumptions of all appliances detected.

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

    Attributes
    ----------
    tracking_types: dict, (class variable)
        Dictionnary with all the tracking methods implemented. The keys are
        the name of the tracking methods implemented. The values are
        dictionnary with two keys: 'model' and 'parameters'. The value
        associated to 'model' is a function for tracking. This function
        is implemented into the submodel 'tracking'. The values associated
        to 'parameters' is a dictionnary name:value of default parameters of
        the function in 'model'. NOTE: When a new tracking function is
        implemented in 'tracking' submodule, the function and default
        parameters need to be entered into this dict.

    tracking_type: string
        Name of the tracking model used. Needs to belong to be one
        key of the dictionnary tracking_types.

    tracking_model: function
        Function used to do the tracking. Function are in the submodule
        'tracking'.
    """

    tracking_types = {
        "simple": {
            "model": tracking.simple_tracking,
            "parameters": {
                }
            }
    }

    def __init__(self, tracking_type, **tracking_parameters):
        super(ApplianceConsumptions, self).__init__()

        # Check name of method for tracking is valid
        assert tracking_type in ApplianceConsumptions.tracking_types
        # define model and default parameters from the dict
        tracking_dict = ApplianceConsumptions.tracking_types[tracking_type]
        model = tracking_dict['model']
        parameters = tracking_dict['parameters']
        # Add the parameters from **parameters in the dict
        for k, v in tracking_parameters.iteritems():
            parameters[k] = v

        self.tracking_type = tracking_type
        self.tracking_model = model
        self.tracking_parameters = parameters

    def tracking(self, meter):
        """
        The tracking of appliances method take as input a
        meter (where the appliance models are already constructed). It
        will track the behaviour appliances defined in ApplianceModels
        class. The tracking construct a pd.dataFrame where the columns
        are the appliance detected and the rows consumption tracked for each
        timestamps. This method can diffent tracking functions. These functions
        are implemented in the submodule 'tracking'. The function used is
        choosen in the __init__ of ApplianceConsumptions.

        The pandas.DataFrame constructed allows therefore to know all the
        consumptions of all appliances detected.

        Parameters
        ----------
        meter: NILM.Meter
            Meter where the appliance models are already built.
        """

        tracking_model = self.tracking_model
        tracking_parameters = self.tracking_parameters

        phases = meter.phases
        powers = meter.power_types
        P = powers[0]

        # Check if appliance models are built
        meter.appliance_models

        clusters = meter.clusters
        events = meter.events

        df = pd.merge(events, clusters[['phase', 'cluster', 'appliance',
                      'transition']], on=['phase', 'cluster'])

        df = df.sort_index(by=['phase', 'appliance', 'timestamps'])

        event_matched_arr = np.zeros(len(df.index), dtype='bool')

        timestamps = meter.measurements.index

        consumptions = pd.DataFrame(index=timestamps)

        for phase in phases:
            mask = (df['phase'] == phase)
            appliances = set(df[mask]['appliance'].tolist())
            appliances = [app for app in appliances if app >= 0]
            for appliance in appliances:
                # Extract transitions, values of transitions ...
                mask = (df['phase'] == phase) & (df['appliance'] == appliance)
                mask = mask.values
                transitions = df[mask]['transition'].values
                power_events = df[mask][P].values
                time_events = df[mask]['timestamps'].values

                conso_appliance, event_matched = \
                    tracking_model(timestamps, time_events, transitions,
                                   power_events, **tracking_parameters)
                name = 'appliance_' + str(int(appliance))
                cols = (phase, name)
                consumptions[cols] = conso_appliance
                event_matched_arr[mask] = event_matched
        consumptions.columns = pd.MultiIndex.from_tuples(consumptions.columns)
        df['event_matched'] = event_matched_arr

        # We sort df like events are sorted
        df = df.sort_index(by=['phase', 'timestamps'])
        meter.events['event_matched'] = df['event_matched'].values
        super(ApplianceConsumptions, self).__init__(consumptions)
