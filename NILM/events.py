import pandas as pd
import detection


class Events(pd.DataFrame):

    detection_types = {
        "simple_edge": {
            "model": detection.simple_edge,
            "parameters": {
                "edge_threshold": 70}},
        "steady_states": {
            "model": detection.steady_states,
            "parameters": {
                "edge_threshold": 70,
                "state_threshold": 15}}}

    def __init__(self, detection_type, **detection_parameters):
        super(Events, self).__init__()
        # Check name of method for association is valid
        assert detection_type in Events.detection_types

        # define model and default parameters from the dict
        detection_dict = Events.detection_types[detection_type]
        model = detection_dict['model']
        parameters = detection_dict['parameters']
        # Add the parameters from **parameters in the dict
        for k, v in detection_parameters.iteritems():
            parameters[k] = v

        self.detection_type = detection_type
        self.detection_model = model
        self.detection_parameters = parameters

    def detection(self, meter):
        phases = meter.phases
        model = self.detection_model
        parameters = self.detection_parameters
        df = pd.DataFrame()
        for phase in phases:
            measurements = meter.measurements[phase]
            dff = model(measurements, **parameters)
            dff['phase'] = phase
            df = df.append(dff)
        df = df.reset_index()
        super(Events, self).__init__(df)
