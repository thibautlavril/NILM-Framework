# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:38:02 2015

@author: thibaut
"""

import pandas as pd
import numpy as np
import modeling


class ApplianceModels(pd.DataFrame):

    """
    This class inherits from pandas.DataFrame.

    The main method is the modeling of appliances. The modeling
    of appliances method take as input a meter
    (where the events are already clustered). It
    will model the appliances by grouping some clusters of events.
    The current algorithm allows only to model two-states-appliances.
    The clusters are defined in Clusters class. The modeling construct
    a pd.dataFrame where the columns are ['phase', 'appliance', 'transition'].
    Each row is a cluster. Therefore for each cluster an appliance number
    will be defined. This method can use diffent modeling functions.
    These functions are implemented in the submodule 'modeling'.
    The function used is choosed in the __init__ of ApplianceModels.

    The pandas.DataFrame constructed allows therefore to know at
    which appliance each cluster is associated.

    Parameters
    ----------
    association_two_states_type: string
        Name of the function used to create two-state
        appliance models. Needs to be one of the
        keys of the dictionnary association_two_states_types.
    association_two_sates_parameters: dict (optional)
        dict of parameters/value to be passed as argument of the
        function model_2states. Arguments not informed will
        take the default value defined in the dictionnary
        association_two_states_types.

    Attributes
    ----------
    association_two_states_types: dict, (class variable)
        Dictionnary wich lists all the methods to create two-states appliances
        implemented. The keys are the name of the methods to create two-states
        appliances implemented.. The values are dictionnary with two keys:
        'model' and 'parameters'. The value associated to 'model' is a
        function for which associate clusters to create two-states appliances.
        This function is implemented into the submodule 'modeling
        The values associated to 'parameters' is a dictionnary nwhich map
        the names of the arguments of the model with the default
        value of theses parameters. NOTE: When a new tracking function is
        implemented in 'modeling' submodule, the function and default
        parameters need to be entered into this dict.
    tracking_type: string
        Name of the tracking model used. Needs to belong to be one
        key of the dictionnary tracking_types.
    model_2states: function
        Function used to do the association_two_states. Function are
        implemented in the submodule 'modleing'.
    parameters_2states: dict
        dict of parameters/value to be passed as argument of the
        function model_2states.
    """

    association_two_states_types = {
        "simple": {
            "model": modeling.simple_association_two_states,
            "parameters": {
                'distance_threshold': 35,
                'metric': modeling.euclidian_cluster_metric}},
        "dbscan": {
            "model": modeling.dbscan_association_two_states,
            "parameters": {
                'eps': 35,
                'min_samples': 1,
                'metric': modeling.euclidian_cluster_metric}}
    }

    def __init__(self, association_two_states_type,
                 **association_two_sates_parameters):
        super(ApplianceModels, self).__init__()
        assert association_two_states_type in\
            ApplianceModels.association_two_states_types
        association_two_states_dict = ApplianceModels.\
            association_two_states_types[association_two_states_type]
        model_2states = association_two_states_dict['model']
        parameters_2states = association_two_states_dict['parameters']
        # Add the parameters from **parameters in the dict
        for k, v in association_two_sates_parameters.iteritems():
            parameters_2states[k] = v

        self.model_2states = model_2states
        self.parameters_2states = parameters_2states

    def modeling(self, meter):
        """
        The modeling of appliances method take as input a meter
        (where the events are already clustered). It
        will model the appliances by grouping some clusters of events.
        The current algorithm allows only to model two-states-appliances.
        The clusters are defined in Clusters class. The modeling construct
        a pd.dataFrame where the columns are:
        ['phase', 'appliance', 'transition'].
        Each row is a cluster. Therefore for each cluster an appliance number
        will be defined. 'transition' informed if it is an 'on' or a 'off'.
        This method can use diffent modeling functions.
        These functions are implemented in the submodule 'modeling'.
        The function used is choosed in the __init__ of ApplianceModels.

        Parameters
        ----------
        meter: NILM.Meter
            Meter where the appliance models are already construct.
        """

        #  Check that the clustering on meter was done
        clusters = meter.clusters

        #  Take the list of phases and powers measured by meter
        powers = meter.power_types
        phases = meter.phases

        # I.Modeling two states apliance

        #  Initialization
        appliances = -10*np.ones(len(clusters.index))
        transitions = np.zeros(len(clusters.index))
        n_appliances = 0
        model_2states = self.model_2states
        parameters_2states = self.parameters_2states

        for phase in phases:
            #  Select the clusters of this phase and with label != -1
            mask = ((clusters.phase == phase) & (clusters.cluster != -1)).values
            df = clusters[mask]
            # Select the powers
            X = df[powers].values

            # Associate the clusters to make appliances.
            # The model and the parameters used
            # are stored in the building_model object
            a = model_2states(X, **parameters_2states)
            a = np.where(a == -1, -1, a + n_appliances)
            n_appliances = max(a) + 1

            # Add if transition is 'on' or 'off'
            t = np.zeros_like(a)
            mask_2 = (a != -1)
            P = X[mask_2][:, 0]
            t[mask_2] = np.where(P > 0, 1, -1)
            appliances[mask] = a
            transitions[mask] = t

        # Add appliances label to meter.clusters
        meter.clusters['appliance'] = appliances
        meter.clusters['transition'] = transitions

        # Construct the pd.DataFrame Appliances Model
        df = meter.clusters.sort_index(by=['phase', 'appliance', 'transition'])
        df = df.set_index(['phase', 'appliance', 'transition'])
        df = df.reset_index()
        super(ApplianceModels, self).__init__(df)

if __name__ == '__main__':
    am = ApplianceModels('simple')
    am.modeling(meter)
