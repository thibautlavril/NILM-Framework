import pandas as pd
import numpy as np
import clustering
import matplotlib.pyplot as plt

class Clusters(pd.DataFrame):

    def __init__(self, meter, clustering_name, 
                 phases_separation=True, features=None, **kwargs):
        super(Clusters, self).__init__()
        self._meter = meter
        assert clustering_name in clustering.clusteringDict
        self._clustering_name = clustering_name
        self._clustering_func = clustering.clusteringDict[clustering_name]
        self._phases_separation = phases_separation
        parameters = clustering.parametersDict[clustering_name]
        for k, v in kwargs.iteritems():
            parameters[k] = v
        self._parameters = parameters
        if (features is None) & (not phases_separation):
             self._features = self._meter.features
        elif (features is None) & (phases_separation):
            self._features = self._meter.features.levels[1]
        else:
            self._features = features
       
    def clustering(self):
        if not self._phases_separation:
            model = self._clustering_func(**self._parameters)
            X = self._meter.events[self._features].values
            model.fit(X)
            self._model = model
            self._fitted = True
            self._labels = model.labels_
            labels = model.labels_
            self._n_clusters = len(set(model.labels_)) - \
                (1 if -1 in model.labels_ else 0)
        else:
            labels = np.array([])
            label_origin = 0
            for phase in self._meter.phases:
                mask = (self._meter.events.phase == phase)
                X = self._meter.events[mask]
                X = X[self._features].values
                model = self._clustering_func(**self._parameters)
                model.fit(X)
                model.labels_ = model.labels_ + label_origin
                np.place(model.labels_, model.labels_==label_origin-1, -1)
                label_origin = label_origin + model.labels_.max() + 1
                labels = np.append(labels, model.labels_)
        labels = np.array(labels)
        self._meter.events['cluster'] = labels
        df = clusters._meter.events.groupby(['phase', 'cluster']).mean()
        columns = df.columns
        serie = clusters._meter.events.groupby(['phase', 'cluster']).count()
        df['count'] = serie[columns[0]].values
        super(Clusters, self).__init__(df)
                
        
    
    @property
    def fitted(self):
        try:
            return self._fitted
        except AttributeError:
            return False
    
    
    def plot_clusters(self):
        if not self._phases_separation:
            for phase in self._meter.phases:
                X = self._meter.events[phase].values
                labels = self._labels
                unique_labels = set(labels)
                colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
                for k, col in zip(unique_labels, colors):
                    class_member_mask = (labels == k)
                    xy = X[class_member_mask]
                    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col)
                plt.show()
        else:
            raise NotImplementedError


if __name__ == '__main__':
    from utils.tools import create_meter
    meter1 = create_meter()
    meter1.load_measurements(sampling_period=1)
    meter1.detect_events('steady_states')
    
    clusters = Clusters(meter1, 'MeanShift')
    clusters.clustering()
    b=clusters._meter.events.groupby(['phase', 'cluster']).mean()

  
    