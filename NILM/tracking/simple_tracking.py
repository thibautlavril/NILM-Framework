# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:46:22 2015

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


def simple_tracking(timestamps, time_events, transitions, power_events):

    appliance_transitions, event_matched = deleting_anomamlies(transitions)
    # Initialization of dataframe with the appliance state and consumption
    df = pd.DataFrame(index=timestamps)
    appliance_state = np.zeros(len(timestamps))
    consumption = np.zeros(len(timestamps))
    df['state'] = appliance_state
    df['consumption'] = consumption

    time_on = timestamps[0]
    state_consumption = consumption[0]
    for transition, time, value in zip(appliance_transitions, time_events,
                                       power_events):
        if transition == 1:
            time_on = time  # We store the 'on' time
            # The consumption of the state is defined as the 'on' transition
            state_consumption = value
        if transition == -1:
            time_off = time
            # We select all the timestamps between time_on and time_off
            cond = (timestamps >= time_on) & (timestamps < time_off)
            # We set to 1 the state for the selected timestamps
            np.place(appliance_state, cond, 1)
            # We set to state_consumption the consumption for the selected ...
            # timestamps.
            np.place(consumption, cond, state_consumption)
    return consumption, event_matched
