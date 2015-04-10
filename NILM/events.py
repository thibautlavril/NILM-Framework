import pandas as pd
import detection


class Events(pd.DataFrame):

    """
    This class inherits from pandas.DataFrame. The
    DataFrame is construct by the method 'detection'.

    Detection method uses event detection methods to detect
    events in the measurments. The result is a DataFrame:
        index: ID of the event
        attributes:
            timestamp: timestamp of when the event was detect.
            phase: phase where the event is detected.
            ['P', 'Q']: value of the transition for each power (if available).
    The method used to detect events is choosed in the '__init__' of
    Events object. This needs to be one of the functions implemented in the
    submodule 'detection'.

    Parameters
    ----------
    detection_type: string
        Name of a detection function. This function will be used to detect
        events. Needs to be one of the keys of the dictionnary
        'detection_types'.

    detection_parameters: dict (optional)
        Arguments to be passed as argument of the function which will be used
        to detect the events. Arguments not informed will take the default
        value defined in the dictionnary 'detection_types'.

    Attributes
    ----------
    detection_types: dict, (class variable)
        Dictionnary wich lists all the functions to detect
        events which are implementend in the submodule 'detection'.
            Keys: str,
                Name of the detection function implemented.
            Values: dict,
                'model': detection function from 'detection' submodule.
                'parameters': dictionary of default parameters of the
                detection function.
        NOTE: When a new detection function is implemented in 'detection'
        submodule, the function and default parameters need to be entered into
        this dict.

    detection_type: str
        Name of the detection function used to cluster events.
        Needs to belong to be one key of the dictionnary 'detection_types'.

    detection_model: function
        Function which will be use to cluster events. This function is
        implemented in the submodule 'detection'.

    detection_parameters: dict
        Arguments passed to the detection_model function. Its the dict
        'detection_parameters' passed into the '__init__' function completed
        by default parameters (if not informed by detection_parameters)
    """

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
        """
        Detection method uses event detection methods to detect
        events in the measurements. The result is a DataFrame:
            index: ID of the event
            attributes:
                timestamp: timestamp of when the event was detect.
                phase: phase where the event is detected.
                ['P', 'Q']: values of the transition for each power
                    (if available).
        The method used to detect events is choosed in the '__init__' of
        Events object. This needs to be one of the functions implemented in the
        submodule 'detection'.

        Parameters
        ----------
        meter: NILM.Meter
            Meter where the measurements are already loaded.
        """

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
