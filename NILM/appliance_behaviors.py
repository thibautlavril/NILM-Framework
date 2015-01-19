# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 09:30:35 2015

@author: thibaut
"""
import numpy as np
import pandas as pd


def deleting_anomamlies(transitions):

    # Initilization, we consider that the previous transition ...
    # was a off, and therefore the appliance is in state off
    previous_transition = -1
    index_previous = None

    transition_matched = np.full_like(transitions, False, dtype=bool)
    appliance_transitions = np.zeros_like(transitions)

    for index, transition in enumerate(transitions):
        # if transition is a 'turning on' we do nothing
        if transition == 1:
            pass
            

        # if transition is a 'turning off' ...
        elif transition == -1:
            if previous_transition == 1:
                # and if the previous one is a 'turning on'
                # We can match the two transitions!
                transition_matched[index_previous] = True
                appliance_transitions[index_previous] = 1
                transition_matched[index] = True
                appliance_transitions[index] = -1
            if previous_transition == -1:
                pass

        # Update
        previous_transition = transition
        index_previous = index

    return appliance_transitions, transition_matched


def build_consumption(timestamps, time_events, appliance_transitions,
                      transitions_values):
    # Initialization of dataframe with the appliance state and consumption
    df = pd.DataFrame(index=timestamps)
    appliance_state = np.zeros(len(timestamps))
    consumption = np.zeros(len(timestamps))
    df['state'] = appliance_state
    df['consumption'] = consumption

    time_on = timestamps[0]
    state_consumption = consumption[0]
    for transition, time, value in zip(appliance_transitions, time_events,
                                       transitions_values):
        if transition == 1:
            time_on = time  # We store the 'on' time
            # The consumption of the state is defined as the 'on' transition
            state_consumption = value
        if transition == -1:
            time_off = time
            # We select all the timestamps between time_on and time_off
            cond = (timestamps >= time_on) & (timestamps < time_off)
            # We set to 1 the state for the selected timestamps
            df['state'] = np.where(cond, 1, df['state'])
            # We set to state_consumption the consumption for the selected ...
            # timestamps.
            df['consumption'] = np.where(cond, state_consumption,
                                         df['consumption'])
    return df


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


class ApplianceBehavior(pd.DataFrame):

    def __init__():
        super(ApplianceBehavior, self).__init()

    def build_consumptions(self, meter):
        assert meter.phase_by_phase # Check that meter disagregate by phase

        phases = meter.phases
        powers = meter.power_types
        power_main = powers[0]

        df_app = meter.appliance_models.reset_index()
        df_eve = meter.events.reset_index()

        df = pd.merge(df_app[['phase', 'cluster', 'appliance', 'transition']],
                      df_eve, on=['phase', 'cluster'])
        
        timestamps = meter.measurements.index
        
        consumptions = pd.DataFrame(index = timestamps)
        
        for phase in phases:
            power = meter.measurements[phase]['P']
            mask = (df['phase'] == phase)
            appliances = set(df[mask]['appliance'].tolist())
            appliances = [app for app in appliances if app != -1]
            for appliance in appliances:
                mask = (df['phase'] == phase) & (df['appliance'] == appliance)
                df2 = df[mask].sort(columns=['index'])
                transitions = df2['transition'].values
                appliance_transitions, transition_matched = deleting_anomamlies(transitions)
                df2['transition'] = appliance_transitions
                df2['transition_matched'] = transition_matched
                time_events = df2['index'].values
                transitions_values = df2[power_main]
                conso = build_consumption(timestamps, time_events, appliance_transitions,
                      transitions_values)
                conso = conso['consumption'].values
                name = 'appliance_' + str(int(appliance))
                consumptions[name] = conso
        super(ApplianceBehavior, self).__init__(consumptions)
                
                
                
                
            
            
                

     
        
        
