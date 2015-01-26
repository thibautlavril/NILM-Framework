import pandas as pd
import numpy as np
import clustering
import matplotlib.pyplot as plt


class Clusters(pd.DataFrame):

    clustering_types = {
        "DBSCAN": {
            "model": clustering.DBSCAN,
            "parameters": {
                "eps": 35,
                "min_samples": 2}},
            "MeanShift": {
                "model": clustering.MeanShift,
                "parameters": {}}}

    def __init__(self, clustering_type, **clustering_parameters):
        super(Clusters, self).__init__()
        # Check name of method for association is valid
        assert clustering_type in Clusters.clustering_types
        # define model and default parameters from the dict
        clustering_dict = Clusters.clustering_types[clustering_type]
        model = clustering_dict['model']
        parameters = clustering_dict['parameters']
        # Add the parameters from **parameters in the dict
        for k, v in clustering_parameters.iteritems():
            parameters[k] = v

        self.clustering_type = clustering_type
        self.clustering_model = model
        self.clustering_parameters = parameters

    def clustering(self, meter, features=None):
        phases = meter.phases
        clustering_model = self.clustering_model
        parameters = self.clustering_parameters
        n_events = len(meter.events.index)
        if features is None:
            features = meter.power_types
        else:
            # Check that features are in powers measured by meter
            assert np.in1d(features, meter.power_types).all()

        n_labels = 0
        labels_arr = -10*np.ones(n_events)
        i = 0

        for phase in phases:
            mask = (meter.events.phase == phase)
            X = meter.events[features][mask].values
            n = len(X)
            model = clustering_model(**parameters)
            model.fit(X)
            # Different labels for each phase, but -1 when not clustered
            labels = model.labels_ + n_labels
            # but label -1 when not clustered
            np.place(labels, labels == n_labels-1, -1)
            labels_arr[i:i+n] = labels
            n_labels = n_labels + model.labels_.max() + 1
            i = n
        meter.events['cluster'] = labels_arr

        self.phases_ = meter.phases
        self.power_types_ = meter.power_types

        df = meter.events.groupby(['phase', 'cluster']).mean()
        serie_count = meter.events.groupby(['phase', 'cluster']).count()
        df['count'] = serie_count[meter.power_types[0]].values
        super(Clusters, self).__init__(df)

    def plot_clusters_2D(self, meter):
        phases = meter.phases
        power_types = meter.power_types
        assert len(power_types) == 2
        for phase in phases:
            mask = (meter.events.phase == phase)
            X = meter.events[power_types][mask].values
            labels = meter.events['cluster'][mask].values
            unique_labels = set(labels)
            colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
            for k, col in zip(unique_labels, colors):
                if k == -1:
                    # Black used for noise.
                    col = 'k'
                class_member_mask = (labels == k)
                xy = X[class_member_mask]
                plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col)
            plt.show()
