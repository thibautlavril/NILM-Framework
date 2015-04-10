import pandas as pd
import numpy as np
import clustering
import matplotlib.pyplot as plt


class Clusters(pd.DataFrame):
    """
    This class inherits from pandas.DataFrame. The
    DataFrame is constructed by the method 'clustering'.

    Clustering method uses unsupervised learning to clusters
    events. The result is a DataFrame. The index is the
    ID of the cluster. The attributes of each cluster are
    the phase, the average powers, the number of events.
    The method used to cluster is choosed in the __init__ of Clusters.
    It needs to be one of the functions implemented in submodule
    clustering.

    Parameters
    ----------
    clustering_type: string
        Name of a clustering function. This function will be used to cluster
        the events. Needs to be one of the keys of the dictionnary
        'clustering_types'.

    clustering_parameters: dict (optional)
        Arguments to be passed as argument of the function which will be used
        to cluster the events. Arguments not informed will take the default
        value defined in the dictionnary 'clustering_types'.

    Attributes
    ----------
    clustering_types: dict, (class variable)
        Dictionnary wich lists all the functions to cluster
        events which are implementend in the submodule 'clustering'.
            Keys: str,
                Name of the clustering function implemented.
            Values: dict,
                'model': clustering function from 'clustering' submodule.
                'parameters': dictionary of default parameters of the
                clustering function.
        NOTE: When a new clustering function is implemented in 'clustering'
        submodule, the function and default parameters need to be entered into
        this dict.

    clustering_type: str
        Name of the clustering function used to cluster events.
        Needs to belong to be one key of the dictionnary 'clustering_types'.

    clustering_model: function
        Function which will be use to cluster events. This function is
        implemented in the submodule 'clustering'.

    clustering_parameters: dict
        Arguments passed to the clustering_model function. Its the dict
        'clustering_parameters' passed into the '__init__' function completed
        by default parameters (if not informed by clustering_parameters)
    """

    clustering_types = {
        "DBSCAN": {
            "model": clustering.DBSCAN,
            "parameters": {
                "eps": 35,
                "min_samples": 1}},
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
        """
        Clustering method uses unsupervised learning to clusters
        events. The result is a DataFrame. The index is the
        ID of the cluster. The attributes of each cluster are
        the phase, the average powers, the number of events.
        The method used to cluster is choosed in the '__init__' of Clusters
        by the parameter 'clustering_type'.
        It needs to be one of the functions implemented in submodule
        'clustering'.

        Parameters
        ----------
        meter: NILM.Meter
            Meter where the events are already detected.
        """

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

        for phase in phases:
            mask = (meter.events.phase == phase).values
            X = meter.events[features][mask].values
            model = clustering_model(**parameters)
            model.fit(X)
            # Different labels for each phase, but -1 when not clustered
            labels = model.labels_ + n_labels
            # but label -1 when not clustered
            np.place(labels, labels == n_labels-1, -1)
            labels_arr[mask] = labels
            n_labels = n_labels + model.labels_.max() + 1
        meter.events['cluster'] = labels_arr

        self.phases_ = meter.phases
        self.power_types_ = meter.power_types

        df = meter.events.groupby(['phase', 'cluster']).mean()
        serie_count = meter.events.groupby(['phase', 'cluster']).count()
        df['n_events'] = serie_count[meter.power_types[0]].values
        df = df.reset_index()
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
