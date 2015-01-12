import pandas as pd
import detection


class Events(pd.DataFrame):
    
    detection_types = {
            "simple_edge": detection.simple_edge,
            "steady_states": detection.steady_states
        }


    def __init__(self, meter):
        super(Events, self).__init__()
        self._meter = meter

    @property
    def meter(self):
        return self._meter

    def detection(self, detection_type, phases_separation=False, **kwargs):
        assert (detection_type in Events.detection_types)
        phases = self.meter.measurements.columns.levels[0]
        detection_func = Events.detection_types[detection_type]
        df = pd.DataFrame()
        
        if phases_separation:
            for phase in phases:
                dff = detection_func(self.meter.measurements[phase], **kwargs)
                dff['phase'] = phase
                df = df.append(dff)
        else:
            
            df = detection_func(self.meter.measurements, **kwargs)

        super(Events, self).__init__(df)

if __name__ == '__main__':
    from utils.tools import create_meter
    meter1 = create_meter()
    meter1.load_measurements(sampling_period=10)
    events = Events(meter1)
    events.detection('simple_edge', edge_threshold=100)
