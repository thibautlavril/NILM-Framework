# import pandas as pd
from sklearn.cluster import MeanShift, estimate_bandwidth
# import numpy as np

# Remark continue to correct it


class MeanShift(MeanShift):

    pass

# def mean_shift_clustering(pair_buffer_df, features):
#     # Creating feature vector
#     cluster_df = pd.DataFrame()
#     if 'active' in features:
#         fmean = lambda row: (np.fabs(row['T1 Active']) +
#                              np.fabs(row['T2 Active'])) / 2
#         cluster_df['active'] = pd.Series(pair_buffer_df.apply(fmean, axis=1),
#                                          index=pair_buffer_df.index)
#     if 'reactive' in features:
#         cluster_df['reactive'] = pd.Series(pair_buffer_df.apply(lambda row:
#         ((np.fabs(row['T1 Reactive']) + np.fabs(row['T2 Reactive'])) / 2), axis=1), index=pair_buffer_df.index)
#     if 'delta' in features:
#         cluster_df['delta'] = pd.Series(pair_buffer_df.apply(lambda row:
#             (row['T2 Time'] - row['T1 Time']), axis=1), index=pair_buffer_df.index)
#         cluster_df['delta'] = cluster_df['delta'].apply(lambda x: int(x) / 6e10)
#     if 'hour_of_use' in features:
#         cluster_df['hour_of_use'] = pd.DatetimeIndex(pair_buffer_df['T1 Time']).hour
    
#     """
#     if 'sd_event' in features:
#         cluster_df['sd_event'] = pd.Series(pair_buffer_df.apply(lambda row:
#         (df.power[row['T1 Time']:row['T2 Time']]).std(), axis=1), index=pair_buffer_df.index)
#     """

#     X = cluster_df.values.reshape((len(cluster_df.index), len(features)))
#     ms = MeanShift(bin_seeding=True)
#     ms.fit(X)
#     labels = ms.labels_
#     cluster_centers = ms.cluster_centers_
#     labels_unique = np.unique(labels)
#     n_clusters_ = len(labels_unique)
#     return pd.DataFrame(cluster_centers, columns=features)