# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:46:22 2015

@author: thibaut
"""

import numpy as np
import pandas as pd


def simple_tracking(timestamps, time_events, transitions, power_events):
    """Compute the consumption of one appliance for all timestamps

    Use a simple tracking for two-states appliances. Only events 'on'
    matched with an event 'off' are considered. Events mismatched are just
    labelled as mismatched.

    Parameters
    ----------
    timestamps: pandas.DateTimeIndex (n_measures, )
        timestamps given by the meter's measurements

    time_events: pandas.DateTimeIndex (n_events, )
        timestamps where all the events of the appliance considered occur.

    transitions: numpy.array of int (n_events, )
        class of transitions (-1 for 'off', 1 for 'on' for 2 states appliances)

    power_events: numpy.array of float (n_events, )
        power value of events (only main power now)

    Returns
    -------
    consumptions: np.array of float (n_measures, )
        consumption of the appliance for each timestamps of the meter

    event_matched: np.array of bools (n_events, )
        True if the corresponding event was match with another event, False
        otherwise.
    """
    appliance_transitions, event_matched = deleting_anomalies(transitions)
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


def deleting_anomalies(transitions):
    """Change transitions to delete anomalies

    Delete anomalies two-states appliances. Deletes transitons 'on' which
    are not followed by transitions 'off'. A new transition array is construct
    Transitions non matched are labelled as mismatched.

    Parameters
    ----------
    transitions: numpy.array of int (n_events, )
        class of transitions (-1 for 'off', 1 for 'on' for 2 states appliances)
        with anomalies: ('on','on') for example.

    Returns
    -------
    appliances_transitions: numpy.array of int (n_events, )
        class of transitions (-1 for 'off', 1 for 'on' for 2 states appliances)
        without anomalies. Non matched transitions have label 0.

    transition_matched: np.array of bools (n_events, )
        True if the corresponding transition was match with another
        transition, False otherwise.
    """
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
