import pandas as pd
import clustering


class Clusters(pd.DataFrame):

    clustering_types = ['dbscan', 'mean_shift']

    clusteringDict = {
        "dbscan": clustering.dbscan,
        "mean_shift": clustering.mean_shift_clustering
        }

    def __init__(self, meter):
        super(Clusters, self).__init__()
        self._meter = meter

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
    meter1.load_events(sampling_period=10)
    Clusters = Clusters(meter1)
    Clusters.clustering('dbscan', edge_threshold=100)