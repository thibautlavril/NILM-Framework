import pandas as pd
import clustering


class Clusters(object):

    def __init__(self, meter, clustering_name, **kwargs):
        self._meter = meter
        assert clustering_name in clustering.clusteringDict
        self._clustering_name = clustering_name
        self._clustering_func = clustering.clusteringDict[clustering_name]
        parameters = clustering.parametersDict[clustering_name]
        for k, v in kwargs.iteritems():
            if k in parameters.keys():
                parameters[k] = v
        self._parameters = parameters
        
        

    @property
    def meter(self):
        return self._meter

    def clustering(self, clustering_type, **kwargs):
        assert (clustering_type in Clusters.clustering_types)
        phases = self.meter.events.columns.levels[0]
        df = pd.DataFrame()
        for phase in phases:
            dff = Clusters.clusteringDict[clustering_type](self.meter.events
                                                           [phase], **kwargs)
            dff['phase'] = phase
            df = df.append(dff)

        super(Clusters, self).__init__(df)

if __name__ == '__main__':
    from utils.tools import create_meter
    meter1 = create_meter()
    meter1.load_measurements(sampling_period=10)
    clusters = Clusters(meter1, 'DBSCAN', eps=2)