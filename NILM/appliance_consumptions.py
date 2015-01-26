# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 09:30:35 2015

@author: thibaut
"""
import numpy as np
import pandas as pd
import tracking


class ApplianceConsumptions(pd.DataFrame):

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

if __name__ == '__main__':
    ap = ApplianceConsumptions('simple')
    ap.tracking(meter)










